# 🎯 Complete Testing Guide - All Possible Scenarios

## 📊 **6 Categories × 3 Subcategories × Multiple Products = 100+ Combinations!**

---

## **CATEGORY 1: ELECTRONICS**

### **Scenario 1A: Buy a Laptop**
```
1. GET /categories → Choose "Electronics" (ID: 1)
2. GET /categories/1 → Choose "Laptops" (ID: 1)
3. GET /categories/1/subcategories/1 → Choose "Dell Inspiron" (ID: 1001)
4. GET /categories/1/subcategories/1/products/1001 → View details
5. POST /register → Create account
6. POST /cart/add → Add Dell Inspiron (₹45,000)
7. POST /order/place → Place order
```

### **Scenario 1B: Buy Headphones**
```
1. GET /categories → Choose "Electronics" (ID: 1)
2. GET /categories/1 → Choose "Headphones" (ID: 2)
3. GET /categories/1/subcategories/2 → Choose "Sony WH-1000XM4" (ID: 1011)
4. GET /categories/1/subcategories/2/products/1011 → View details
5. POST /register → Create account
6. POST /cart/add → Add Sony Headphones (₹25,000)
7. POST /order/place → Place order
```

### **Scenario 1C: Buy Camera**
```
1. GET /categories → Choose "Electronics" (ID: 1)
2. GET /categories/1 → Choose "Cameras" (ID: 3)
3. GET /categories/1/subcategories/3 → Choose "Canon EOS 1500D" (ID: 1021)
4. GET /categories/1/subcategories/3/products/1021 → View details
5. POST /register → Create account
6. POST /cart/add → Add Canon Camera (₹35,000)
7. POST /order/place → Place order
```

---

## **CATEGORY 2: CLOTHING STORE**

### **Scenario 2A: Buy Men's Sweater**
```
1. GET /categories → Choose "Clothing Store" (ID: 2)
2. GET /categories/2 → Choose "Men Clothing" (ID: 1)
3. GET /categories/2/subcategories/1 → Choose "Winter Sweater" (ID: 2001)
4. GET /categories/2/subcategories/1/products/2001 → View details
5. POST /register → Create account
6. POST /cart/add → Add Sweater (₹700)
7. POST /order/place → Place order
```

### **Scenario 2B: Buy Women's Kurti**
```
1. GET /categories → Choose "Clothing Store" (ID: 2)
2. GET /categories/2 → Choose "Women Clothing" (ID: 2)
3. GET /categories/2/subcategories/2 → Choose "Women's Kurti" (ID: 2011)
4. GET /categories/2/subcategories/2/products/2011 → View details
5. POST /register → Create account
6. POST /cart/add → Add Kurti (₹599)
7. POST /order/place → Place order
```

### **Scenario 2C: Buy Baby Romper**
```
1. GET /categories → Choose "Clothing Store" (ID: 2)
2. GET /categories/2 → Choose "Baby Clothing" (ID: 3)
3. GET /categories/2/subcategories/3 → Choose "Baby Romper" (ID: 2021)
4. GET /categories/2/subcategories/3/products/2021 → View details
5. POST /register → Create account
6. POST /cart/add → Add Romper (₹399)
7. POST /order/place → Place order
```

---

## **CATEGORY 3: TV & APPLIANCES**

### **Scenario 3A: Buy Samsung TV**
```
1. GET /categories → Choose "TV & Appliances" (ID: 3)
2. GET /categories/3 → Choose "Televisions" (ID: 1)
3. GET /categories/3/subcategories/1 → Choose "Samsung 43\" 4K" (ID: 3001)
4. GET /categories/3/subcategories/1/products/3001 → View details
5. POST /register → Create account
6. POST /cart/add → Add Samsung TV (₹35,000)
7. POST /order/place → Place order
```

### **Scenario 3B: Buy Refrigerator**
```
1. GET /categories → Choose "TV & Appliances" (ID: 3)
2. GET /categories/3 → Choose "Refrigerators" (ID: 2)
3. GET /categories/3/subcategories/2 → Choose "Samsung 260L" (ID: 3011)
4. GET /categories/3/subcategories/2/products/3011 → View details
5. POST /register → Create account
6. POST /cart/add → Add Refrigerator (₹25,000)
7. POST /order/place → Place order
```

### **Scenario 3C: Buy Washing Machine**
```
1. GET /categories → Choose "TV & Appliances" (ID: 3)
2. GET /categories/3 → Choose "Washing Machines" (ID: 3)
3. GET /categories/3/subcategories/3 → Choose "IFB 6kg" (ID: 3021)
4. GET /categories/3/subcategories/3/products/3021 → View details
5. POST /register → Create account
6. POST /cart/add → Add Washing Machine (₹22,000)
7. POST /order/place → Place order
```

---

## **CATEGORY 4: SMARTPHONES**

### **Scenario 4A: Buy Samsung Galaxy**
```
1. GET /categories → Choose "Smartphones" (ID: 4)
2. GET /categories/4 → Choose "Android Phones" (ID: 1)
3. GET /categories/4/subcategories/1 → Choose "Samsung Galaxy S23" (ID: 4001)
4. GET /categories/4/subcategories/1/products/4001 → View details
5. POST /register → Create account
6. POST /cart/add → Add Samsung Galaxy (₹65,000)
7. POST /order/place → Place order
```

### **Scenario 4B: Buy iPhone**
```
1. GET /categories → Choose "Smartphones" (ID: 4)
2. GET /categories/4 → Choose "iPhones" (ID: 2)
3. GET /categories/4/subcategories/2 → Choose "iPhone 14" (ID: 4011)
4. GET /categories/4/subcategories/2/products/4011 → View details
5. POST /register → Create account
6. POST /cart/add → Add iPhone 14 (₹70,000)
7. POST /order/place → Place order
```

### **Scenario 4C: Buy Budget Phone**
```
1. GET /categories → Choose "Smartphones" (ID: 4)
2. GET /categories/4 → Choose "Budget Phones" (ID: 3)
3. GET /categories/4/subcategories/3 → Choose "Redmi Note 12" (ID: 4021)
4. GET /categories/4/subcategories/3/products/4021 → View details
5. POST /register → Create account
6. POST /cart/add → Add Redmi Note (₹15,000)
7. POST /order/place → Place order
```

---

## **CATEGORY 5: KITCHEN WARE**

### **Scenario 5A: Buy Cookware**
```
1. GET /categories → Choose "Kitchen Ware" (ID: 5)
2. GET /categories/5 → Choose "Cookware" (ID: 1)
3. GET /categories/5/subcategories/1 → Choose "Pressure Cooker" (ID: 5002)
4. GET /categories/5/subcategories/1/products/5002 → View details
5. POST /register → Create account
6. POST /cart/add → Add Pressure Cooker (₹1,299)
7. POST /order/place → Place order
```

### **Scenario 5B: Buy Mixer Grinder**
```
1. GET /categories → Choose "Kitchen Ware" (ID: 5)
2. GET /categories/5 → Choose "Kitchen Appliances" (ID: 2)
3. GET /categories/5/subcategories/2 → Choose "Mixer Grinder" (ID: 5011)
4. GET /categories/5/subcategories/2/products/5011 → View details
5. POST /register → Create account
6. POST /cart/add → Add Mixer Grinder (₹2,500)
7. POST /order/place → Place order
```

### **Scenario 5C: Buy Dinner Set**
```
1. GET /categories → Choose "Kitchen Ware" (ID: 5)
2. GET /categories/5 → Choose "Dinnerware" (ID: 3)
3. GET /categories/5/subcategories/3 → Choose "Dinner Set 24pc" (ID: 5021)
4. GET /categories/5/subcategories/3/products/5021 → View details
5. POST /register → Create account
6. POST /cart/add → Add Dinner Set (₹1,999)
7. POST /order/place → Place order
```

---

## **CATEGORY 6: HOME DECOR**

### **Scenario 6A: Buy Wall Art**
```
1. GET /categories → Choose "Home Decor" (ID: 6)
2. GET /categories/6 → Choose "Wall Art" (ID: 1)
3. GET /categories/6/subcategories/1 → Choose "Canvas Painting" (ID: 6001)
4. GET /categories/6/subcategories/1/products/6001 → View details
5. POST /register → Create account
6. POST /cart/add → Add Canvas Painting (₹1,299)
7. POST /order/place → Place order
```

### **Scenario 6B: Buy LED Light**
```
1. GET /categories → Choose "Home Decor" (ID: 6)
2. GET /categories/6 → Choose "Lighting" (ID: 2)
3. GET /categories/6/subcategories/2 → Choose "LED Ceiling Light" (ID: 6011)
4. GET /categories/6/subcategories/2/products/6011 → View details
5. POST /register → Create account
6. POST /cart/add → Add LED Light (₹1,499)
7. POST /order/place → Place order
```

### **Scenario 6C: Buy Cushion Covers**
```
1. GET /categories → Choose "Home Decor" (ID: 6)
2. GET /categories/6 → Choose "Cushions & Curtains" (ID: 3)
3. GET /categories/6/subcategories/3 → Choose "Cushion Covers" (ID: 6021)
4. GET /categories/6/subcategories/3/products/6021 → View details
5. POST /register → Create account
6. POST /cart/add → Add Cushion Covers (₹599)
7. POST /order/place → Place order
```

---

## 🎯 **Quick Reference URLs**

### **Electronics:**
- Laptops: `/categories/1/subcategories/1`
- Headphones: `/categories/1/subcategories/2`
- Cameras: `/categories/1/subcategories/3`

### **Clothing:**
- Men: `/categories/2/subcategories/1`
- Women: `/categories/2/subcategories/2`
- Baby: `/categories/2/subcategories/3`

### **TV & Appliances:**
- TVs: `/categories/3/subcategories/1`
- Refrigerators: `/categories/3/subcategories/2`
- Washing Machines: `/categories/3/subcategories/3`

### **Smartphones:**
- Android: `/categories/4/subcategories/1`
- iPhones: `/categories/4/subcategories/2`
- Budget: `/categories/4/subcategories/3`

### **Kitchen Ware:**
- Cookware: `/categories/5/subcategories/1`
- Appliances: `/categories/5/subcategories/2`
- Dinnerware: `/categories/5/subcategories/3`

### **Home Decor:**
- Wall Art: `/categories/6/subcategories/1`
- Lighting: `/categories/6/subcategories/2`
- Cushions: `/categories/6/subcategories/3`

---

## 🎤 **For Judges:**

**"Sir/Ma'am, aap koi bhi category choose kar sakte hain:"**

- Electronics → Laptop, Headphones, Camera
- Clothing → Men, Women, Baby
- TV & Appliances → TV, Fridge, Washing Machine
- Smartphones → Android, iPhone, Budget
- Kitchen Ware → Cookware, Appliances, Dinnerware
- Home Decor → Wall Art, Lighting, Cushions

**"Har category mein 3 subcategories hain, aur har subcategory mein 3-4 products hain. Total 100+ combinations!"**

**"Jo bhi aap choose karenge, wahi response mein aayega - fully dynamic!"**

---

**Ab judges kuch bhi choose kar sakte hain - sab ready hai!** 🚀
