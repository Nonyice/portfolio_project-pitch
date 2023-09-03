from flask import Flask, render_template, request, redirect, url_for,jsonify

import psycopg2
import keyring

app = Flask(__name__, static_url_path='/static')
app.config['SECRET_KEY'] = 'mealtreat'

# Configure database connection details

db_host = "127.0.0.1"
db_name = "meal-treat"
db_user = "postgres"
db_password = keyring.get_password('meal-treat', 'postgres')

#Define the route for the homepage
@app.route('/')
def home():
    return render_template('index.html')
    

# Define the route for the contact form
@app.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        email = request.form['email']
        message = request.form['message']

        # Connect to the database
        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        cur = conn.cursor()

        # Insert form data into the database
        cur.execute("INSERT INTO contact_form (name, email, message) VALUES (%s, %s, %s)",
                    (name, email, message))
        #Commit the database insertions
        conn.commit()

        # Close the database connection
        cur.close()
        conn.close()

        return 'Form submitted successfully!'
    
    return render_template('contact.html')

@app.route('/services')
def services():
    return render_template('services.html')


# Calculate order price based on order details
def compute_total_price(order_details):
    price_menu = {
    'White Rice/Chicken': 1060,
    'Vegetable Soup/Fufu/Beef': 890,
    'Beans(Poridge)': 1250,
    'cake': 2500,
    'chin_chin(painter)': 5000,
    'small_chops': 1900
    }

    total_price = 0

    for item in order_details:
        if item in price_menu:
            total_price += price_menu[item]
    return total_price


@app.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        customer_name = request.form.get('customer_name')
        phone_number = request.form.get('phone_number')
        location = request.form.get('location')
        order_details = request.form.getlist('order_details')

        # Calculate the total price
        total_price = compute_total_price(order_details)
        order_price = total_price

        # Save order to the database
        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        cursor = conn.cursor()
        
        cursor.execute('INSERT INTO orders (customer_name, phone_number, location, order_details, order_price) VALUES (%s, %s, %s, %s, %s)',
                (customer_name, phone_number, location, order_details, order_price))
        conn.commit()
        order_id = cursor.lastrowid
        cursor.close()
        conn.close()

        # Render the template to display the total price and confirm the order
        return render_template('confirm_order.html', total_price=total_price,
                               customer_name=customer_name, phone_number=phone_number,
                               location=location, order_details=order_details)

        

        # Send order details to the restaurant
        restaurant_message = f"New Order Received!\n\nCustomer: {customer_name}\nPhone Number: {phone_number}\nLocation: {location}\nOrder Details: {order_details}"
        # Here in the next version i will include mobile and email notification to the restaurant
        # Redirect to confirmation page
        return redirect(url_for('confirm_order', order_id=order_id))
    

    # Render the order form template
    return render_template('order.html')


@app.route('/confirm_order', methods=['POST'])
def confirm_order():
    # Get the form data from the request

    customer_name = request.form.get('customer_name')
    phone_number = request.form.get('phone_number')
    location = request.form.get('location')
    order_details = request.form.getlist('order_details')
    total_price = float(request.form.get('total_price'))

    if request.method == 'POST':
        if request.form.get('confirm_button') == 'confirm':
            # I will implement Payment method here in the next version
            # After successful payment, return success message
            # Render the success message template
            return render_template('order_success.html')
        else:
            return 'Order canceled successfully!'
            # Order canceled by the customer, delete the order from the database
        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        cursor = conn.cursor()
        cursor.execute('DELETE FROM orders WHERE id = %s', (order_id,))
        conn.commit()
        conn.close()

            
    
    return render_template('confirm_order.html', order=order)

@app.route('/submit_review', methods=['GET', 'POST'])
def leave_a_review():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form['name']
        review = request.form['review']
        image_data = request.files['image_data']

        #Read image files as binary
        image_bytes = image_data.read()

        # Connect to the database
        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        cur = conn.cursor()
  
        # Insert form data into the database
        cur.execute("INSERT INTO customer_review (name, review, image_data) VALUES (%s, %s, %s)",
                    (name, review, psycopg2.Binary(image_bytes)))
        #Commit the database insertions
        conn.commit()

        # Close the database connection
        cur.close()
        conn.close()

        return 'Review submitted successfully!'
    
    return render_template('submit_review.html')

@app.route('/add_reviews')
def new_review():

    try:
        conn = psycopg2.connect(host=db_host, dbname=db_name, user=db_user, password=db_password)
        cur = conn.cursor()

        cursor.execute('SELECT name, review, image_data FROM customer_review')
        customer_review = [{'name': name, 'review': review, 'image': image_data} for name, review, image_data in cursor.fetchall()]
        
        cursor.close()
        conn.close()

    except Exception as e:
        return str(e)


    


if __name__ == '__main__':
    app.run(debug=True)
