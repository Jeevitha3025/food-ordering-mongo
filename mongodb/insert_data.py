from pymongo import MongoClient
from bson import ObjectId

client = MongoClient('mongodb://localhost:27017/')
db = client['sqs']

# Replace with your actual ObjectIds
kuteera_id = ObjectId('666ff9c4646cc1c66ef71a4b')
foodcourt_id = ObjectId('666ffa07646cc1c66ef71a4c')

menu_items = [
    # Kuteera Items
    (kuteera_id, 'Masala Dosa', 'South Indian', 70.00),
    (kuteera_id, 'Plain Dosa', 'South Indian', 60.00),
    (kuteera_id, 'Idli Vada', 'South Indian', 50.00),
    (kuteera_id, 'Upma', 'South Indian', 40.00),
    (kuteera_id, 'Pongal', 'South Indian', 55.00),
    (kuteera_id, 'Jeera Rice', 'Rice Items', 80.00),
    (kuteera_id, 'Lemon Rice', 'Rice Items', 70.00),
    (kuteera_id, 'Tamarind Rice', 'Rice Items', 75.00),
    (kuteera_id, 'Curd Rice', 'Rice Items', 65.00),
    (kuteera_id, 'Ghee Rice', 'Rice Items', 90.00),
    (kuteera_id, 'Bisi Bele Bath', 'Rice Items', 85.00),
    (kuteera_id, 'Paneer Butter Masala', 'Main Course', 180.00),
    (kuteera_id, 'Palak Paneer', 'Main Course', 170.00),
    (kuteera_id, 'Chole Bhature', 'Main Course', 120.00),
    (kuteera_id, 'Rajma Chawal', 'Main Course', 110.00),
    (kuteera_id, 'Dal Makhani', 'Main Course', 130.00),
    (kuteera_id, 'Vegetable Biryani', 'Main Course', 150.00),
    (kuteera_id, 'Butter Naan', 'Breads', 35.00),
    (kuteera_id, 'Garlic Naan', 'Breads', 40.00),
    (kuteera_id, 'Tandoori Roti', 'Breads', 20.00),
    (kuteera_id, 'Aloo Paratha', 'Breads', 45.00),
    (kuteera_id, 'Poori', 'Breads', 25.00),
    (kuteera_id, 'Gulab Jamun', 'Dessert', 40.00),
    (kuteera_id, 'Rasgulla', 'Dessert', 35.00),
    (kuteera_id, 'Gajar ka Halwa', 'Dessert', 60.00),
    (kuteera_id, 'Jalebi', 'Dessert', 30.00),
    (kuteera_id, 'Rasmalai', 'Dessert', 50.00),

    # Food Court Items
    (foodcourt_id, 'Masala Chai', 'Beverages', 20.00),
    (foodcourt_id, 'Filter Coffee', 'Beverages', 25.00),
    (foodcourt_id, 'Lassi', 'Beverages', 30.00),
    (foodcourt_id, 'Jaljeera', 'Beverages', 15.00),
    (foodcourt_id, 'Nimbu Pani', 'Beverages', 10.00),
    (foodcourt_id, 'Veg Samosa', 'Snacks', 20.00),
    (foodcourt_id, 'Paneer Tikka', 'Snacks', 140.00),
    (foodcourt_id, 'Hara Bhara Kabab', 'Snacks', 100.00),
    (foodcourt_id, 'Dhokla', 'Snacks', 60.00),
    (foodcourt_id, 'Bhel Puri', 'Snacks', 50.00),
    (foodcourt_id, 'Bombay Veg Sandwich', 'Sandwiches', 60.00),
    (foodcourt_id, 'Paneer Tikka Sandwich', 'Sandwiches', 80.00),
    (foodcourt_id, 'Grilled Cheese Sandwich', 'Sandwiches', 70.00),
    (foodcourt_id, 'Aloo Masala Sandwich', 'Sandwiches', 55.00),
    (foodcourt_id, 'Vegetable Mayo Sandwich', 'Sandwiches', 65.00),
    (foodcourt_id, 'Corn & Spinach Sandwich', 'Sandwiches', 75.00),
    (foodcourt_id, 'Plain Maggi', 'maggi', 40.00),
    (foodcourt_id, 'Masala Maggi', 'maggi', 50.00),
    (foodcourt_id, 'Cheese Maggi', 'maggi', 60.00),
    (foodcourt_id, 'Veg Masala Maggi', 'maggi', 55.00),
    (foodcourt_id, 'Paneer Maggi', 'maggi', 70.00),
]

for restaurant_id, name, category, price in menu_items:
    db.Menu_Items.insert_one({
        'restaurant_id': restaurant_id,
        'name': name,
        'category': category,
        'price': price
    })

print("✅ Full menu inserted successfully!")
