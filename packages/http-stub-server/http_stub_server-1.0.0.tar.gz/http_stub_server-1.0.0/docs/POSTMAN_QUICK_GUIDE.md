# 🚀 Postman Quick Guide - Step by Step

## Your Token: `9xhqbtqnm`

---

## 📋 **How to Add Authorization Header**

### **Method 1: Headers Tab (Recommended)**

**For Every Request:**

1. Click on **"Headers"** tab (next to Params)
2. Add new header:
   - **Key:** `Authorization`
   - **Value:** `9xhqbtqnm`
3. Click **Send**

---

### **Method 2: Authorization Tab (Alternative)**

1. Click on **"Authorization"** tab
2. **Type:** Select "API Key"
3. **Key:** `Authorization`
4. **Value:** `9xhqbtqnm`
5. **Add to:** Header
6. Click **Send**

---

## 🎯 **Complete Request Examples**

### **1. Get All Categories**

```
Method: GET
URL: http://localhost:5600/categories

Headers:
Authorization: 9xhqbtqnm
```

**Postman Setup:**
- Method dropdown: `GET`
- URL bar: `http://localhost:5600/categories`
- Headers tab:
  - Key: `Authorization`
  - Value: `9xhqbtqnm`
- Click **Send**

---

### **2. Get Category Details (Electronics)**

```
Method: GET
URL: http://localhost:5600/categories/1

Headers:
Authorization: 9xhqbtqnm
```

**Postman Setup:**
- Method: `GET`
- URL: `http://localhost:5600/categories/1`
- Headers:
  - Key: `Authorization`
  - Value: `9xhqbtqnm`
- Click **Send**

---

### **3. Get Subcategory Products (Laptops)**

```
Method: GET
URL: http://localhost:5600/categories/1/subcategories/1

Headers:
Authorization: 9xhqbtqnm
```

**Postman Setup:**
- Method: `GET`
- URL: `http://localhost:5600/categories/1/subcategories/1`
- Headers:
  - Key: `Authorization`
  - Value: `9xhqbtqnm`
- Click **Send**

---

### **4. Get Product Details (Dell Inspiron)**

```
Method: GET
URL: http://localhost:5600/categories/1/subcategories/1/products/1001

Headers:
Authorization: 9xhqbtqnm
```

**Postman Setup:**
- Method: `GET`
- URL: `http://localhost:5600/categories/1/subcategories/1/products/1001`
- Headers:
  - Key: `Authorization`
  - Value: `9xhqbtqnm`
- Click **Send**

---

### **5. Add to Cart**

```
Method: POST
URL: http://localhost:5600/cart/add

Headers:
Authorization: 9xhqbtqnm
Content-Type: application/json

Body (raw JSON):
{
  "productId": 1001,
  "productName": "Dell Inspiron 15",
  "price": 45000,
  "quantity": 1,
  "size": "15 inch",
  "color": "Silver"
}
```

**Postman Setup:**
- Method: `POST`
- URL: `http://localhost:5600/cart/add`
- Headers:
  - Key: `Authorization`, Value: `9xhqbtqnm`
  - Key: `Content-Type`, Value: `application/json`
- Body tab:
  - Select: `raw`
  - Dropdown: `JSON`
  - Paste JSON above
- Click **Send**

---

### **6. View Cart**

```
Method: GET
URL: http://localhost:5600/cart

Headers:
Authorization: 9xhqbtqnm
```

**Postman Setup:**
- Method: `GET`
- URL: `http://localhost:5600/cart`
- Headers:
  - Key: `Authorization`
  - Value: `9xhqbtqnm`
- Click **Send**

---

### **7. Place Order**

```
Method: POST
URL: http://localhost:5600/order/place

Headers:
Authorization: 9xhqbtqnm
Content-Type: application/json

Body (raw JSON):
{
  "name": "Soumya Sagar",
  "email": "soumya@example.com",
  "phone": "9876543210",
  "address": "123 Main Street",
  "city": "Mumbai",
  "state": "Maharashtra",
  "pincode": "400001",
  "productId": 1001,
  "productName": "Dell Inspiron 15",
  "price": 45000,
  "quantity": 1,
  "size": "15 inch",
  "paymentMethod": "COD",
  "totalAmount": 45000
}
```

**Postman Setup:**
- Method: `POST`
- URL: `http://localhost:5600/order/place`
- Headers:
  - Key: `Authorization`, Value: `9xhqbtqnm`
  - Key: `Content-Type`, Value: `application/json`
- Body tab:
  - Select: `raw`
  - Dropdown: `JSON`
  - Paste JSON above
- Click **Send**
- **Wait 3 seconds** (order processing)

---

### **8. View Orders**

```
Method: GET
URL: http://localhost:5600/orders

Headers:
Authorization: 9xhqbtqnm
```

**Postman Setup:**
- Method: `GET`
- URL: `http://localhost:5600/orders`
- Headers:
  - Key: `Authorization`
  - Value: `9xhqbtqnm`
- Click **Send**

---

### **9. Track Order**

```
Method: GET
URL: http://localhost:5600/order/ORD123456

Headers:
Authorization: 9xhqbtqnm
```

**Postman Setup:**
- Method: `GET`
- URL: `http://localhost:5600/order/ORD123456`
- Headers:
  - Key: `Authorization`
  - Value: `9xhqbtqnm`
- Click **Send**

---

### **10. Search Products**

```
Method: GET
URL: http://localhost:5600/search?q=laptop

Headers:
Authorization: 9xhqbtqnm
```

**Postman Setup:**
- Method: `GET`
- URL: `http://localhost:5600/search?q=laptop`
- Headers:
  - Key: `Authorization`
  - Value: `9xhqbtqnm`
- Click **Send**

---

## 🎯 **Quick Copy-Paste URLs**

**Your Token:** `9xhqbtqnm`

**GET Requests (Add Authorization header):**
```
http://localhost:5600/categories
http://localhost:5600/categories/1
http://localhost:5600/categories/1/subcategories/1
http://localhost:5600/categories/1/subcategories/1/products/1001
http://localhost:5600/cart
http://localhost:5600/orders
http://localhost:5600/order/ORD123456
http://localhost:5600/search?q=laptop
```

**POST Requests (Add Authorization + Content-Type headers):**
```
http://localhost:5600/cart/add
http://localhost:5600/order/place
```

---

## 📝 **Common Body Templates**

### **Add to Cart Body:**
```json
{
  "productId": 1001,
  "productName": "Dell Inspiron 15",
  "price": 45000,
  "quantity": 1,
  "size": "15 inch",
  "color": "Silver"
}
```

### **Place Order Body:**
```json
{
  "name": "Your Name",
  "email": "your@email.com",
  "phone": "9876543210",
  "address": "123 Main Street",
  "city": "Mumbai",
  "state": "Maharashtra",
  "pincode": "400001",
  "productId": 1001,
  "productName": "Dell Inspiron 15",
  "price": 45000,
  "quantity": 1,
  "size": "15 inch",
  "paymentMethod": "COD",
  "totalAmount": 45000
}
```

---

## ⚡ **Pro Tips**

### **1. Save Token as Variable**
- Click on "Environments" (top right)
- Create new environment: "HTTP Stub Server"
- Add variable:
  - Name: `token`
  - Value: `9xhqbtqnm`
- Use in headers: `{{token}}`

### **2. Create Collection**
- Click "Collections" → "New Collection"
- Name: "E-commerce API"
- Add all requests to collection
- Save for reuse

### **3. Check Response**
- Status code should be 200 or 201
- If 401: Token missing or wrong
- If 404: URL wrong
- If 500: Server error

### **4. Demo Sequence**
1. Categories (30s)
2. Browse Products (1m)
3. Add to Cart (1m)
4. Place Order (3m - includes 3s delay)
5. Track Order (30s)

---

## 🚨 **Common Errors**

### **401 Unauthorized**
**Problem:** Token missing
**Solution:** Add `Authorization: 9xhqbtqnm` in Headers

### **404 Not Found**
**Problem:** Wrong URL
**Solution:** Check URL spelling and port (5600)

### **Connection Refused**
**Problem:** Server not running
**Solution:** Run `python server.py`

### **415 Unsupported Media Type**
**Problem:** Content-Type missing for POST
**Solution:** Add `Content-Type: application/json` header

---

## ✅ **Checklist Before Demo**

- [ ] Server running on port 5600
- [ ] Token copied: `9xhqbtqnm`
- [ ] Postman open
- [ ] All requests tested
- [ ] Headers added correctly
- [ ] Body JSON formatted
- [ ] Demo sequence practiced

---

**Ab Postman mein test karo! Har request mein Authorization header yaad rakhna!** 🚀
