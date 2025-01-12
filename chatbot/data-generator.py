import random
import csv

# Categories and associated product names
categories = {
    'electronics': [
        'Apple iPad Pro', 
        'Samsung 4K Smart TV', 
        'Sony Noise Cancelling Headphones', 
        'GoPro HERO11 Black', 
        'Dell XPS Laptop', 
        'Apple AirPods Pro', 
        'Beats Studio3 Wireless Headphones', 
        'Nintendo Switch OLED', 
        'Canon EOS R6 Camera', 
        'Bose SoundLink Bluetooth Speaker'
    ],
    'clothing': [
        'Levi\'s 501 Original Jeans', 
        'Nike Air Max Sneakers', 
        'The North Face Denali Jacket', 
        'Adidas Ultraboost Running Shoes', 
        'Columbia Winter Coat', 
        'Patagonia Fleece Pullover', 
        'Under Armour Running Shorts', 
        'Ray-Ban Aviator Sunglasses', 
        'Calvin Klein Hoodie', 
        'Timberland Boots'
    ],
    'household': [
        'Instant Pot Duo 7-in-1', 
        'Keurig K-Elite Coffee Maker', 
        'Roomba i7+ Robot Vacuum', 
        'Dyson V11 Cordless Vacuum', 
        'KitchenAid Stand Mixer', 
        'Ninja Air Fryer', 
        'Cuisinart Food Processor', 
        'Breville Smart Oven', 
        'Samsung Family Hub Refrigerator', 
        'Philips Sonicare Toothbrush'
    ],
    'footwear': [
        'Crocs Classic Clog', 
        'Nike Air Force 1', 
        'Birkenstock Arizona Sandals', 
        'Skechers Memory Foam Shoes', 
        'New Balance Running Shoes', 
        'ASICS Gel-Kayano Sneakers', 
        'Dr. Martens 1460 Boots', 
        'Vans Old Skool Sneakers', 
        'Converse Chuck Taylor All Stars', 
        'Hoka One One Running Shoes'
    ],
    'watches': [
        'Casio G-Shock Digital Watch', 
        'Fossil Hybrid Smartwatch', 
        'Timex Weekender', 
        'Seiko 5 Automatic', 
        'Apple Watch Series 8', 
        'Garmin Fenix 7', 
        'Michael Kors Smartwatch', 
        'Fitbit Versa 3', 
        'Citizen Eco-Drive', 
        'Samsung Galaxy Watch 5'
    ],
    'computer accessories': [
        'Blue Yeti USB Microphone', 
        'Logitech MX Master 3 Mouse', 
        'Razer Blackwidow Keyboard', 
        'WD 2TB External Hard Drive', 
        'Dell Ultrasharp Monitor', 
        'Logitech C920 Webcam', 
        'SteelSeries Arctis Pro Headset', 
        'Elgato Stream Deck', 
        'Anker USB-C Hub', 
        'Samsung T7 Portable SSD'
    ],
    'pet supplies': [
        'Purina Pro Plan Dog Food', 
        'Kong Classic Dog Toy', 
        'Cat Litter Robot', 
        'Seresto Flea Collar', 
        'Wellness Core Dog Food', 
        'Interactive Cat Laser Toy', 
        'Dog Training Pads', 
        'Raised Dog Feeding Station', 
        'Cat Scratching Post', 
        'Automatic Pet Feeder'
    ],
    'grocery': [
        'Tide Pods Laundry Detergent', 
        'Starbucks Coffee Beans', 
        'Oreo Cookies', 
        'Hidden Valley Ranch Dressing', 
        'Ben & Jerry\'s Ice Cream', 
        'Heinz Ketchup', 
        'Kraft Mac & Cheese', 
        'Nature Valley Granola Bars', 
        'Skippy Peanut Butter', 
        'Cheerios Cereal'
    ]
}

def generate_product_data(num_products):
    products = []
    used_products = set()

    while len(products) < num_products:
        category = random.choice(list(categories.keys()))
        product = random.choice(categories[category])
        
        if product not in used_products:
            price = round(random.uniform(10, 2000), 2)
            discount = round(random.uniform(5, 30), 0)
            shipping_days = random.randint(1, 7)
            rating = round(random.uniform(3.5, 5), 1)
            
            products.append([
                product, 
                price, 
                f"{discount}%", 
                f"{shipping_days}", 
                rating, 
                category
            ])
            used_products.add(product)

    return products

# Generate 50 unique products
product_data = generate_product_data(50)

# Write to CSV
with open('product_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Product', 'Price', 'Discount', 'Shipping Time', 'Rating', 'Category'])
    writer.writerows(product_data)


for product in product_data:
    print(f"{product[0]},{product[1]},{product[2]},{product[3]},{product[4]},{product[5]}")