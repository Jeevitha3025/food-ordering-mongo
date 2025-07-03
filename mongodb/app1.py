from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)
app.secret_key = 'your_secret_key'

client = MongoClient("mongodb://localhost:27017/")
db = client['sqs']
menu_items_col = db['Menu_Items']
customers_col = db['Customers']
orders_col = db['Orders']
order_items_col = db['Order_Items']
restaurants_col = db['Restaurants']

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/customer', methods=['GET', 'POST'])
def customer():
    if request.method == 'POST':
        session.clear()
        name = request.form['name']
        phone = request.form['phone']
        email = request.form['email']
        customer = {"name": name, "phone": phone, "email": email}
        customer_id = customers_col.insert_one(customer).inserted_id
        session['customer_id'] = str(customer_id)
        return redirect(url_for('restaurant'))
    return render_template('customer.html')

@app.route('/restaurant', methods=['GET', 'POST'])
def restaurant():
    restaurants = list(restaurants_col.find())
    if request.method == 'POST':
        session['restaurant_id'] = request.form['restaurant']
        return redirect(url_for('order_type'))
    return render_template('restaurant.html', restaurants=restaurants)

@app.route('/order_type', methods=['GET', 'POST'])
def order_type():
    if request.method == 'POST':
        session['order_type'] = request.form['order_type']
        return redirect(url_for('categories'))
    return render_template('order_type.html')

@app.route('/categories', methods=['GET', 'POST'])
def categories():
    categories = menu_items_col.distinct("category", {"restaurant_id": ObjectId(session['restaurant_id'])})
    if request.method == 'POST':
        session['category'] = request.form['category']
        return redirect(url_for('items'))
    return render_template('categories.html', categories=categories)

@app.route('/items', methods=['GET', 'POST'])
def items():
    items = list(menu_items_col.find({
        "restaurant_id": ObjectId(session['restaurant_id']),
        "category": session['category']
    }))
    if request.method == 'POST':
        item_id = request.form['item_id']
        quantity = int(request.form['quantity'])
        item = menu_items_col.find_one({"_id": ObjectId(item_id)})
        cart_item = {"item_id": item_id, "name": item['name'], "price": item['price'], "quantity": quantity}
        if 'cart' not in session:
            session['cart'] = []
        cart = session['cart']
        for c in cart:
            if c['item_id'] == item_id:
                c['quantity'] += quantity
                break
        else:
            cart.append(cart_item)
        session['cart'] = cart
        return redirect(url_for('categories'))
    return render_template('items.html', items=items)

@app.route('/cart', methods=['GET', 'POST'])
def cart():
    if request.method == 'POST':
        action = request.form.get('action')
        index_val = request.form.get('index')
        if index_val is not None:
            index = int(index_val)
            cart = session.get('cart', [])
            if action == 'update':
                quantity = int(request.form['quantity'])
                if quantity > 0:
                    cart[index]['quantity'] = quantity
                else:
                    cart.pop(index)
            elif action == 'remove':
                cart.pop(index)
            session['cart'] = cart
        return redirect(url_for('cart'))

    cart = session.get('cart', [])
    subtotal = sum(item['price'] * item['quantity'] for item in cart)
    delivery_charge = subtotal * 0.05 if session['order_type'] == 'delivery' else 0
    total = subtotal + delivery_charge
    return render_template('cart.html', cart=cart, subtotal=subtotal, delivery_charge=delivery_charge, total=total)

@app.route('/confirm', methods=['POST'])
def confirm():
    cart = session.get('cart', [])
    if not cart:
        return redirect(url_for('categories'))
    order = {
        "customer_id": ObjectId(session['customer_id']),
        "restaurant_id": ObjectId(session['restaurant_id']),
        "order_type": session['order_type'],
        "items": cart
    }
    orders_col.insert_one(order)
    session.clear()
    return render_template('confirm.html')

@app.route('/cancel', methods=['POST'])
def cancel():
    session.clear()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
