# HTTP Stub Server - Python Version 🐍

## Ye Kya Hai? (What is this?)

Ye ek **Mock API Server** hai jo testing aur development ke liye use hota hai. Real backend ki tarah kaam karta hai lekin database ki zaroorat nahi hoti.

**Judges ko explain karna:**
> "Ye server ek configurable API hai jo JSON file se endpoints read karta hai aur dynamic responses generate karta hai. Isme authentication, logging, auto-reload jaise features hain jo production-ready applications mein hote hain."

---

## Features ✨

1. **Dynamic Endpoints** - Config file se endpoints automatically load hote hain
2. **Authentication** - Token-based security (login/register required)
3. **Template Variables** - Dynamic data generation (`{{timestamp}}`, `{{randomId}}`, etc.)
4. **Auto-Reload** - Config file change hone pe automatically reload
5. **Request Logging** - Har API call ka record `requests.log` mein
6. **Delay Simulation** - Real API ki tarah network delay
7. **Complete E-commerce Data** - 6 categories, 18 subcategories, 60+ products

---

## Installation (Setup Kaise Karein)

### Step 1: Python Install Karein
Python 3.8 ya usse upar chahiye. Check karein:
```bash
python --version
```

### Step 2: Dependencies Install Karein
```bash
pip install -r requirements.txt
```

Ye packages install honge:
- **Flask** - Web server framework
- **Flask-CORS** - Frontend se connect hone ke liye
- **watchdog** - Config file auto-reload ke liye

### Step 3: Server Start Karein
```bash
python server.py
```

Server start ho jayega: `http://localhost:5600`

---

## File Structure (Kaunsi File Kya Karti Hai)

```
├── server.py           # Main server file (saara logic yahan hai)
├── data.py             # Products ka complete data (database ki tarah)
├── config.json         # API endpoints configuration
├── requirements.txt    # Python packages list
├── requests.log        # API calls ka log (automatically banta hai)
└── README_PYTHON.md    # Ye file (instructions)
```

---

## API Endpoints (Kya Kya Available Hai)

### 1. Authentication APIs

#### Register (Naya Account Banana)
```http
POST /register
Content-Type: application/json

{
  "name": "Rahul Kumar",
  "email": "rahul@example.com",
  "phone": "9876543210",
  "password": "password123"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Account created successfully!",
  "user": {
    "id": "a7b3c9d2e",
    "name": "Rahul Kumar",
    "email": "rahul@example.com"
  },
  "token": "x8y2z5k9m"
}
```

#### Login (Account Mein Login Karna)
```http
POST /login
Content-Type: application/json

{
  "email": "rahul@example.com",
  "password": "password123"
}
```

---

### 2. Product Browsing APIs (Authentication Required)

**Important:** Ye APIs use karne ke liye token chahiye!

Token bhejne ke 2 tarike:
1. **Header mein:** `Authorization: your_token_here`
2. **Query parameter mein:** `/categories?token=your_token_here`

#### Get All Categories
```http
GET /categories
Authorization: your_token_here
```

#### Get Category Details (Subcategories)
```http
GET /categories/1
Authorization: your_token_here
```
Example: Category 1 = Electronics

#### Get Products in Subcategory
```http
GET /categories/1/subcategories/1
Authorization: your_token_here
```
Example: Electronics > Laptops

#### Get Single Product Details
```http
GET /categories/1/subcategories/1/products/1001
Authorization: your_token_here
```
Example: Dell Inspiron 15 ki complete details

---

### 3. Shopping Cart APIs

#### Add to Cart
```http
POST /cart/add
Authorization: your_token_here
Content-Type: application/json

{
  "productId": 2001,
  "productName": "Men's Winter Sweater",
  "price": 700,
  "quantity": 1,
  "size": "L",
  "color": "Black"
}
```

#### View Cart
```http
GET /cart
Authorization: your_token_here
```

---

### 4. Order APIs

#### Place Order
```http
POST /order/place
Authorization: your_token_here
Content-Type: application/json

{
  "name": "Rahul Kumar",
  "email": "rahul@example.com",
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
```

#### Get All Orders
```http
GET /orders
Authorization: your_token_here
```

#### Track Order
```http
GET /order/ORD123456
Authorization: your_token_here
```

---

## Available Categories (Kya Kya Products Hain)

| Category ID | Name | Subcategories |
|------------|------|---------------|
| 1 | Electronics | Laptops, Headphones, Cameras |
| 2 | Clothing Store | Men, Women, Baby Clothing |
| 3 | TV & Appliances | TVs, Refrigerators, Washing Machines |
| 4 | Smartphones | Android, iPhones, Budget Phones |
| 5 | Kitchen Ware | Cookware, Appliances, Dinnerware |
| 6 | Home Decor | Wall Art, Lighting, Cushions & Curtains |

**Total:** 6 categories, 18 subcategories, 60+ products

---

## Template Variables (Dynamic Data)

Config file mein ye placeholders use kar sakte ho:

| Variable | Description | Example |
|----------|-------------|---------|
| `{{timestamp}}` | Current date/time | `2025-12-02T10:30:00Z` |
| `{{randomId}}` | Random unique ID | `a7b3c9d2e` |
| `{{query.name}}` | URL parameter | `/api?name=Rahul` → `Rahul` |
| `{{body.email}}` | POST data | Request body se email |
| `{{params.id}}` | Path parameter | `/order/:id` → order ID |

---

## Config File Kaise Edit Karein

`config.json` file mein naye endpoints add kar sakte ho:

```json
{
  "port": 5600,
  "endpoints": [
    {
      "path": "/test",
      "method": "GET",
      "status": 200,
      "delay": 500,
      "response": {
        "message": "Hello {{query.name}}!",
        "timestamp": "{{timestamp}}"
      }
    }
  ]
}
```

**Auto-reload hai!** Config save karte hi changes apply ho jayenge, server restart ki zaroorat nahi.

---

## Judges Ko Demo Kaise Dein

### 1. Server Start Karein
```bash
python server.py
```

### 2. Postman Ya Browser Mein Test Karein

**Step 1:** Register karein
```
POST http://localhost:5600/register
Body: {"name": "Test User", "email": "test@test.com", "phone": "1234567890"}
```

**Step 2:** Token copy karein response se

**Step 3:** Categories dekhen
```
GET http://localhost:5600/categories
Header: Authorization: your_token_here
```

**Step 4:** Products browse karein
```
GET http://localhost:5600/categories/1/subcategories/1
Header: Authorization: your_token_here
```

### 3. Key Points Explain Karein

1. **Authentication:** "Bina login ke products nahi dekh sakte - security feature"
2. **Dynamic Data:** "Har request pe unique ID aur timestamp generate hota hai"
3. **Logging:** "Har API call ka record requests.log mein save hota hai"
4. **Auto-reload:** "Config file change karne pe automatically reload ho jata hai"
5. **Real-world Simulation:** "Delays aur error handling real API ki tarah hai"

---

## Troubleshooting (Agar Problem Aaye)

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Port already in use"
`config.json` mein port number change karein:
```json
{
  "port": 5601
}
```

### Server start nahi ho raha
Check karein:
1. Python version 3.8+ hai?
2. Saare packages install hain?
3. `config.json` file valid JSON hai?

---

## Code Mein Important Functions

### 1. `load_config()`
Config file ko read karta hai aur memory mein load karta hai.

### 2. `process_template()`
Template variables (`{{timestamp}}`, etc.) ko actual values se replace karta hai.

### 3. `check_auth()`
User logged in hai ya nahi check karta hai token se.

### 4. `universal_handler()`
Config file se endpoints read karke dynamically handle karta hai.

### 5. `ConfigFileHandler`
Config file ke changes detect karta hai aur auto-reload karta hai.

---

## Advantages (Node.js Se Better Kaise Hai)

1. **Simple Syntax** - Python zyada readable hai
2. **Less Code** - Same functionality, kam lines
3. **Easy to Learn** - Beginners ke liye perfect
4. **Better Comments** - Hindi mein explain karna easy
5. **No npm/node_modules** - Lightweight setup

---

## Questions Judges Pooch Sakte Hain

**Q: Ye real database use karta hai?**
A: Nahi, ye mock server hai. Data `data.py` file mein hardcoded hai. Real project mein MongoDB/MySQL use hoga.

**Q: Authentication real hai?**
A: Nahi, ye simulated hai. Real mein JWT tokens aur password hashing hogi.

**Q: Config file kaise reload hota hai?**
A: `watchdog` library file changes detect karti hai aur automatically reload karti hai.

**Q: Ye production mein use kar sakte hain?**
A: Nahi, ye sirf testing/development ke liye hai. Production mein proper backend chahiye.

**Q: Frontend se kaise connect karein?**
A: CORS enabled hai, kisi bhi frontend (React, HTML) se directly API call kar sakte ho.

---

## Next Steps (Aage Kya Kar Sakte Ho)

1. ✅ Frontend banao (HTML/React) jo is API ko use kare
2. ✅ Real database integrate karo (MongoDB/PostgreSQL)
3. ✅ JWT authentication implement karo
4. ✅ Payment gateway add karo
5. ✅ Email notifications add karo

---

## Support

Agar koi doubt ho toh:
1. Code mein comments padho (har line explain ki hai)
2. `requests.log` file check karo (debugging ke liye)
3. Console output dekho (errors wahan dikhenge)

**All the best for your presentation! 🚀**
