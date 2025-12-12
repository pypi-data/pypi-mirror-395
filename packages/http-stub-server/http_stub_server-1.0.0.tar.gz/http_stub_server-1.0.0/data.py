# ============================================
# E-COMMERCE PRODUCT DATA
# ============================================
# Complete product catalog for the mock e-commerce API
# This serves as an in-memory database replacement for testing purposes
# In production, this would be replaced with actual database queries

# Data Structure:
# category_data = {
#     "category_id": {
#         "name": "Category Name",
#         "subcategories": {
#             "subcategory_id": {
#                 "name": "Subcategory Name",
#                 "products": [list of product objects]
#             }
#         }
#     }
# }

category_data = {
    # ============================================
    # CATEGORY 1: ELECTRONICS
    # ============================================
    "1": {
        "name": "Electronics",
        "subcategories": {
            # Subcategory: Laptops (4 products)
            "1": {
                "name": "Laptops",
                "products": [
                    {
                        "id": 1001,
                        "name": "Dell Inspiron 15",
                        "price": 45000,
                        "originalPrice": 55000,
                        "discount": "18% off",
                        "rating": 4.5,
                        "inStock": True,
                        "specs": "Intel i5, 8GB RAM, 512GB SSD"
                    },
                    {
                        "id": 1002,
                        "name": "HP Pavilion",
                        "price": 48000,
                        "originalPrice": 60000,
                        "discount": "20% off",
                        "rating": 4.3,
                        "inStock": True,
                        "specs": "Intel i5, 16GB RAM, 1TB SSD"
                    },
                    {
                        "id": 1003,
                        "name": "Lenovo ThinkPad",
                        "price": 55000,
                        "originalPrice": 70000,
                        "discount": "21% off",
                        "rating": 4.7,
                        "inStock": True,
                        "specs": "Intel i7, 16GB RAM, 512GB SSD"
                    },
                    {
                        "id": 1004,
                        "name": "Asus VivoBook",
                        "price": 42000,
                        "originalPrice": 52000,
                        "discount": "19% off",
                        "rating": 4.4,
                        "inStock": False,  # Out of stock
                        "specs": "AMD Ryzen 5, 8GB RAM, 512GB SSD"
                    }
                ]
            },
            # Subcategory 2: Headphones
            "2": {
                "name": "Headphones",
                "products": [
                    {
                        "id": 1011,
                        "name": "Sony WH-1000XM4",
                        "price": 25000,
                        "originalPrice": 30000,
                        "discount": "17% off",
                        "rating": 4.8,
                        "inStock": True,
                        "specs": "Noise Cancelling, Bluetooth"
                    },
                    {
                        "id": 1012,
                        "name": "Bose QuietComfort",
                        "price": 28000,
                        "originalPrice": 32000,
                        "discount": "13% off",
                        "rating": 4.7,
                        "inStock": True,
                        "specs": "Active Noise Cancelling"
                    },
                    {
                        "id": 1013,
                        "name": "JBL Tune 750",
                        "price": 5000,
                        "originalPrice": 7000,
                        "discount": "29% off",
                        "rating": 4.2,
                        "inStock": True,
                        "specs": "Wireless, 15hr Battery"
                    }
                ]
            },
            # Subcategory 3: Cameras
            "3": {
                "name": "Cameras",
                "products": [
                    {
                        "id": 1021,
                        "name": "Canon EOS 1500D",
                        "price": 35000,
                        "originalPrice": 42000,
                        "discount": "17% off",
                        "rating": 4.6,
                        "inStock": True,
                        "specs": "24MP, DSLR, WiFi"
                    },
                    {
                        "id": 1022,
                        "name": "Nikon D3500",
                        "price": 32000,
                        "originalPrice": 38000,
                        "discount": "16% off",
                        "rating": 4.5,
                        "inStock": True,
                        "specs": "24MP, DSLR, Bluetooth"
                    },
                    {
                        "id": 1023,
                        "name": "Sony Alpha A6000",
                        "price": 45000,
                        "originalPrice": 55000,
                        "discount": "18% off",
                        "rating": 4.7,
                        "inStock": False,
                        "specs": "24MP, Mirrorless"
                    }
                ]
            }
        }
    },
    
    # ============================================
    # CATEGORY 2: CLOTHING STORE
    # ============================================
    "2": {
        "name": "Clothing Store",
        "subcategories": {
            # Subcategory 1: Men Clothing
            "1": {
                "name": "Men Clothing",
                "products": [
                    {
                        "id": 2001,
                        "name": "Men's Winter Sweater",
                        "price": 700,
                        "originalPrice": 1200,
                        "discount": "42% off",
                        "rating": 4.5,
                        "inStock": True,
                        "sizes": ["S", "M", "L", "XL", "XXL"]
                    },
                    {
                        "id": 2002,
                        "name": "Casual T-Shirt",
                        "price": 299,
                        "originalPrice": 599,
                        "discount": "50% off",
                        "rating": 4.2,
                        "inStock": True,
                        "sizes": ["S", "M", "L", "XL"]
                    },
                    {
                        "id": 2003,
                        "name": "Formal Shirt",
                        "price": 899,
                        "originalPrice": 1499,
                        "discount": "40% off",
                        "rating": 4.7,
                        "inStock": True,
                        "sizes": ["M", "L", "XL", "XXL"]
                    },
                    {
                        "id": 2004,
                        "name": "Denim Jeans",
                        "price": 1299,
                        "originalPrice": 2499,
                        "discount": "48% off",
                        "rating": 4.6,
                        "inStock": True,
                        "sizes": ["30", "32", "34", "36", "38"]
                    }
                ]
            },
            # Subcategory 2: Women Clothing
            "2": {
                "name": "Women Clothing",
                "products": [
                    {
                        "id": 2011,
                        "name": "Women's Kurti",
                        "price": 599,
                        "originalPrice": 1200,
                        "discount": "50% off",
                        "rating": 4.6,
                        "inStock": True,
                        "sizes": ["S", "M", "L", "XL"]
                    },
                    {
                        "id": 2012,
                        "name": "Saree",
                        "price": 1999,
                        "originalPrice": 3500,
                        "discount": "43% off",
                        "rating": 4.8,
                        "inStock": True,
                        "sizes": ["Free Size"]
                    },
                    {
                        "id": 2013,
                        "name": "Western Dress",
                        "price": 899,
                        "originalPrice": 1800,
                        "discount": "50% off",
                        "rating": 4.4,
                        "inStock": True,
                        "sizes": ["S", "M", "L"]
                    },
                    {
                        "id": 2014,
                        "name": "Leggings",
                        "price": 299,
                        "originalPrice": 599,
                        "discount": "50% off",
                        "rating": 4.3,
                        "inStock": True,
                        "sizes": ["S", "M", "L", "XL"]
                    }
                ]
            },
            # Subcategory 3: Baby Clothing
            "3": {
                "name": "Baby Clothing",
                "products": [
                    {
                        "id": 2021,
                        "name": "Baby Romper",
                        "price": 399,
                        "originalPrice": 799,
                        "discount": "50% off",
                        "rating": 4.7,
                        "inStock": True,
                        "sizes": ["0-3M", "3-6M", "6-12M"]
                    },
                    {
                        "id": 2022,
                        "name": "Baby Dress",
                        "price": 499,
                        "originalPrice": 999,
                        "discount": "50% off",
                        "rating": 4.5,
                        "inStock": True,
                        "sizes": ["0-3M", "3-6M", "6-12M"]
                    },
                    {
                        "id": 2023,
                        "name": "Baby Onesie Set",
                        "price": 699,
                        "originalPrice": 1299,
                        "discount": "46% off",
                        "rating": 4.6,
                        "inStock": True,
                        "sizes": ["0-3M", "3-6M"]
                    }
                ]
            }
        }
    },
    
    # ============================================
    # CATEGORY 3: TV & APPLIANCES
    # ============================================
    "3": {
        "name": "TV & Appliances",
        "subcategories": {
            # Subcategory 1: Televisions
            "1": {
                "name": "Televisions",
                "products": [
                    {
                        "id": 3001,
                        "name": "Samsung 43\" 4K Smart TV",
                        "price": 35000,
                        "originalPrice": 45000,
                        "discount": "22% off",
                        "rating": 4.5,
                        "inStock": True,
                        "specs": "4K UHD, Smart TV, HDR"
                    },
                    {
                        "id": 3002,
                        "name": "LG 55\" OLED TV",
                        "price": 85000,
                        "originalPrice": 120000,
                        "discount": "29% off",
                        "rating": 4.8,
                        "inStock": True,
                        "specs": "OLED, 4K, Dolby Vision"
                    },
                    {
                        "id": 3003,
                        "name": "Sony Bravia 50\" LED",
                        "price": 55000,
                        "originalPrice": 70000,
                        "discount": "21% off",
                        "rating": 4.6,
                        "inStock": False,
                        "specs": "4K, Android TV"
                    }
                ]
            },
            # Subcategory 2: Refrigerators
            "2": {
                "name": "Refrigerators",
                "products": [
                    {
                        "id": 3011,
                        "name": "Samsung Double Door 260L",
                        "price": 25000,
                        "originalPrice": 32000,
                        "discount": "22% off",
                        "rating": 4.4,
                        "inStock": True,
                        "specs": "260L, Frost Free"
                    },
                    {
                        "id": 3012,
                        "name": "LG Single Door 190L",
                        "price": 15000,
                        "originalPrice": 20000,
                        "discount": "25% off",
                        "rating": 4.3,
                        "inStock": True,
                        "specs": "190L, Direct Cool"
                    },
                    {
                        "id": 3013,
                        "name": "Whirlpool Triple Door 330L",
                        "price": 35000,
                        "originalPrice": 45000,
                        "discount": "22% off",
                        "rating": 4.6,
                        "inStock": True,
                        "specs": "330L, Frost Free"
                    }
                ]
            },
            # Subcategory 3: Washing Machines
            "3": {
                "name": "Washing Machines",
                "products": [
                    {
                        "id": 3021,
                        "name": "IFB Front Load 6kg",
                        "price": 22000,
                        "originalPrice": 28000,
                        "discount": "21% off",
                        "rating": 4.5,
                        "inStock": True,
                        "specs": "6kg, Front Load, 1000 RPM"
                    },
                    {
                        "id": 3022,
                        "name": "Samsung Top Load 7kg",
                        "price": 18000,
                        "originalPrice": 24000,
                        "discount": "25% off",
                        "rating": 4.4,
                        "inStock": True,
                        "specs": "7kg, Top Load"
                    },
                    {
                        "id": 3023,
                        "name": "LG Fully Automatic 8kg",
                        "price": 25000,
                        "originalPrice": 32000,
                        "discount": "22% off",
                        "rating": 4.6,
                        "inStock": False,
                        "specs": "8kg, Fully Automatic"
                    }
                ]
            }
        }
    },
    
    # ============================================
    # CATEGORY 4: SMARTPHONES
    # ============================================
    "4": {
        "name": "Smartphones",
        "subcategories": {
            # Subcategory 1: Android Phones
            "1": {
                "name": "Android Phones",
                "products": [
                    {
                        "id": 4001,
                        "name": "Samsung Galaxy S23",
                        "price": 65000,
                        "originalPrice": 80000,
                        "discount": "19% off",
                        "rating": 4.7,
                        "inStock": True,
                        "specs": "8GB RAM, 128GB, 5G"
                    },
                    {
                        "id": 4002,
                        "name": "OnePlus 11",
                        "price": 55000,
                        "originalPrice": 65000,
                        "discount": "15% off",
                        "rating": 4.6,
                        "inStock": True,
                        "specs": "12GB RAM, 256GB, 5G"
                    },
                    {
                        "id": 4003,
                        "name": "Xiaomi 13 Pro",
                        "price": 60000,
                        "originalPrice": 75000,
                        "discount": "20% off",
                        "rating": 4.5,
                        "inStock": True,
                        "specs": "12GB RAM, 256GB, 5G"
                    },
                    {
                        "id": 4004,
                        "name": "Realme GT 3",
                        "price": 35000,
                        "originalPrice": 45000,
                        "discount": "22% off",
                        "rating": 4.4,
                        "inStock": False,
                        "specs": "8GB RAM, 128GB, 5G"
                    }
                ]
            },
            # Subcategory 2: iPhones
            "2": {
                "name": "iPhones",
                "products": [
                    {
                        "id": 4011,
                        "name": "iPhone 14",
                        "price": 70000,
                        "originalPrice": 80000,
                        "discount": "13% off",
                        "rating": 4.8,
                        "inStock": True,
                        "specs": "128GB, A15 Bionic, 5G"
                    },
                    {
                        "id": 4012,
                        "name": "iPhone 14 Pro",
                        "price": 120000,
                        "originalPrice": 135000,
                        "discount": "11% off",
                        "rating": 4.9,
                        "inStock": True,
                        "specs": "256GB, A16 Bionic, 5G"
                    },
                    {
                        "id": 4013,
                        "name": "iPhone 13",
                        "price": 55000,
                        "originalPrice": 65000,
                        "discount": "15% off",
                        "rating": 4.7,
                        "inStock": True,
                        "specs": "128GB, A15 Bionic"
                    }
                ]
            },
            # Subcategory 3: Budget Phones
            "3": {
                "name": "Budget Phones",
                "products": [
                    {
                        "id": 4021,
                        "name": "Redmi Note 12",
                        "price": 15000,
                        "originalPrice": 20000,
                        "discount": "25% off",
                        "rating": 4.3,
                        "inStock": True,
                        "specs": "6GB RAM, 128GB, 4G"
                    },
                    {
                        "id": 4022,
                        "name": "Samsung Galaxy M14",
                        "price": 12000,
                        "originalPrice": 16000,
                        "discount": "25% off",
                        "rating": 4.2,
                        "inStock": True,
                        "specs": "4GB RAM, 64GB, 4G"
                    },
                    {
                        "id": 4023,
                        "name": "Realme Narzo 50",
                        "price": 13000,
                        "originalPrice": 18000,
                        "discount": "28% off",
                        "rating": 4.4,
                        "inStock": True,
                        "specs": "6GB RAM, 128GB, 4G"
                    }
                ]
            }
        }
    },
    
    # ============================================
    # CATEGORY 5: KITCHEN WARE
    # ============================================
    "5": {
        "name": "Kitchen Ware",
        "subcategories": {
            # Subcategory 1: Cookware
            "1": {
                "name": "Cookware",
                "products": [
                    {
                        "id": 5001,
                        "name": "Non-Stick Tawa",
                        "price": 599,
                        "originalPrice": 1200,
                        "discount": "50% off",
                        "rating": 4.4,
                        "inStock": True,
                        "specs": "28cm, Non-Stick Coating"
                    },
                    {
                        "id": 5002,
                        "name": "Pressure Cooker 5L",
                        "price": 1299,
                        "originalPrice": 2000,
                        "discount": "35% off",
                        "rating": 4.6,
                        "inStock": True,
                        "specs": "5L, Aluminum, ISI Certified"
                    },
                    {
                        "id": 5003,
                        "name": "Kadhai Set",
                        "price": 899,
                        "originalPrice": 1800,
                        "discount": "50% off",
                        "rating": 4.3,
                        "inStock": True,
                        "specs": "3 Piece Set, Non-Stick"
                    }
                ]
            },
            # Subcategory 2: Kitchen Appliances
            "2": {
                "name": "Kitchen Appliances",
                "products": [
                    {
                        "id": 5011,
                        "name": "Mixer Grinder",
                        "price": 2500,
                        "originalPrice": 4000,
                        "discount": "38% off",
                        "rating": 4.5,
                        "inStock": True,
                        "specs": "750W, 3 Jars"
                    },
                    {
                        "id": 5012,
                        "name": "Electric Kettle",
                        "price": 899,
                        "originalPrice": 1500,
                        "discount": "40% off",
                        "rating": 4.4,
                        "inStock": True,
                        "specs": "1.8L, Auto Shut-off"
                    },
                    {
                        "id": 5013,
                        "name": "Toaster",
                        "price": 1299,
                        "originalPrice": 2000,
                        "discount": "35% off",
                        "rating": 4.3,
                        "inStock": True,
                        "specs": "2 Slice, 800W"
                    }
                ]
            },
            # Subcategory 3: Dinnerware
            "3": {
                "name": "Dinnerware",
                "products": [
                    {
                        "id": 5021,
                        "name": "Dinner Set 24 Pieces",
                        "price": 1999,
                        "originalPrice": 4000,
                        "discount": "50% off",
                        "rating": 4.6,
                        "inStock": True,
                        "specs": "Ceramic, Microwave Safe"
                    },
                    {
                        "id": 5022,
                        "name": "Glass Set 6 Pieces",
                        "price": 399,
                        "originalPrice": 800,
                        "discount": "50% off",
                        "rating": 4.4,
                        "inStock": True,
                        "specs": "Transparent, 300ml"
                    },
                    {
                        "id": 5023,
                        "name": "Steel Plates Set",
                        "price": 899,
                        "originalPrice": 1500,
                        "discount": "40% off",
                        "rating": 4.5,
                        "inStock": True,
                        "specs": "Stainless Steel, 6 Pieces"
                    }
                ]
            }
        }
    },
    
    # ============================================
    # CATEGORY 6: HOME DECOR
    # ============================================
    "6": {
        "name": "Home Decor",
        "subcategories": {
            # Subcategory 1: Wall Art
            "1": {
                "name": "Wall Art",
                "products": [
                    {
                        "id": 6001,
                        "name": "Canvas Painting Set",
                        "price": 1299,
                        "originalPrice": 2500,
                        "discount": "48% off",
                        "rating": 4.5,
                        "inStock": True,
                        "specs": "3 Piece Set, Modern Art"
                    },
                    {
                        "id": 6002,
                        "name": "Wall Clock",
                        "price": 599,
                        "originalPrice": 1200,
                        "discount": "50% off",
                        "rating": 4.4,
                        "inStock": True,
                        "specs": "12 inch, Silent Movement"
                    },
                    {
                        "id": 6003,
                        "name": "Photo Frames Set",
                        "price": 799,
                        "originalPrice": 1500,
                        "discount": "47% off",
                        "rating": 4.3,
                        "inStock": True,
                        "specs": "5 Piece Set, Wooden"
                    }
                ]
            },
            # Subcategory 2: Lighting
            "2": {
                "name": "Lighting",
                "products": [
                    {
                        "id": 6011,
                        "name": "LED Ceiling Light",
                        "price": 1499,
                        "originalPrice": 2500,
                        "discount": "40% off",
                        "rating": 4.6,
                        "inStock": True,
                        "specs": "24W, Cool White"
                    },
                    {
                        "id": 6012,
                        "name": "Table Lamp",
                        "price": 899,
                        "originalPrice": 1500,
                        "discount": "40% off",
                        "rating": 4.4,
                        "inStock": True,
                        "specs": "Wooden Base, E27 Holder"
                    },
                    {
                        "id": 6013,
                        "name": "String Lights",
                        "price": 399,
                        "originalPrice": 800,
                        "discount": "50% off",
                        "rating": 4.5,
                        "inStock": True,
                        "specs": "10m, Warm White, USB"
                    }
                ]
            },
            # Subcategory 3: Cushions & Curtains
            "3": {
                "name": "Cushions & Curtains",
                "products": [
                    {
                        "id": 6021,
                        "name": "Cushion Covers Set",
                        "price": 599,
                        "originalPrice": 1200,
                        "discount": "50% off",
                        "rating": 4.4,
                        "inStock": True,
                        "specs": "5 Piece Set, Cotton"
                    },
                    {
                        "id": 6022,
                        "name": "Door Curtains",
                        "price": 899,
                        "originalPrice": 1800,
                        "discount": "50% off",
                        "rating": 4.5,
                        "inStock": True,
                        "specs": "7ft, Polyester, 2 Pieces"
                    },
                    {
                        "id": 6023,
                        "name": "Bedsheet Set",
                        "price": 1299,
                        "originalPrice": 2500,
                        "discount": "48% off",
                        "rating": 4.6,
                        "inStock": True,
                        "specs": "Double Bed, Cotton, 3 Pieces"
                    }
                ]
            }
        }
    }
}
