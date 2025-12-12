# ============================================
# API TESTING SCRIPT
# ============================================
# Automated testing suite for the HTTP Stub Server
# Tests all major API endpoints with realistic scenarios
# Usage: python test_api.py

import requests
import json
import time

# Server configuration
BASE_URL = "http://localhost:5600"

# ANSI color codes for terminal output (may not work on all Windows terminals)
GREEN = '\033[92m'
RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'

def print_success(message):
    """Prints success message in green"""
    print(f"{GREEN}✅ {message}{RESET}")

def print_error(message):
    """Prints error message in red"""
    print(f"{RED}❌ {message}{RESET}")

def print_info(message):
    """Prints informational message in blue"""
    print(f"{BLUE}ℹ️  {message}{RESET}")

def print_response(response):
    """Prints formatted JSON response"""
    print(json.dumps(response.json(), indent=2))
    print()

# ============================================
# TEST 1: USER REGISTRATION
# ============================================
def test_register():
    """Tests user registration endpoint"""
    print_info("TEST 1: Creating new account...")
    
    url = f"{BASE_URL}/register"
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "9876543210",
        "password": "password123"
    }
    
    try:
        response = requests.post(url, json=data)
        
        if response.status_code == 201:
            print_success("Account created successfully!")
            print_response(response)
            
            # Extract and return token for subsequent tests
            token = response.json().get('token')
            return token
        else:
            print_error(f"Failed with status code: {response.status_code}")
            return None
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

# ============================================
# TEST 2: USER LOGIN
# ============================================
def test_login():
    """Tests user login endpoint"""
    print_info("TEST 2: Logging in...")
    
    url = f"{BASE_URL}/login"
    data = {
        "email": "test@example.com",
        "password": "password123"
    }
    
    try:
        response = requests.post(url, json=data)
        
        if response.status_code == 200:
            print_success("Login successful!")
            print_response(response)
            return response.json().get('token')
        else:
            print_error(f"Failed with status code: {response.status_code}")
            return None
            
    except Exception as e:
        print_error(f"Error: {str(e)}")
        return None

# ============================================
# TEST 3: AUTHENTICATION VALIDATION
# ============================================
def test_categories_without_auth():
    """Tests that protected endpoints require authentication"""
    print_info("TEST 3: Trying to get categories without token (should fail)...")
    
    url = f"{BASE_URL}/categories"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 401:
            print_success("Correctly blocked! Authentication working.")
            print_response(response)
        else:
            print_error("Authentication not working properly!")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")

# ============================================
# TEST 4: GET CATEGORIES (With Token)
# ============================================
def test_categories_with_auth(token):
    print_info("TEST 4: Getting all categories with token...")
    
    url = f"{BASE_URL}/categories"
    headers = {"Authorization": token}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print_success("Categories fetched successfully!")
            print_response(response)
        else:
            print_error(f"Failed with status code: {response.status_code}")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")

# ============================================
# TEST 5: GET CATEGORY DETAILS (Electronics)
# ============================================
def test_category_details(token):
    print_info("TEST 5: Getting Electronics category details...")
    
    url = f"{BASE_URL}/categories/1"
    headers = {"Authorization": token}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print_success("Category details fetched!")
            print_response(response)
        else:
            print_error(f"Failed with status code: {response.status_code}")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")

# ============================================
# TEST 6: GET PRODUCTS (Laptops)
# ============================================
def test_products(token):
    print_info("TEST 6: Getting Laptops products...")
    
    url = f"{BASE_URL}/categories/1/subcategories/1"
    headers = {"Authorization": token}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print_success("Products fetched!")
            print_response(response)
        else:
            print_error(f"Failed with status code: {response.status_code}")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")

# ============================================
# TEST 7: GET SINGLE PRODUCT DETAILS
# ============================================
def test_product_details(token):
    print_info("TEST 7: Getting Dell Inspiron 15 details...")
    
    url = f"{BASE_URL}/categories/1/subcategories/1/products/1001"
    headers = {"Authorization": token}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print_success("Product details fetched!")
            print_response(response)
        else:
            print_error(f"Failed with status code: {response.status_code}")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")

# ============================================
# TEST 8: ADD TO CART
# ============================================
def test_add_to_cart(token):
    print_info("TEST 8: Adding product to cart...")
    
    url = f"{BASE_URL}/cart/add"
    headers = {"Authorization": token}
    data = {
        "productId": 2001,
        "productName": "Men's Winter Sweater",
        "price": 700,
        "quantity": 1,
        "size": "L",
        "color": "Black"
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            print_success("Product added to cart!")
            print_response(response)
        else:
            print_error(f"Failed with status code: {response.status_code}")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")

# ============================================
# TEST 9: VIEW CART
# ============================================
def test_view_cart(token):
    print_info("TEST 9: Viewing cart...")
    
    url = f"{BASE_URL}/cart"
    headers = {"Authorization": token}
    
    try:
        response = requests.get(url, headers=headers)
        
        if response.status_code == 200:
            print_success("Cart fetched!")
            print_response(response)
        else:
            print_error(f"Failed with status code: {response.status_code}")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")

# ============================================
# TEST 10: PLACE ORDER
# ============================================
def test_place_order(token):
    print_info("TEST 10: Placing order...")
    
    url = f"{BASE_URL}/order/place"
    headers = {"Authorization": token}
    data = {
        "name": "Test User",
        "email": "test@example.com",
        "phone": "9876543210",
        "address": "123 Main Street",
        "city": "Mumbai",
        "state": "Maharashtra",
        "pincode": "400001",
        "productId": 2001,
        "productName": "Men's Winter Sweater",
        "price": 700,
        "quantity": 1,
        "size": "L",
        "paymentMethod": "COD",
        "totalAmount": 770
    }
    
    try:
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 201:
            print_success("Order placed successfully!")
            print_response(response)
        else:
            print_error(f"Failed with status code: {response.status_code}")
            
    except Exception as e:
        print_error(f"Error: {str(e)}")

# ============================================
# MAIN FUNCTION - Saare Tests Run Karta Hai
# ============================================
def main():
    print("\n" + "="*60)
    print("🚀 HTTP STUB SERVER - API TESTING")
    print("="*60 + "\n")
    
    # Check karo ki server running hai ya nahi
    try:
        response = requests.get(BASE_URL)
        print_success("Server is running!")
    except:
        print_error("Server is not running! Please start it first:")
        print("   python server.py")
        return
    
    print("\n" + "-"*60 + "\n")
    
    # Test 1: Register
    token = test_register()
    if not token:
        print_error("Registration failed! Stopping tests.")
        return
    
    time.sleep(1)
    print("-"*60 + "\n")
    
    # Test 2: Login
    test_login()
    time.sleep(1)
    print("-"*60 + "\n")
    
    # Test 3: Categories without auth (should fail)
    test_categories_without_auth()
    time.sleep(1)
    print("-"*60 + "\n")
    
    # Test 4: Categories with auth
    test_categories_with_auth(token)
    time.sleep(1)
    print("-"*60 + "\n")
    
    # Test 5: Category details
    test_category_details(token)
    time.sleep(1)
    print("-"*60 + "\n")
    
    # Test 6: Products list
    test_products(token)
    time.sleep(1)
    print("-"*60 + "\n")
    
    # Test 7: Single product details
    test_product_details(token)
    time.sleep(1)
    print("-"*60 + "\n")
    
    # Test 8: Add to cart
    test_add_to_cart(token)
    time.sleep(1)
    print("-"*60 + "\n")
    
    # Test 9: View cart
    test_view_cart(token)
    time.sleep(1)
    print("-"*60 + "\n")
    
    # Test 10: Place order
    test_place_order(token)
    
    print("\n" + "="*60)
    print("✅ ALL TESTS COMPLETED!")
    print("="*60 + "\n")
    
    print_info("Check 'requests.log' file to see all API calls logged!")

if __name__ == "__main__":
    main()
