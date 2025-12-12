# ============================================
# HTTP STUB SERVER - PYTHON VERSION
# ============================================
# A configurable mock API server for testing and development
# This server simulates a real backend API but serves data from
# configuration files instead of a database

# Required Libraries Import
from flask import Flask, request, jsonify, Response
from flask_cors import CORS
import json
import time
import re
from datetime import datetime
import random
import string
import os
from threading import Thread
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Import category data (complete product catalog)
from data import category_data

# ============================================
# FLASK APP INITIALIZATION
# ============================================
app = Flask(__name__)
CORS(app)  # Enable CORS for frontend API access

# File paths configuration
CONFIG_PATH = 'config.json'
LOG_PATH = 'logs/requests.log'

# Global configuration storage
config = {}

# ============================================
# HELPER FUNCTIONS
# ============================================

def generate_random_id():
    """
    Generates a random unique ID for users, orders, etc.
    Returns a 9-character alphanumeric string
    Example: "a7b3c9d2e"
    """
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=9))


def load_config():
    """
    Loads the configuration file (config.json)
    Reads endpoint definitions and server settings from JSON file
    Returns True on success, False on failure
    """
    global config
    try:
        with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print('✅ Configuration loaded successfully')
        return True
    except Exception as e:
        print(f'❌ Error loading config: {str(e)}')
        return False


def log_request(method, url, query_params, status_code, duration_ms):
    """
    Logs each API request to the log file for debugging and monitoring
    
    Parameters:
    - method: HTTP method (GET, POST, etc.)
    - url: Request path
    - query_params: URL query parameters
    - status_code: HTTP response code (200, 404, etc.)
    - duration_ms: Request processing time in milliseconds
    """
    log_entry = {
        'timestamp': datetime.now().isoformat(),
        'method': method,
        'url': url,
        'query': query_params,
        'status': status_code,
        'duration': f'{duration_ms}ms'
    }
    
    try:
        with open(LOG_PATH, 'a', encoding='utf-8') as f:
            f.write(json.dumps(log_entry) + '\n')
    except Exception as e:
        print(f'Log write error: {str(e)}')
    
    print(f"[{log_entry['timestamp']}] {method} {url} - {status_code} ({duration_ms}ms)")


def process_template(obj, context):
    """
    Processes template variables and replaces them with actual values
    Enables dynamic response generation based on request data
    
    Supported template variables:
    - {{timestamp}} -> Current ISO timestamp
    - {{randomId}} -> Random unique identifier
    - {{query.name}} -> Value from URL query parameter
    - {{body.email}} -> Value from POST request body
    - {{params.id}} -> Value from URL path parameter
    
    Parameters:
    - obj: Response object containing template variables
    - context: Dictionary with query, body, and params data
    
    Returns: Processed object with all variables replaced
    """
    # Convert object to JSON string for processing
    json_str = json.dumps(obj)
    
    # Replace timestamp placeholder with current time
    json_str = json_str.replace('{{timestamp}}', datetime.now().isoformat())
    
    # Replace randomId placeholders (each occurrence gets unique ID)
    while '{{randomId}}' in json_str:
        json_str = json_str.replace('{{randomId}}', generate_random_id(), 1)
    
    # Replace query parameter placeholders
    for key, value in context.get('query', {}).items():
        placeholder = '{{query.' + key + '}}'
        json_str = json_str.replace(placeholder, str(value))
    
    # Replace body parameter placeholders
    for key, value in context.get('body', {}).items():
        placeholder = '{{body.' + key + '}}'
        json_str = json_str.replace(placeholder, str(value))
    
    # Replace path parameter placeholders
    for key, value in context.get('params', {}).items():
        placeholder = '{{params.' + key + '}}'
        json_str = json_str.replace(placeholder, str(value))
    
    # Convert back to object and return
    return json.loads(json_str)


def path_matches(endpoint_path, request_path):
    """
    Checks if a request path matches an endpoint pattern
    Supports dynamic path parameters like /order/:orderId
    
    Example:
    - endpoint_path: "/order/:orderId"
    - request_path: "/order/ORD123"
    - Returns: (True, {'orderId': 'ORD123'})
    
    Parameters:
    - endpoint_path: Pattern with :param placeholders
    - request_path: Actual request URL path
    
    Returns: Tuple of (match_found, extracted_params)
    """
    # Convert :param syntax to regex named groups
    pattern = endpoint_path
    pattern = re.sub(r':(\w+)', r'(?P<\1>[^/]+)', pattern)
    pattern = f'^{pattern}$'
    
    # Attempt to match the pattern
    match = re.match(pattern, request_path)
    if match:
        return True, match.groupdict()
    return False, {}


# ============================================
# MIDDLEWARE - Request/Response Interceptors
# ============================================

@app.before_request
def before_request():
    """
    Executes before each request
    Stores request start time for performance logging
    """
    request.start_time = time.time()


@app.after_request
def after_request(response):
    """
    Executes after each request
    Logs request details to file for monitoring and debugging
    """
    # Calculate request processing duration in milliseconds
    duration = int((time.time() - request.start_time) * 1000)
    
    # Log the request details
    log_request(
        request.method,
        request.path,
        dict(request.args),
        response.status_code,
        duration
    )
    
    return response


# ============================================
# AUTHENTICATION MIDDLEWARE
# ============================================

def check_auth():
    """
    Validates user authentication via token
    Checks for authorization token in headers or query parameters
    
    Returns:
    - None: If token is present (authentication successful)
    - Response tuple: If token is missing (401 Unauthorized error)
    """
    # Check for token in Authorization header or query parameter
    token = request.headers.get('Authorization') or request.args.get('token')
    
    if not token:
        # Return 401 Unauthorized if no token found
        return jsonify({
            'success': False,
            'error': 'Unauthorized',
            'message': 'Please create an account or login first to browse products!',
            'redirectTo': '/register',
            'timestamp': datetime.now().isoformat()
        }), 401
    
    return None  # Token present, authentication successful


# ============================================
# ROOT ENDPOINT (Welcome Page)
# ============================================

@app.route('/', methods=['GET'])
def home():
    """
    Root endpoint - displays server information and available endpoints
    """
    return jsonify({
        'message': 'HTTP Stub Server - Python Version',
        'status': 'running',
        'port': config.get('port', 5600),
        'version': '1.0.0',
        'endpoints': {
            'authentication': ['/register', '/login'],
            'categories': ['/categories', '/categories/:id'],
            'products': ['/categories/:id/subcategories/:id', '/categories/:id/subcategories/:id/products/:id'],
            'cart': ['/cart', '/cart/add'],
            'orders': ['/orders', '/order/place', '/order/:id'],
            'other': ['/search', '/profile']
        },
        'documentation': 'See README_PYTHON.md for complete API documentation',
        'test': 'Run python test_api.py to test all endpoints'
    })

# ============================================
# DYNAMIC CATEGORY ROUTES (Authentication Required)
# ============================================

@app.route('/categories/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """
    Returns category details with its subcategories
    Used when user selects a category to view available subcategories
    
    Example: GET /categories/1 -> Returns Electronics subcategories
    
    Authentication: Required (token must be provided)
    Response: Category name, subcategories list, item counts
    """
    # Verify authentication
    auth_error = check_auth()
    if auth_error:
        return auth_error
    
    # Convert category ID to string (data.py uses string keys)
    category_key = str(category_id)
    
    # Validate category exists
    if category_key not in category_data:
        return jsonify({'error': 'Category not found'}), 404
    
    category = category_data[category_key]
    
    # Build subcategories list with item counts
    subcategories = []
    for sub_id, sub_data in category['subcategories'].items():
        subcategories.append({
            'id': int(sub_id),
            'name': sub_data['name'],
            'itemCount': len(sub_data['products'])
        })
    
    # Prepare response data
    response_data = {
        'categoryId': category_id,
        'categoryName': category['name'],
        'subcategories': subcategories,
        'timestamp': datetime.now().isoformat()
    }
    
    # Simulate network delay (400ms) for realistic API behavior
    time.sleep(0.4)
    
    return jsonify(response_data)


@app.route('/categories/<int:category_id>/subcategories/<int:subcategory_id>', methods=['GET'])
def get_subcategory_products(category_id, subcategory_id):
    """
    Returns all products within a specific subcategory
    Used to display product listings when user selects a subcategory
    
    Example: GET /categories/1/subcategories/1 -> Returns all Laptops
    
    Authentication: Required
    Response: Product list with prices, ratings, stock status, etc.
    """
    # Verify authentication
    auth_error = check_auth()
    if auth_error:
        return auth_error
    
    # Convert IDs to strings for data lookup
    cat_key = str(category_id)
    sub_key = str(subcategory_id)
    
    # Validate category and subcategory exist
    if cat_key not in category_data or sub_key not in category_data[cat_key]['subcategories']:
        return jsonify({'error': 'Subcategory not found'}), 404
    
    subcategory = category_data[cat_key]['subcategories'][sub_key]
    
    # Prepare response with product list
    response_data = {
        'categoryId': category_id,
        'subcategoryId': subcategory_id,
        'subcategoryName': subcategory['name'],
        'products': subcategory['products'],
        'totalProducts': len(subcategory['products']),
        'timestamp': datetime.now().isoformat()
    }
    
    # Simulate network delay (500ms)
    time.sleep(0.5)
    
    return jsonify(response_data)


@app.route('/categories/<int:category_id>/subcategories/<int:subcategory_id>/products/<int:product_id>', methods=['GET'])
def get_product_details(category_id, subcategory_id, product_id):
    """
    Returns complete details for a single product
    Used for product detail page with full specifications and delivery info
    
    Example: GET /categories/1/subcategories/1/products/1001 -> Dell Inspiron details
    
    Authentication: Required
    Response: Enhanced product data with description, images, delivery info
    """
    # Verify authentication
    auth_error = check_auth()
    if auth_error:
        return auth_error
    
    # Convert IDs to strings for data lookup
    cat_key = str(category_id)
    sub_key = str(subcategory_id)
    
    # Validate category and subcategory exist
    if cat_key not in category_data or sub_key not in category_data[cat_key]['subcategories']:
        return jsonify({'error': 'Product not found'}), 404
    
    subcategory = category_data[cat_key]['subcategories'][sub_key]
    
    # Find the specific product
    product = None
    for p in subcategory['products']:
        if p['id'] == product_id:
            product = p
            break
    
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    # Build enhanced product details with additional information
    response_data = {
        'productId': product_id,
        **product,  # Include all existing product fields
        'description': f"Premium quality {product['name']}. {product.get('specs', 'High quality product.')}",
        'images': [
            f"{product['name'].lower().replace(' ', '_')}_1.jpg",
            f"{product['name'].lower().replace(' ', '_')}_2.jpg"
        ],
        'deliveryInfo': {
            'estimatedDays': '3-5 days',
            'freeDelivery': product['price'] > 500,
            'returnPolicy': '7 days return'
        },
        'timestamp': datetime.now().isoformat()
    }
    
    # Simulate network delay (300ms)
    time.sleep(0.3)
    
    return jsonify(response_data)


# ============================================
# UNIVERSAL ROUTE HANDLER
# ============================================

@app.route('/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH'])
def universal_handler(path):
    """
    Dynamically handles all endpoints defined in config.json
    This is the core routing mechanism that enables configuration-driven API behavior
    
    Process:
    1. Matches request path against configured endpoints
    2. Processes template variables in response
    3. Applies configured delays for realistic simulation
    4. Returns response with appropriate status code and headers
    
    Parameters:
    - path: Request URL path (captured by Flask)
    
    Returns: JSON response based on configuration
    """
    # Prepend slash to path for matching
    request_path = '/' + path
    
    # Verify endpoints are configured
    if 'endpoints' not in config:
        return jsonify({'error': 'No endpoints configured'}), 404
    
    # Search for matching endpoint in configuration
    matched_endpoint = None
    path_params = {}
    
    for endpoint in config['endpoints']:
        # Check HTTP method match
        if endpoint['method'].upper() != request.method:
            continue
        
        # Check path pattern match
        matches, params = path_matches(endpoint['path'], request_path)
        if matches:
            matched_endpoint = endpoint
            path_params = params
            break
    
    # Return 404 if no matching endpoint found
    if not matched_endpoint:
        return jsonify({
            'error': 'Endpoint not found in current configuration',
            'path': request_path,
            'method': request.method
        }), 404
    
    # Apply configured delay (simulates network latency)
    delay = matched_endpoint.get('delay', 0)
    if delay > 0:
        time.sleep(delay / 1000.0)  # Convert milliseconds to seconds
    
    # Build context for template processing
    # Only try to get JSON body for methods that typically have a body
    body_data = {}
    if request.method in ['POST', 'PUT', 'PATCH']:
        try:
            body_data = request.get_json(silent=True) or {}
            # Debug: Print body data
            print(f"DEBUG: Body data received: {body_data}")
        except Exception as e:
            print(f"DEBUG: Error getting body: {str(e)}")
            body_data = {}
    
    context = {
        'query': dict(request.args),           # URL query parameters
        'params': path_params,                  # Path parameters (:id syntax)
        'body': body_data                       # POST/PUT request body
    }
    
    # Debug: Print context
    print(f"DEBUG: Context for template: {context}")
    
    # Process template variables in response
    response_data = process_template(matched_endpoint['response'], context)
    
    # Create response with processed data
    response = jsonify(response_data)
    
    # Apply custom headers if specified
    if 'headers' in matched_endpoint:
        for key, value in matched_endpoint['headers'].items():
            response.headers[key] = value
    
    # Return response with configured status code
    return response, matched_endpoint['status']


# ============================================
# CONFIG FILE WATCHER (Auto-reload)
# ============================================

class ConfigFileHandler(FileSystemEventHandler):
    """
    Monitors configuration file for changes and triggers reload
    Enables hot-reloading of endpoints without server restart
    """
    def on_modified(self, event):
        if event.src_path.endswith('config.json'):
            print('🔄 Config file changed, reloading...')
            time.sleep(0.1)  # Brief delay to ensure file write is complete
            load_config()
            print('✅ Configuration reloaded - new endpoints will be used automatically')


def start_config_watcher():
    """
    Starts the configuration file watcher in a background thread
    Monitors current directory for config.json modifications
    """
    try:
        event_handler = ConfigFileHandler()
        observer = Observer()
        observer.schedule(event_handler, path='.', recursive=False)
        observer.start()
        print('🔄 Auto-reload: ENABLED (config changes apply instantly)')
    except Exception as e:
        print(f'⚠️  Auto-reload: DISABLED (watchdog error: {str(e)})')
        print('   Config changes will require server restart')


# ============================================
# SERVER STARTUP
# ============================================

def main():
    """
    Main entry point for the HTTP Stub Server
    Can be called from command line or imported as a module
    """
    # Load initial configuration
    if not load_config():
        print('Failed to start server due to config error')
        exit(1)
    
    # Get port from config (default: 5600)
    PORT = config.get('port', 5600)
    
    # Display startup information
    print(f'🚀 HTTP Stub Server running on http://localhost:{PORT}')
    print(f'📝 Logs are being written to: {LOG_PATH}')
    print(f'⚙️  Config file: {CONFIG_PATH}')
    
    # List all configured endpoints
    print('\n📋 Available endpoints:')
    if 'endpoints' in config:
        for ep in config['endpoints']:
            delay_info = f"[delay: {ep['delay']}ms]" if ep.get('delay') else ''
            print(f"   {ep['method']} {ep['path']} ({ep['status']}) {delay_info}")
    
    # Start config file watcher in background thread
    watcher_thread = Thread(target=start_config_watcher, daemon=True)
    watcher_thread.start()
    
    # Start Flask development server
    # debug=False: Production mode for clean output during demos
    # host='0.0.0.0': Allow network access (not just localhost)
    app.run(host='0.0.0.0', port=PORT, debug=False)


if __name__ == '__main__':
    main()
