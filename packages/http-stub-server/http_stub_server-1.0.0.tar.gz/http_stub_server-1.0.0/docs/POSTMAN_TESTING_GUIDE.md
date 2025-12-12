# Postman Testing Guide - Python Server

## Postman Mein Kaise Test Karein

---

## Setup (One-time)

### Step 1: Postman Install Karo
Download: https://www.postman.com/downloads/

### Step 2: New Collection Banao
1. Postman open karo
2. "Collections" pe click karo
3. "+" button pe click karo
4. Name: "HTTP Stub Server - Python"

---

## Test Sequence (Order Mein Karo)

### 🔹 TEST 1: Register (Account Banana)

**Request Type:** POST  
**URL:** `http://localhost:5600/register`

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
  "name": "Rahul Kumar",
  "email": "rahul@example.com",
  "phone": "9876543210",
  "password": "password123"
}
```

**Expected Response (201):**
```json
{
  "success": true,
  "message": "Account created successfully!",
  "user": {
    "id": "a7b3c9d2e",
    "name": "Rahul Kumar",
    "email": "rahul@example.com",
    "phone": "9876543210"
  },
  "token": "x8y2z5k9m",
  "timestamp": "2025-12-02T10:30:00.000Z"
}
```

**Important:** Token copy kar lo! Baaki tests mein use hoga.

---

### 🔹 TEST 2: Login

**Request Type:** POST  
**URL:** `http://localhost:5600/login`

**Headers:**
```
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
  "email": "rahul@example.com",
  "password": "password123"
}
```

**Expected Response (200):**
```json
{
  "success": true,
  "message": "Login successful!",
  "user": {
    "id": "a7b3c9d2e",
    "email": "rahul@example.com",
    "name": "Rahul Kumar"
  },
  "token": "x8y2z5k9m",
  "timestamp": "2025-12-02T10:31:00.000Z"
}
```

---

### 🔹 TEST 3: Get Categories (Without Token - Should Fail)

**Request Type:** GET  
**URL:** `http://localhost:5600/categories`

**Headers:** (kuch nahi)

**Expected Response (401):**
```json
{
  "success": false,
  "error": "Unauthorized",
  "message": "Please create an account or login first to browse products!",
  "redirectTo": "/register",
  "timestamp": "2025-12-02T10:32:00.000Z"
}
```

**Ye test dikhata hai ki authentication kaam kar raha hai!**

---

### 🔹 TEST 4: Get Categories (With Token)

**Request Type:** GET  
**URL:** `http://localhost:5600/categories`

**Headers:**
```
Authorization: your_token_here
```
(Token ko TEST 1 se copy karo)

**Expected Response (200):**
```json
{
  "categories": [
    {"id": 1, "name": "Electronics", "icon": "electronics.png", "itemCount": 250},
    {"id": 2, "name": "Clothing Store", "icon": "clothing.png", "itemCount": 500},
    {"id": 3, "name": "TV & Appliances", "icon": "tv.png", "itemCount": 180},
    {"id": 4, "name": "Smartphones", "icon": "phone.png", "itemCount": 120},
    {"id": 5, "name": "Kitchen Ware", "icon": "kitchen.png", "itemCount": 300},
    {"id": 6, "name": "Home Decor", "icon": "home.png", "itemCount": 220}
  ],
  "timestamp": "2025-12-02T10:33:00.000Z"
}
```

---

### 🔹 TEST 5: Get Category Details (Electronics)

**Request Type:** GET  
**URL:** `http://localhost:5600/categories/1`

**Headers:**
```
Authorization: your_token_here
```

**Expected Response (200):**
```json
{
  "categoryId": 1,
  "categoryName": "Electronics",
  "subcategories": [
    {"id": 1, "name": "Laptops", "itemCount": 4},
    {"id": 2, "name": "Headphones", "itemCount": 3},
    {"id": 3, "name": "Cameras", "itemCount": 3}
  ],
  "timestamp": "2025-12-02T10:34:00.000Z"
}
```

**Note:** 400ms delay hoga (real API ki tarah)

---

### 🔹 TEST 6: Get Products (Laptops)

**Request Type:** GET  
**URL:** `http://localhost:5600/categories/1/subcategories/1`

**Headers:**
```
Authorization: your_token_here
```

**Expected Response (200):**
```json
{
  "categoryId": 1,
  "subcategoryId": 1,
  "subcategoryName": "Laptops",
  "products": [
    {
      "id": 1001,
      "name": "Dell Inspiron 15",
      "price": 45000,
      "originalPrice": 55000,
      "discount": "18% off",
      "rating": 4.5,
      "inStock": true,
      "specs": "Intel i5, 8GB RAM, 512GB SSD"
    },
    {
      "id": 1002,
      "name": "HP Pavilion",
      "price": 48000,
      "originalPrice": 60000,
      "discount": "20% off",
      "rating": 4.3,
      "inStock": true,
      "specs": "Intel i5, 16GB RAM, 1TB SSD"
    }
    // ... more products
  ],
  "totalProducts": 4,
  "timestamp": "2025-12-02T10:35:00.000Z"
}
```

**Note:** 500ms delay hoga

---

### 🔹 TEST 7: Get Single Product Details

**Request Type:** GET  
**URL:** `http://localhost:5600/categories/1/subcategories/1/products/1001`

**Headers:**
```
Authorization: your_token_here
```

**Expected Response (200):**
```json
{
  "productId": 1001,
  "id": 1001,
  "name": "Dell Inspiron 15",
  "price": 45000,
  "originalPrice": 55000,
  "discount": "18% off",
  "rating": 4.5,
  "inStock": true,
  "specs": "Intel i5, 8GB RAM, 512GB SSD",
  "description": "Premium quality Dell Inspiron 15. Intel i5, 8GB RAM, 512GB SSD",
  "images": [
    "dell_inspiron_15_1.jpg",
    "dell_inspiron_15_2.jpg"
  ],
  "deliveryInfo": {
    "estimatedDays": "3-5 days",
    "freeDelivery": true,
    "returnPolicy": "7 days return"
  },
  "timestamp": "2025-12-02T10:36:00.000Z"
}
```

**Note:** 300ms delay hoga

---

### 🔹 TEST 8: Add to Cart

**Request Type:** POST  
**URL:** `http://localhost:5600/cart/add`

**Headers:**
```
Authorization: your_token_here
Content-Type: application/json
```

**Body (raw JSON):**
```json
{
  "productId": 2001,
  "productName": "Men's Winter Sweater",
  "price": 700,
  "quantity": 1,
  "size": "L",
  "color": "Black"
}
```

**Expected Response (200):**
```json
{
  "success": true,
  "message": "Item added to cart successfully!",
  "cartItem": {
    "productId": "2001",
    "productName": "Men's Winter Sweater",
    "price": "700",
    "quantity": "1",
    "size": "L",
    "color": "Black"
  },
  "cartTotal": {
    "items": 1,
    "subtotal": "700",
    "tax": 70,
    "total": 770
  },
  "timestamp": "2025-12-02T10:37:00.000Z"
}
```

**Note:** 500ms delay hoga

---

### 🔹 TEST 9: View Cart

**Request Type:** GET  
**URL:** `http://localhost:5600/cart`

**Headers:**
```
Authorization: your_token_here
```

**Expected Response (200):**
```json
{
  "cartId": "a7b3c9d2e",
  "items": [
    {
      "productId": 101,
      "name": "Men's Winter Sweater",
      "price": 700,
      "quantity": 1,
      "size": "L",
      "color": "Black",
      "image": "sweater1.jpg"
    }
  ],
  "summary": {
    "subtotal": 700,
    "tax": 70,
    "deliveryCharges": 0,
    "discount": 0,
    "total": 770
  },
  "timestamp": "2025-12-02T10:38:00.000Z"
}
```

---

### 🔹 TEST 10: Place Order

**Request Type:** POST  
**URL:** `http://localhost:5600/order/place`

**Headers:**
```
Authorization: your_token_here
Content-Type: application/json
```

**Body (raw JSON):**
```json
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

**Expected Response (201):**
```json
{
  "success": true,
  "message": "Your order has been placed successfully!",
  "orderId": "ORDa7b3c9d2e",
  "orderDetails": {
    "customerName": "Rahul Kumar",
    "email": "rahul@example.com",
    "phone": "9876543210",
    "address": {
      "street": "123 Main Street",
      "city": "Mumbai",
      "state": "Maharashtra",
      "pincode": "400001"
    },
    "items": [
      {
        "productId": "2001",
        "productName": "Men's Winter Sweater",
        "price": "700",
        "quantity": "1",
        "size": "L"
      }
    ],
    "paymentMethod": "COD",
    "totalAmount": "770"
  },
  "estimatedDelivery": "3-5 business days",
  "trackingId": "TRKx8y2z5k9m",
  "orderPlacedAt": "2025-12-02T10:39:00.000Z"
}
```

**Note:** 3000ms (3 seconds) delay hoga - order processing simulate karne ke liye

---

### 🔹 TEST 11: Get All Orders

**Request Type:** GET  
**URL:** `http://localhost:5600/orders`

**Headers:**
```
Authorization: your_token_here
```

**Expected Response (200):**
```json
{
  "orders": [
    {
      "orderId": "ORD123456",
      "productName": "Men's Winter Sweater",
      "price": 700,
      "quantity": 1,
      "status": "Delivered",
      "orderDate": "2025-11-15",
      "deliveryDate": "2025-11-18"
    },
    {
      "orderId": "ORD123457",
      "productName": "Casual T-Shirt",
      "price": 299,
      "quantity": 2,
      "status": "In Transit",
      "orderDate": "2025-11-18",
      "estimatedDelivery": "2025-11-22"
    }
  ],
  "totalOrders": 2,
  "timestamp": "2025-12-02T10:40:00.000Z"
}
```

---

### 🔹 TEST 12: Track Order

**Request Type:** GET  
**URL:** `http://localhost:5600/order/ORD123456`

**Headers:**
```
Authorization: your_token_here
```

**Expected Response (200):**
```json
{
  "orderId": "ORD123456",
  "status": "In Transit",
  "productName": "Men's Winter Sweater",
  "price": 700,
  "quantity": 1,
  "orderDate": "2025-11-18",
  "estimatedDelivery": "2025-11-22",
  "trackingId": "TRK987654",
  "shippingAddress": {
    "name": "John Doe",
    "street": "123 Main Street",
    "city": "Mumbai",
    "state": "Maharashtra",
    "pincode": "400001"
  },
  "trackingHistory": [
    {"status": "Order Placed", "date": "2025-11-18T10:00:00Z", "location": "Mumbai"},
    {"status": "Packed", "date": "2025-11-18T14:00:00Z", "location": "Mumbai Warehouse"},
    {"status": "Shipped", "date": "2025-11-19T08:00:00Z", "location": "Mumbai Hub"},
    {"status": "In Transit", "date": "2025-11-20T06:00:00Z", "location": "En route to delivery"}
  ],
  "timestamp": "2025-12-02T10:41:00.000Z"
}
```

---

### 🔹 TEST 13: Search Products

**Request Type:** GET  
**URL:** `http://localhost:5600/search?q=sweater`

**Headers:**
```
Authorization: your_token_here
```

**Expected Response (200):**
```json
{
  "query": "sweater",
  "results": [
    {"id": 101, "name": "Men's Winter Sweater", "price": 700, "image": "sweater1.jpg", "rating": 4.5},
    {"id": 105, "name": "Hoodie", "price": 899, "image": "hoodie1.jpg", "rating": 4.8}
  ],
  "totalResults": 2,
  "timestamp": "2025-12-02T10:42:00.000Z"
}
```

---

### 🔹 TEST 14: Get User Profile

**Request Type:** GET  
**URL:** `http://localhost:5600/profile?name=Rahul&email=rahul@example.com`

**Headers:**
```
Authorization: your_token_here
```

**Expected Response (200):**
```json
{
  "userId": "a7b3c9d2e",
  "name": "Rahul",
  "email": "rahul@example.com",
  "phone": "+91-9876543210",
  "address": {
    "street": "123 Main Street",
    "city": "Mumbai",
    "state": "Maharashtra",
    "pincode": "400001"
  },
  "memberSince": "2024-01-15",
  "totalOrders": 12,
  "timestamp": "2025-12-02T10:43:00.000Z"
}
```

---

## Postman Environment Variables (Optional)

Agar token bar bar copy-paste nahi karna chahte:

### Step 1: Environment Banao
1. Postman mein "Environments" pe click karo
2. "+" button pe click karo
3. Name: "HTTP Stub Server"

### Step 2: Variables Add Karo
```
Variable: base_url
Initial Value: http://localhost:5600
Current Value: http://localhost:5600

Variable: token
Initial Value: (empty)
Current Value: (empty)
```

### Step 3: Register Request Mein Script Add Karo
"Tests" tab mein ye code dalo:
```javascript
// Token ko environment variable mein save karo
var response = pm.response.json();
pm.environment.set("token", response.token);
```

### Step 4: Baaki Requests Mein Use Karo
Headers mein:
```
Authorization: {{token}}
```

URL mein:
```
{{base_url}}/categories
```

---

## Common Errors & Solutions

### ❌ Error: "Cannot connect to server"
**Solution:** Server running hai? Check karo:
```bash
python server.py
```

### ❌ Error: "401 Unauthorized"
**Solution:** Token bhejo header mein:
```
Authorization: your_token_here
```

### ❌ Error: "404 Not Found"
**Solution:** URL check karo, typo toh nahi hai?

### ❌ Error: "500 Internal Server Error"
**Solution:** Server logs check karo terminal mein

---

## Tips for Demo

### 1. Order Mein Test Karo
Pehle register → login → categories → products → cart → order

### 2. Authentication Dikhaao
Bina token ke request bhejo, phir token ke saath - difference dikhaao

### 3. Delays Notice Karo
Order place karte waqt 3 second delay hoga - ye real API simulate karta hai

### 4. Logs Dikhaao
`requests.log` file open karke dikhaao ki saare requests log ho rahe hain

### 5. Dynamic Data Dikhaao
Multiple times same request bhejo - har baar unique ID aur timestamp milega

---

## Postman Collection Export (Optional)

Agar collection save karni hai:

1. Collection pe right-click karo
2. "Export" select karo
3. "Collection v2.1" select karo
4. Save karo

Phir kisi ko bhi share kar sakte ho!

---

## Summary

**Total Tests:** 14  
**Time Required:** 10-15 minutes  
**Prerequisites:** Server running hona chahiye

**Test Flow:**
```
Register → Login → Categories → Products → Cart → Order → Track
```

**All the best for testing! 🚀**
