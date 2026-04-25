"""
Built-in sample product catalog for demonstration.
50 realistic products across 8 categories.
"""

SAMPLE_PRODUCTS = [
    # ── Laptops ───────────────────────────────────────────────────────────────
    {
        "name": "MacBook Air M3 13-inch",
        "brand": "Apple",
        "category": "laptop",
        "price": 1099,
        "description": "Ultra-thin laptop with Apple M3 chip, all-day battery life, and stunning Liquid Retina display. Perfect for students and professionals.",
        "specs": {"processor": "Apple M3", "ram": "8GB", "storage": "256GB SSD", "display": "13.6-inch Liquid Retina", "battery": "18 hours", "weight": "2.7 lbs"},
        "url": "https://apple.com/macbook-air"
    },
    {
        "name": "MacBook Pro 14-inch M3 Pro",
        "brand": "Apple",
        "category": "laptop",
        "price": 1999,
        "description": "Professional-grade laptop with M3 Pro chip, ProMotion display, and exceptional performance for creative workflows.",
        "specs": {"processor": "Apple M3 Pro", "ram": "18GB", "storage": "512GB SSD", "display": "14.2-inch Liquid Retina XDR", "battery": "18 hours", "weight": "3.5 lbs"},
        "url": "https://apple.com/macbook-pro"
    },
    {
        "name": "Dell XPS 15",
        "brand": "Dell",
        "category": "laptop",
        "price": 1799,
        "description": "Premium Windows laptop with OLED display, powerful Intel Core i7, and sleek aluminum design. Ideal for content creators.",
        "specs": {"processor": "Intel Core i7-13700H", "ram": "16GB DDR5", "storage": "512GB NVMe SSD", "display": "15.6-inch OLED Touch", "battery": "13 hours", "weight": "4.2 lbs"},
        "url": "https://dell.com/xps15"
    },
    {
        "name": "Lenovo ThinkPad X1 Carbon Gen 11",
        "brand": "Lenovo",
        "category": "laptop",
        "price": 1349,
        "description": "Business ultrabook with legendary ThinkPad reliability, military-grade durability, and enterprise security features.",
        "specs": {"processor": "Intel Core i5-1335U", "ram": "16GB", "storage": "256GB SSD", "display": "14-inch IPS", "battery": "15 hours", "weight": "2.48 lbs"},
        "url": "https://lenovo.com/thinkpad-x1"
    },
    {
        "name": "ASUS ROG Zephyrus G14",
        "brand": "ASUS",
        "category": "laptop",
        "price": 1449,
        "description": "Compact gaming laptop with AMD Ryzen 9 and NVIDIA RTX 4060. Blazing performance in a portable chassis.",
        "specs": {"processor": "AMD Ryzen 9 7940HS", "ram": "16GB DDR5", "storage": "1TB SSD", "display": "14-inch QHD 165Hz", "gpu": "RTX 4060", "weight": "3.8 lbs"},
        "url": "https://asus.com/rog-zephyrus-g14"
    },
    {
        "name": "HP Spectre x360 14",
        "brand": "HP",
        "category": "laptop",
        "price": 1299,
        "description": "2-in-1 convertible laptop with OLED display and Intel Evo platform. Use it as a tablet or laptop.",
        "specs": {"processor": "Intel Core Ultra 7", "ram": "16GB", "storage": "512GB SSD", "display": "14-inch OLED 2.8K", "battery": "17 hours", "weight": "3.01 lbs"},
        "url": "https://hp.com/spectre-x360"
    },
    {
        "name": "Acer Swift 3 Slim",
        "brand": "Acer",
        "category": "laptop",
        "price": 649,
        "description": "Budget-friendly ultrabook with AMD Ryzen 7 and fast SSD. Great value for everyday computing tasks.",
        "specs": {"processor": "AMD Ryzen 7 7730U", "ram": "16GB", "storage": "512GB SSD", "display": "14-inch FHD IPS", "battery": "12 hours", "weight": "2.65 lbs"},
        "url": "https://acer.com/swift-3"
    },

    # ── Smartphones ───────────────────────────────────────────────────────────
    {
        "name": "iPhone 15 Pro",
        "brand": "Apple",
        "category": "smartphone",
        "price": 999,
        "description": "Pro-grade smartphone with titanium design, A17 Pro chip, and 48MP camera system with 5x optical zoom.",
        "specs": {"chip": "A17 Pro", "storage": "128GB", "display": "6.1-inch Super Retina XDR", "camera": "48MP main + 12MP ultrawide + 12MP 5x telephoto", "battery": "Up to 23 hours", "color": "Natural Titanium"},
        "url": "https://apple.com/iphone-15-pro"
    },
    {
        "name": "Samsung Galaxy S24 Ultra",
        "brand": "Samsung",
        "category": "smartphone",
        "price": 1299,
        "description": "Flagship Android phone with built-in S Pen, 200MP camera, and Snapdragon 8 Gen 3 processor.",
        "specs": {"processor": "Snapdragon 8 Gen 3", "ram": "12GB", "storage": "256GB", "display": "6.8-inch QHD+ Dynamic AMOLED", "camera": "200MP main", "battery": "5000mAh"},
        "url": "https://samsung.com/galaxy-s24-ultra"
    },
    {
        "name": "Google Pixel 8a",
        "brand": "Google",
        "category": "smartphone",
        "price": 499,
        "description": "Affordable Pixel with Google Tensor G3 chip, excellent camera AI, and guaranteed 7 years of updates.",
        "specs": {"processor": "Tensor G3", "ram": "8GB", "storage": "128GB", "display": "6.1-inch OLED 120Hz", "camera": "64MP main + 13MP ultrawide", "battery": "4492mAh"},
        "url": "https://store.google.com/pixel-8a"
    },
    {
        "name": "OnePlus 12",
        "brand": "OnePlus",
        "category": "smartphone",
        "price": 799,
        "description": "Flagship killer with Snapdragon 8 Gen 3, 100W fast charging, and Hasselblad-tuned cameras.",
        "specs": {"processor": "Snapdragon 8 Gen 3", "ram": "12GB", "storage": "256GB", "display": "6.82-inch LTPO AMOLED 120Hz", "camera": "50MP Hasselblad", "charging": "100W SuperVOOC"},
        "url": "https://oneplus.com/12"
    },

    # ── Headphones ────────────────────────────────────────────────────────────
    {
        "name": "Sony WH-1000XM5",
        "brand": "Sony",
        "category": "headphones",
        "price": 349,
        "description": "Industry-leading noise cancellation headphones with 30-hour battery, multipoint connection, and exceptional sound quality.",
        "specs": {"type": "Over-ear", "anc": "Yes - Industry Leading", "battery": "30 hours", "driver": "30mm", "connectivity": "Bluetooth 5.2", "weight": "250g"},
        "url": "https://sony.com/wh1000xm5"
    },
    {
        "name": "Apple AirPods Pro 2nd Gen",
        "brand": "Apple",
        "category": "earbuds",
        "price": 249,
        "description": "Premium true wireless earbuds with Adaptive Transparency, Personalized Spatial Audio, and H2 chip.",
        "specs": {"type": "In-ear TWS", "anc": "Adaptive ANC", "battery": "6 hours (30 with case)", "chip": "H2", "connectivity": "Bluetooth 5.3", "water_resistance": "IPX4"},
        "url": "https://apple.com/airpods-pro"
    },
    {
        "name": "Bose QuietComfort 45",
        "brand": "Bose",
        "category": "headphones",
        "price": 279,
        "description": "Legendary Bose noise cancellation with TriPort acoustic architecture, 24-hour battery, and plush comfort.",
        "specs": {"type": "Over-ear", "anc": "WorldClass QuietComfort", "battery": "24 hours", "connectivity": "Bluetooth 5.1", "weight": "238g", "foldable": "Yes"},
        "url": "https://bose.com/quietcomfort-45"
    },
    {
        "name": "Jabra Evolve2 85",
        "brand": "Jabra",
        "category": "headphones",
        "price": 449,
        "description": "Professional wireless headset with advanced ANC, dual connectivity, and 37-hour battery. Built for work from anywhere.",
        "specs": {"type": "Over-ear", "anc": "8-mic ANC", "battery": "37 hours", "connectivity": "Bluetooth 5.0 + USB", "weight": "340g", "certifications": "UC Optimized"},
        "url": "https://jabra.com/evolve2-85"
    },

    # ── Smartwatches ──────────────────────────────────────────────────────────
    {
        "name": "Apple Watch Series 9",
        "brand": "Apple",
        "category": "smartwatch",
        "price": 399,
        "description": "Most advanced Apple Watch with S9 chip, Double Tap gesture, and brighter Always-On Retina display.",
        "specs": {"chip": "S9 SiP", "display": "45mm LTPO OLED", "battery": "18 hours", "gps": "Yes", "health": "ECG, Blood Oxygen, Crash Detection", "water_resistance": "50m"},
        "url": "https://apple.com/apple-watch-series-9"
    },
    {
        "name": "Samsung Galaxy Watch 6 Classic",
        "brand": "Samsung",
        "category": "smartwatch",
        "price": 379,
        "description": "Premium Android smartwatch with rotating bezel, sapphire crystal display, and comprehensive health tracking.",
        "specs": {"display": "47mm Super AMOLED", "battery": "40 hours", "os": "Wear OS + One UI Watch 5", "health": "BioActive Sensor, ECG, Blood Pressure", "water_resistance": "5ATM + IP68", "material": "Stainless Steel"},
        "url": "https://samsung.com/galaxy-watch-6-classic"
    },
    {
        "name": "Garmin Fenix 7X Solar",
        "brand": "Garmin",
        "category": "smartwatch",
        "price": 899,
        "description": "Premium GPS multisport watch with solar charging, 28-day battery life, and military-grade durability.",
        "specs": {"display": "51mm MIP", "battery": "28 days (37 with solar)", "gps": "Multi-band GPS", "sensors": "Heart rate, SpO2, HRV", "water_resistance": "100m", "material": "Titanium bezel"},
        "url": "https://garmin.com/fenix-7x"
    },

    # ── Cameras ───────────────────────────────────────────────────────────────
    {
        "name": "Sony Alpha 7 IV",
        "brand": "Sony",
        "category": "camera",
        "price": 2499,
        "description": "Full-frame mirrorless camera with 33MP BSI sensor, 4K 60fps video, and real-time Eye AF tracking.",
        "specs": {"sensor": "33MP Full-frame BSI Exmor R", "processor": "BIONZ XR", "video": "4K 60fps", "autofocus": "759-point PDAF", "ibis": "5.5-stop", "weather_sealing": "Yes"},
        "url": "https://sony.com/alpha-a7iv"
    },
    {
        "name": "Fujifilm X100VI",
        "brand": "Fujifilm",
        "category": "camera",
        "price": 1599,
        "description": "Iconic fixed-lens compact camera with 40MP sensor, in-body stabilization, and stunning retro design.",
        "specs": {"sensor": "40MP X-Trans BSI CMOS 5 HR", "lens": "23mm f/2 (35mm equiv.)", "video": "6.2K 30fps", "ibis": "6-stop", "viewfinder": "Hybrid OVF/EVF", "weather_sealing": "Yes"},
        "url": "https://fujifilm.com/x100vi"
    },

    # ── Tablets ───────────────────────────────────────────────────────────────
    {
        "name": "iPad Pro 11-inch M4",
        "brand": "Apple",
        "category": "tablet",
        "price": 999,
        "description": "Incredibly thin and powerful tablet with M4 chip, Ultra Retina XDR display, and Apple Pencil Pro support.",
        "specs": {"chip": "Apple M4", "display": "11-inch Ultra Retina XDR", "storage": "256GB", "camera": "12MP wide + 10MP ultrawide", "battery": "10 hours", "thickness": "5.3mm"},
        "url": "https://apple.com/ipad-pro"
    },
    {
        "name": "Samsung Galaxy Tab S9+",
        "brand": "Samsung",
        "category": "tablet",
        "price": 999,
        "description": "Premium Android tablet with Dynamic AMOLED display, included S Pen, and DeX desktop mode.",
        "specs": {"processor": "Snapdragon 8 Gen 2", "ram": "12GB", "storage": "256GB", "display": "12.4-inch Dynamic AMOLED 2X 120Hz", "battery": "10090mAh", "s_pen": "Included"},
        "url": "https://samsung.com/galaxy-tab-s9-plus"
    },

    # ── Shoes / Sneakers ──────────────────────────────────────────────────────
    {
        "name": "Nike Air Max 270",
        "brand": "Nike",
        "category": "shoes",
        "price": 150,
        "description": "Lifestyle sneaker with Nike's largest Air unit yet, offering all-day cushioning and a bold silhouette.",
        "specs": {"sole": "Max Air 270 unit", "upper": "Mesh + synthetic", "closure": "Lace-up", "style": "Lifestyle/Casual", "colors": "Multiple colorways", "gender": "Unisex"},
        "url": "https://nike.com/air-max-270"
    },
    {
        "name": "Adidas Ultraboost 23",
        "brand": "Adidas",
        "category": "shoes",
        "price": 190,
        "description": "Performance running shoes with BOOST midsole, Primeknit upper, and Continental rubber outsole.",
        "specs": {"sole": "BOOST midsole", "upper": "Primeknit+", "closure": "Lace-up", "style": "Running/Performance", "drop": "10mm", "weight": "312g"},
        "url": "https://adidas.com/ultraboost-23"
    },
    {
        "name": "New Balance 990v6",
        "brand": "New Balance",
        "category": "shoes",
        "price": 185,
        "description": "Heritage running shoe made in the USA with ENCAP midsole, pigskin leather upper, and classic design.",
        "specs": {"sole": "ENCAP + blown rubber", "upper": "Pigskin leather + mesh", "closure": "Lace-up", "style": "Heritage/Lifestyle", "made_in": "USA", "width_options": "Multiple"},
        "url": "https://newbalance.com/990v6"
    },
]
