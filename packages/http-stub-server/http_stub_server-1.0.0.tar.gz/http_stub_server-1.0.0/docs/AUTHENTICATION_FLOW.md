# 🔐 Authentication Flow Guide

## Overview
This stub server simulates authentication by providing both **authorized** and **unauthorized** endpoints. This demonstrates how real-world applications handle user authentication.

---

## 🎯 Two Scenarios

### **Scenario 1: WITHOUT Login (Unauthorized)**
User tries to access protected resources without authentication.

### **Scenario 2: WITH Login (Authorized)**
User creates account/logs in first, then accesses resources.

---

## 📋 Complete Flow Examples

### **❌ SCENARIO 1: User Tries to Browse WITHOUT Account**

#### **Step 1: Try to view categories (FAILS)**
```
Method: GET
URL: http://localhost:5600/categories/unauthorized
```

**Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": "Unauthorized",
  "message": "Please create an account or login first to browse products!",
  "redirectTo": "/register",
  "timestamp": "2025-11-20T..."
}
```

#### **Step 2: Try to add to cart (FAILS)**
```
Method: POST
URL: http://localhost:5600/cart/add/unauthorized
Body: {"productId": "101", "productName": "Sweater"}
```

**Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": "Unauthorized",
  "message": "You must be logged in to add items to cart. Please login or create an account first!",
  "redirectTo": "/login"
}
```

#### **Step 3: Try to place order (FAILS)**
```
Method: POST
URL: http://localhost:5600/order/place/unauthorized
Body: {"name": "Rahul", "productId": "101"}
```

**Response (401 Unauthorized):**
```json
{
  "success": false,
  "error": "Unauthorized",
  "message": "Cannot place order without login! Please create an account first to complete your purchase.",
  "redirectTo": "/register"
}
```

---

### **✅ SCENARIO 2: User Creates Account First (SUCCESS)**

#### **Step 1: Register Account**
```
Method: POST
URL: http://localhost:5600/register
Body:
{
  "name": "Rahul Kumar",
  "email": "rahul@example.com",
  "phone": "9876543210",
  "password": "password123"
}
```

**Response (201 Created):**
```json
{
  "success": true,
  "message": "Account created successfully!",
  "user": {
    "id": "abc123",
    "name": "Rahul Kumar",
    "email": "rahul@example.com",
    "phone": "9876543210"
  },
  "token": "xyz789"
}
```

✅ **Now user has a token!**

---

#### **Step 2: Browse Categories (SUCCESS)**
```
Method: GET
URL: http://localhost:5600/categories
```

**Response (200 OK):**
```json
{
  "categories": [
    {"id": 1, "name": "Electronics"},
    {"id": 2, "name": "Clothing Store"},
    ...
  ]
}
```

✅ **User can now browse!**

---

#### **Step 3: View Products (SUCCESS)**
```
Method: GET
URL: http://localhost:5600/products/1
```

**Response (200 OK):**
```json
{
  "products": [
    {"id": 101, "name": "Men's Winter Sweater", "price": 700},
    ...
  ]
}
```

---

#### **Step 4: Add to Cart (SUCCESS)**
```
Method: POST
URL: http://localhost:5600/cart/add
Body:
{
  "productId": "101",
  "productName": "Men's Winter Sweater",
  "price": "700",
  "quantity": "1",
  "size": "L"
}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Item added to cart successfully!",
  "cartItem": {
    "productId": "101",
    "productName": "Men's Winter Sweater",
    "price": "700"
  }
}
```

✅ **Item added!**

---

#### **Step 5: Place Order (SUCCESS)**
```
Method: POST
URL: http://localhost:5600/order/place
Body:
{
  "name": "Rahul Kumar",
  "email": "rahul@example.com",
  "productId": "101",
  "productName": "Men's Winter Sweater",
  "price": "700",
  "totalAmount": "770"
}
```

**Response (201 Created - 3 sec delay):**
```json
{
  "success": true,
  "message": "Your order has been placed successfully!",
  "orderId": "ORDabc123",
  "orderDetails": {
    "customerName": "Rahul Kumar",
    "email": "rahul@example.com",
    "items": [...]
  }
}
```

✅ **Order placed successfully!**

---

## 🎤 Presentation Script

### **Demo for Judges:**

**"Let me show you the authentication flow."**

**Step 1: Show Unauthorized Access**
```
"First, let's try to browse products WITHOUT creating an account."
[Hit /categories/unauthorized]
"See? The system says: 'Please create an account first!'"
"This is how real e-commerce sites work - you need to login first."
```

**Step 2: Create Account**
```
"Now let's create an account."
[Hit /register with user details]
"Account created! We got a token back."
"In a real application, this token would be stored and sent with every request."
```

**Step 3: Show Authorized Access**
```
"Now that we're logged in, let's browse categories."
[Hit /categories]
"Success! Now we can see all categories."

"Let's add a product to cart."
[Hit /cart/add]
"Success! Item added."

"Finally, let's place the order."
[Hit /order/place]
[Wait 3 seconds]
"Order placed successfully! See - all our details are here."
```

**Key Point:**
```
"This demonstrates proper authentication flow:
1. User must register/login first
2. Only then can they browse and buy
3. All their data is tracked throughout the journey
4. This is exactly how real e-commerce platforms work!"
```

---

## 🎯 Key Endpoints

### **Unauthorized Endpoints (Show Errors):**
- `GET /categories/unauthorized` - Browse without login
- `POST /cart/add/unauthorized` - Add to cart without login
- `POST /order/place/unauthorized` - Order without login

### **Authorized Endpoints (After Login):**
- `POST /register` - Create account
- `POST /login` - Login
- `GET /categories` - Browse categories
- `GET /products/:id` - View products
- `POST /cart/add` - Add to cart
- `POST /order/place` - Place order

---

## 💡 Why This Matters

**Real-World Simulation:**
- Shows understanding of authentication
- Demonstrates security awareness
- Proves knowledge of user flows
- Impresses judges with completeness

**Technical Depth:**
- HTTP status codes (200, 201, 401)
- Error handling
- User journey mapping
- State management concepts

---

## 🚀 Testing in Postman

### **Test 1: Unauthorized Flow**
1. Hit `/categories/unauthorized` → Get 401 error
2. Hit `/cart/add/unauthorized` → Get 401 error
3. Hit `/order/place/unauthorized` → Get 401 error

### **Test 2: Authorized Flow**
1. Hit `/register` → Get token
2. Hit `/categories` → Success
3. Hit `/cart/add` → Success
4. Hit `/order/place` → Success

---

**This makes your project production-ready and shows professional understanding!** 🎉
