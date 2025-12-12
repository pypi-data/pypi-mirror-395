# 📋 JSON Response Guide - Where to Find What

---

## 🗂️ **File Structure:**

```
project/
├── config.json          ← Static endpoints (register, login, cart, orders)
├── data.js              ← Dynamic data (categories, products)
├── server.js            ← Server logic (generates responses)
└── JSON_RESPONSE_GUIDE.md  ← This file
```

---

## 📄 **File 1: `config.json`**

### **Purpose:** 
Static endpoints jo **config se directly** response dete hain.

### **Contains:**
1. ✅ Register endpoint response
2. ✅ Login endpoint response
3. ✅ Unauthorized error responses
4. ✅ Cart endpoints
5. ✅ Order placement
6. ✅ Search, Profile, etc.

### **Example Structure:**
```json
{
  "port": 5600,              // ← Server port number
  "endpoints": [             // ← Array of all endpoints
    {
      "path": "/register",   // ← URL path
      "method": "POST",      // ← HTTP method
      "status": 201,         // ← Response status code
      "delay": 1000,         // ← Artificial delay (ms)
      "response": {          // ← JSON response object
        "success": true,
        "message": "Account created successfully!",
        "user": {
          "id": "{{randomId}}",      // ← Dynamic: Random ID
          "name": "{{body.name}}",   // ← Dynamic: From POST body
          "email": "{{body.email}}"  // ← Dynamic: From POST body
        },
        "token": "{{randomId}}",     // ← Dynamic: Random token
        "timestamp": "{{timestamp}}" // ← Dynamic: Current time
      }
    }
  ]
}
```

### **Key Endpoints in config.json:**

#### **1. POST /register**
```json
{
  "success": true,
  "message": "Account created successfully!",
  "user": {
    "id": "k3al6uifg",           // ← Random generated
    "name": "Rahul Kumar",        // ← From your POST body
    "email": "rahul@example.com", // ← From your POST body
    "phone": "9876543210"         // ← From your POST body
  },
  "token": "xyz789abc",           // ← Random generated
  "timestamp": "2025-11-25T..."   // ← Current timestamp
}
```

#### **2. POST /login**
```json
{
  "success": true,
  "message": "Login successful!",
  "user": {
    "id": "abc123",
    "email": "rahul@example.com",
    "name": "Rahul Kumar"
  },
  "token": "xyz789",
  "timestamp": "2025-11-25T..."
}
```

#### **3. GET /categories/unauthorized** (401 Error)
```json
{
  "success": false,
  "error": "Unauthorized",
  "message": "Please create an account or login first to browse products!",
  "redirectTo": "/register",
  "timestamp": "2025-11-25T..."
}
```

#### **4. POST /cart/add**
```json
{
  "success": true,
  "message": "Item added to cart successfully!",
  "cartItem": {
    "productId": "101",              // ← From your POST body
    "productName": "Winter Sweater", // ← From your POST body
    "price": "700",                  // ← From your POST body
    "quantity": "1",                 // ← From your POST body
    "size": "L",                     // ← From your POST body
    "color": "Black"                 // ← From your POST body
  },
  "cartTotal": {
    "items": 1,
    "subtotal": "700",
    "tax": 70,
    "total": 770
  },
  "timestamp": "2025-11-25T..."
}
```

#### **5. POST /order/place** (3 second delay)
```json
{
  "success": true,
  "message": "Your order has been placed successfully!",
  "orderId": "ORDk3al6uifg",        // ← Random generated
  "orderDetails": {
    "customerName": "Rahul Kumar",   // ← From your POST body
    "email": "rahul@example.com",    // ← From your POST body
    "phone": "9876543210",           // ← From your POST body
    "address": {
      "street": "123 Main Street",   // ← From your POST body
      "city": "Mumbai",              // ← From your POST body
      "state": "Maharashtra",        // ← From your POST body
      "pincode": "400001"            // ← From your POST body
    },
    "items": [...],                  // ← From your POST body
    "paymentMethod": "Credit Card",  // ← From your POST body
    "totalAmount": "770"             // ← From your POST body
  },
  "estimatedDelivery": "3-5 business days",
  "trackingId": "TRKxyz789",         // ← Random generated
  "orderPlacedAt": "2025-11-25T..."  // ← Current timestamp
}
```

---

## 📄 **File 2: `data.js`**

### **Purpose:** 
Dynamic product database jo **category/subcategory ID** ke basis pe response generate karta hai.

### **Contains:**
1. ✅ 6 Categories (Electronics, Clothing, TV, Smartphones, Kitchen, Home Decor)
2. ✅ 18 Subcategories (3 per category)
3. ✅ 60+ Products (3-4 per subcategory)

### **Structure:**
```javascript
const categoryData = {
  "1": {                    // ← Category ID
    name: "Electronics",    // ← Category name
    subcategories: {
      "1": {                // ← Subcategory ID
        name: "Laptops",    // ← Subcategory name
        products: [         // ← Array of products
          {
            id: 1001,
            name: "Dell Inspiron 15",
            price: 45000,
            rating: 4.5,
            inStock: true
          }
        ]
      }
    }
  }
}
```

### **How Responses are Generated:**

#### **1. GET /categories/1** (Electronics)
**Server reads:** `data.js` → `categoryData["1"]`

**Response:**
```json
{
  "categoryId": "1",
  "categoryName": "Electronics",
  "subcategories": [
    {"id": 1, "name": "Laptops", "itemCount": 4},
    {"id": 2, "name": "Headphones", "itemCount": 3},
    {"id": 3, "name": "Cameras", "itemCount": 3}
  ],
  "timestamp": "2025-11-25T..."
}
```

#### **2. GET /categories/1/subcategories/1** (Laptops)
**Server reads:** `data.js` → `categoryData["1"].subcategories["1"]`

**Response:**
```json
{
  "categoryId": "1",
  "subcategoryId": "1",
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
  ],
  "totalProducts": 4,
  "timestamp": "2025-11-25T..."
}
```

#### **3. GET /categories/1/subcategories/1/products/1001** (Dell Laptop)
**Server reads:** `data.js` → Find product with `id: 1001`

**Response:**
```json
{
  "productId": "1001",
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
  "timestamp": "2025-11-25T..."
}
```

---

## 🎯 **All 6 Categories in data.js:**

### **Category 1: Electronics (ID: 1)**
- Subcategory 1: Laptops (4 products)
- Subcategory 2: Headphones (3 products)
- Subcategory 3: Cameras (3 products)

### **Category 2: Clothing Store (ID: 2)**
- Subcategory 1: Men Clothing (4 products)
- Subcategory 2: Women Clothing (4 products)
- Subcategory 3: Baby Clothing (3 products)

### **Category 3: TV & Appliances (ID: 3)**
- Subcategory 1: Televisions (3 products)
- Subcategory 2: Refrigerators (3 products)
- Subcategory 3: Washing Machines (3 products)

### **Category 4: Smartphones (ID: 4)**
- Subcategory 1: Android Phones (4 products)
- Subcategory 2: iPhones (3 products)
- Subcategory 3: Budget Phones (3 products)

### **Category 5: Kitchen Ware (ID: 5)**
- Subcategory 1: Cookware (3 products)
- Subcategory 2: Kitchen Appliances (3 products)
- Subcategory 3: Dinnerware (3 products)

### **Category 6: Home Decor (ID: 6)**
- Subcategory 1: Wall Art (3 products)
- Subcategory 2: Lighting (3 products)
- Subcategory 3: Cushions & Curtains (3 products)

---

## 🔧 **Dynamic Template Variables:**

### **Used in config.json:**

| Variable | Description | Example |
|----------|-------------|---------|
| `{{timestamp}}` | Current ISO timestamp | `2025-11-25T15:30:00.000Z` |
| `{{randomId}}` | Random 9-char ID | `k3al6uifg` |
| `{{query.name}}` | Query parameter | `?name=Ram` → `Ram` |
| `{{params.id}}` | Path parameter | `/users/123` → `123` |
| `{{body.name}}` | POST body field | `{"name": "Rahul"}` → `Rahul` |
| `{{body.email}}` | POST body field | `{"email": "a@b.com"}` → `a@b.com` |

---

## 📊 **Quick Reference:**

### **Static Responses (config.json):**
- ✅ `/register` - Account creation
- ✅ `/login` - User login
- ✅ `/cart/add` - Add to cart
- ✅ `/order/place` - Place order
- ✅ `/cart` - View cart
- ✅ `/orders` - Order history
- ✅ `/search` - Search products
- ✅ `/profile` - User profile

### **Dynamic Responses (data.js + server.js):**
- ✅ `/categories/:id` - Category details
- ✅ `/categories/:id/subcategories/:id` - Products list
- ✅ `/categories/:id/subcategories/:id/products/:id` - Product details

---

## 🎯 **How to Modify Responses:**

### **To change static responses:**
1. Open `config.json`
2. Find the endpoint
3. Edit the `response` object
4. Save file
5. Server auto-reloads!

### **To add new products:**
1. Open `data.js`
2. Find the category
3. Find the subcategory
4. Add product to `products` array
5. Save file
6. Restart server

---

## 📝 **Example: Adding a New Product**

**In data.js:**
```javascript
"1": { // Electronics
  subcategories: {
    "1": { // Laptops
      products: [
        // Add this new product:
        {
          id: 1005,
          name: "MacBook Pro",
          price: 120000,
          rating: 4.9,
          inStock: true,
          specs: "M2 Chip, 16GB RAM, 512GB SSD"
        }
      ]
    }
  }
}
```

**Response will be:**
```
GET /categories/1/subcategories/1
```
```json
{
  "products": [
    {...},
    {
      "id": 1005,
      "name": "MacBook Pro",
      "price": 120000,
      "rating": 4.9,
      "inStock": true,
      "specs": "M2 Chip, 16GB RAM, 512GB SSD"
    }
  ]
}
```

---

**Yeh complete guide hai! Sab kuch detail mein explain kiya hai!** 📋✅
