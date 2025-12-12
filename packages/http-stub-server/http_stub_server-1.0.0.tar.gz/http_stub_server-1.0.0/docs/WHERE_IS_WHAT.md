# 📍 WHERE IS WHAT - Quick Reference

---

## 🗂️ **File Locations:**

| File | Purpose | Contains |
|------|---------|----------|
| `config.json` | Static endpoints | Register, Login, Cart, Orders |
| `config.COMMENTED.json` | Same as above with comments | Detailed explanations |
| `data.js` | Product database | All categories, products |
| `server.js` | Server logic | Route handlers, authentication |
| `JSON_RESPONSE_GUIDE.md` | Complete guide | All response examples |
| `WHERE_IS_WHAT.md` | This file | Quick reference |

---

## 📋 **JSON Responses Location:**

### **Static Responses → `config.json`**

✅ **Authentication:**
- `/register` - Line 8-24
- `/login` - Line 26-40

✅ **Errors:**
- `/categories/unauthorized` - Line 42-52
- `/cart/add/unauthorized` - Line 70-80
- `/order/place/unauthorized` - Line 120-130

✅ **Shopping:**
- `/cart/add` - Line 82-105
- `/cart` - Line 107-130
- `/order/place` - Line 132-165 (3 sec delay!)

✅ **Other:**
- `/orders` - Line 167-190
- `/order/:orderId` - Line 192-220
- `/search` - Line 222-235
- `/profile` - Line 237-255

---

### **Dynamic Responses → `data.js` + `server.js`**

✅ **Categories:**
- `/categories/:id` - Generated from `data.js`
- Example: `/categories/1` → Electronics

✅ **Products:**
- `/categories/:id/subcategories/:id` - Generated from `data.js`
- Example: `/categories/1/subcategories/1` → Laptops

✅ **Product Details:**
- `/categories/:id/subcategories/:id/products/:id` - Generated from `data.js`
- Example: `/categories/1/subcategories/1/products/1001` → Dell Laptop

---

## 🎯 **Quick Access:**

### **Want to see Register response?**
→ Open `config.json` → Line 8-24
→ Or open `config.COMMENTED.json` → Line 15-35 (with comments)

### **Want to see Product list?**
→ Open `data.js` → Find category → Find subcategory → See products array

### **Want to understand how it works?**
→ Open `JSON_RESPONSE_GUIDE.md` → Complete explanations with examples

---

## 📊 **Data Structure:**

```
config.json
├── port: 5600
└── endpoints[]
    ├── /register (POST)
    ├── /login (POST)
    ├── /cart/add (POST)
    ├── /order/place (POST)
    └── ... (13 total)

data.js
├── Category 1: Electronics
│   ├── Subcategory 1: Laptops (4 products)
│   ├── Subcategory 2: Headphones (3 products)
│   └── Subcategory 3: Cameras (3 products)
├── Category 2: Clothing Store
│   ├── Subcategory 1: Men (4 products)
│   ├── Subcategory 2: Women (4 products)
│   └── Subcategory 3: Baby (3 products)
├── Category 3: TV & Appliances
├── Category 4: Smartphones
├── Category 5: Kitchen Ware
└── Category 6: Home Decor
```

---

## 🔍 **How to Find Specific Response:**

### **Example 1: "Where is Register response?"**
1. Open `config.json`
2. Search for `"path": "/register"`
3. Look at `"response"` object
4. That's your JSON response!

### **Example 2: "Where are iPhone products?"**
1. Open `data.js`
2. Search for `"4"` (Smartphones category)
3. Find `"2"` (iPhones subcategory)
4. Look at `products` array
5. That's your iPhone list!

### **Example 3: "What does Order response look like?"**
1. Open `JSON_RESPONSE_GUIDE.md`
2. Search for "POST /order/place"
3. See complete example with explanations

---

## 💡 **Pro Tips:**

✅ **For Presentation:**
- Use `config.COMMENTED.json` to explain structure
- Use `JSON_RESPONSE_GUIDE.md` for detailed examples

✅ **For Development:**
- Edit `config.json` for static endpoints
- Edit `data.js` for products
- Server auto-reloads!

✅ **For Testing:**
- Use Postman with URLs from `ALL_SCENARIOS.md`
- Check responses match `JSON_RESPONSE_GUIDE.md`

---

## 📝 **Summary:**

| What You Want | Where to Look |
|---------------|---------------|
| Register/Login response | `config.json` lines 8-40 |
| Cart/Order response | `config.json` lines 82-165 |
| Product data | `data.js` |
| Complete examples | `JSON_RESPONSE_GUIDE.md` |
| Commented version | `config.COMMENTED.json` |
| Quick reference | `WHERE_IS_WHAT.md` (this file) |

---

**Sab kuch organized hai! Koi bhi response 2 minutes mein mil jayega!** 📋✅
