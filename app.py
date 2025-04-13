from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.secret_key = "supersecretkey"  # For flash messages

# Initialize SQLite database
def init_db():
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users 
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, 
                  username TEXT, 
                  email TEXT UNIQUE, 
                  password TEXT)''')
    conn.commit()
    conn.close()

    # Print all table names in the database
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table';")
    print(c.fetchall())
    conn.close()

@app.route("/")
def index():
    if 'user_id' not in session:
        return redirect(url_for('login_page'))  # Redirect to login if not logged in
    return render_template("index.html")

@app.route("/home")
def home():
    return redirect(url_for('index'))

@app.route("/login", methods=["GET", "POST"])
def login_page():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        print(f"Email: {email}, Password: {password}")  # Debugging log

        # Check user credentials in the database
        with sqlite3.connect('database.db') as conn:
            c = conn.cursor()
            c.execute("SELECT id, username, password FROM users WHERE email = ?", (email,))
            user = c.fetchone()

        print(f"User from DB: {user}")  # Debugging log

        if user and user[2] == password:  # Compare plain text passwords
            session['user_id'] = user[0]
            session['username'] = user[1]
            flash(f"Welcome back, {user[1]}!", "success")
            return redirect(url_for('index'))  # Redirect to the index page
        else:
            flash("Invalid email or password. Please try again.", "error")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for('login_page'))

@app.route("/signup", methods=['POST'])
def signup():
    username = request.form['username']
    email = request.form['email']
    password = request.form['password']  # Store plain text password

    try:
        conn = sqlite3.connect('database.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", 
                  (username, email, password))
        conn.commit()
        flash("Sign-up successful! Please log in.", "success")
        return redirect(url_for('login_page'))
    except sqlite3.IntegrityError:
        flash("Email already exists!", "error")
        return redirect(url_for('login_page'))
    finally:
        conn.close()

@app.route("/products")
def products():
    return render_template("products.html")

@app.route("/cart")
def cart():
    return render_template("cart.html")

@app.route("/checkout")
def checkout():
    return render_template('checkout.html')

@app.route("/fruits")
def fruits():
    return render_template("fruits.html")

@app.route("/vegetables")
def vegetables():
    return render_template("vegetables.html")

@app.route("/dairy")
def dairy():
    return render_template("dairy.html")

@app.route("/pantry")
def pantry():
    return render_template("pantry.html")

@app.route("/contact")
def contact():
    return render_template("contact.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/product_detail")
def product_detail():
    name = request.args.get('name', 'Unknown Product')
    price = request.args.get('price', '0')
    image = request.args.get('image', 'placeholder.jpg')
    return render_template('product_detail.html', name=name, price=price, image=image)

@app.route("/search")
def search():
    query = request.args.get('query', '').lower()
    products = [
        {"name": "Apples", "price": 108, "image": "https://assets.clevelandclinic.org/transform/cd71f4bd-81d4-45d8-a450-74df78e4477a/Apples-184940975-770x533-1_jpg"},
        {"name": "Mangoes", "price": 74, "image": "https://ichef.bbci.co.uk/images/ic/1920x1080/p06hk0h6.jpg"},
        {"name": "Bananas", "price": 40, "image": "https://nutritionsource.hsph.harvard.edu/wp-content/uploads/2018/08/bananas-1354785_1920.jpg"},
        {"name": "Kiwi", "price": 32, "image": "https://www.sakraworldhospital.com/assets/spl_splimgs/benefits-kiwi-of-fruit.webp"},
        {"name": "Grapes", "price": 73, "image": "https://m.media-amazon.com/images/I/71MQD-Dj1gL.jpg"},
        {"name": "Oranges", "price": 85, "image": "https://cdn-prod.medicalnewstoday.com/content/images/articles/272/272782/oranges-in-a-box.jpg"},
        {"name": "Watermelon", "price": 70, "image": "https://www.watermelon.org/wp-content/uploads/2020/07/Seeded-Wedge-scaled.jpg"},
        {"name": "Strawberry", "price": 80, "image": "https://www.jiomart.com/images/product/original/590001814/strawberry-small-pack-180-g-product-images-o590001814-p590116964-1-202412161658.jpg?im=Resize=(1000,1000)"},
        {"name": "Pineapple", "price": 55, "image": "https://www.healthxchange.sg/sites/hexassets/Assets/food-nutrition/pineapple-health-benefits-and-ways-to-enjoy.jpg"},
        {"name": "Onions", "price": 25, "image": "https://www.bbassets.com/media/uploads/p/xl/10000148_33-fresho-onion.jpg"},
        {"name": "Tomatoes", "price": 22, "image": "https://i0.wp.com/images-prod.healthline.com/hlcmsresource/images/AN_images/tomatoes-1296x728-feature.jpg?w=1155&h=1528"},
        {"name": "Brinjal", "price": 23, "image": "https://m.media-amazon.com/images/I/51XBbkVrvWL._AC_UF1000,1000_QL80_DpWeblab_.jpg"},
        {"name": "Spinach", "price": 10, "image": "https://images.unsplash.com/photo-1576045057995-568f588f82fb?fm=jpg&q=60&w=3000&ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8c3BpbmFjaHxlbnwwfHwwfHx8MA%3D%3D"},
        {"name": "Cauliflower", "price": 24, "image": "https://media.istockphoto.com/id/90634594/photo/close-up-of-several-heads-of-cauliflower.jpg?s=612x612&w=0&k=20&c=hpYY7BqSUNwM-oq26wNv5pGLSPf4HijXr3zA0J3yd0E="},
        {"name": "Potato", "price": 45, "image": "https://media.istockphoto.com/id/610765164/photo/new-potato.jpg?s=612x612&w=0&k=20&c=bSfq7ykW8Ztp7uU5cBvuOIaHZMD_I1XeToLalhGQWMY="},
        {"name": "Cabbage", "price": 30, "image": "https://media.istockphoto.com/id/673162168/photo/green-cabbage-isolated-on-white.jpg?s=612x612&w=0&k=20&c=mCc4mXATvCcfp2E9taRJBp-QPYQ_LCj6nE1D7geaqVk="},
        {"name": "Cucumber", "price": 15, "image": "https://seed2plant.in/cdn/shop/products/saladcucumberseeds.jpg?v=1603435556"},
        {"name": "Carrot", "price": 24, "image": "https://www.hhs1.com/hubfs/carrots%20on%20wood-1.jpg"},
        # New items
        {"name": "Milk", "price": 57, "image": "https://5.imimg.com/data5/SELLER/Default/2022/10/EZ/KE/XT/1486667/a2-cow-milk.jpg"},
        {"name": "Butter", "price": 275, "image": "https://www.heritagefoods.in/static/images/detailslider/mega/cooking-butter-1.png"},
        {"name": "Cheese", "price": 275, "image": "https://m.media-amazon.com/images/I/61+AzywctoL._AC_UF894,1000_QL80_.jpg"},
        {"name": "Ghee", "price": 748, "image": "https://www.eatingwell.com/thmb/EY63AWae1w0ru7GZQBhYf5zoug8=/1500x0/filters:no_upscale():max_bytes(150000):strip_icc()/what-is-ghee-b7d45427a4064055a4b3d920cf6c22a1.jpg"},
        {"name": "Yogurt", "price": 38, "image": "https://cdn.britannica.com/86/197886-050-014D8A12/bowl-yogurt.jpg"},
        {"name": "Paneer", "price": 430, "image": "https://www.frescocheese.com/wp-content/uploads/2023/01/slice-of-indian-paneer-cheese-and-cuttings-2021-12-09-02-39-31-utc-1024x683.jpg"},
        {"name": "Badam Milk", "price": 20, "image": "https://www.indianhealthyrecipes.com/wp-content/uploads/2023/04/badam-milk-recipe.jpg"},
        {"name": "Curd", "price": 35, "image": "https://dodladairy.com/wp-content/uploads/2024/01/Curd-cup.png"},
        {"name": "Rose Milk", "price": 50, "image": "https://www.spiceupthecurry.com/wp-content/uploads/2023/04/rose-milk-recipe-3.jpg"},
        {"name": "Basmati Rice", "price": 350, "image": "https://www.indianhealthyrecipes.com/wp-content/uploads/2023/07/basmati-rice-recipe-500x500.jpg"},
        {"name": "Turmeric Powder", "price": 154, "image": "https://m.media-amazon.com/images/I/41ZT+xOOaYL._AC_UF350,350_QL80_.jpg"},
        {"name": "Red Chilli Powder", "price": 450, "image": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSt-4J7BaPOFZkupmViS1o9F0gaxZ6f45Og_A&s"},
        {"name": "Wheat Flour", "price": 70, "image": "https://static.toiimg.com/thumb/msid-63797959,width-1070,height-580,resizemode-75/63797959,pt-32,y_pad-40/63797959.jpg"},
        {"name": "Gram Flour", "price": 104, "image": "https://nuttyyogi.com/cdn/shop/products/HealthyOrganic_Besan_1080x_cec1c8a6-8fb2-421c-a135-29858e0b0f6e.jpg?v=1606373711"},
        {"name": "Salt", "price": 62, "image": "https://jindalnaturecure.in/wp-content/uploads/2018/11/Beware-of-common-salt.jpg"},
        {"name": "Coffee", "price": 450, "image": "https://cdn.britannica.com/16/138916-050-93D18857/coffee-beans-ground-paper-bags.jpg?w=400&h=300&c=crop"},
        {"name": "Sunflower Oil", "price": 764, "image": "https://m.media-amazon.com/images/I/51dAFGjEDqL._AC_UF894,1000_QL80_DpWeblab_.jpg"},
        {"name": "Sugar", "price": 50, "image": "https://example.com/sugar.jpg"}
    ]

    filtered_products = [p for p in products if query in p['name'].lower()]

    return render_template('search_results.html', query=query, products=filtered_products)

@app.route("/test_redirect")
def test_redirect():
    return redirect(url_for('index'))

@app.errorhandler(404)
def page_not_found(e):
    return "Page not found. Check your routes and templates.", 404

@app.errorhandler(500)
def internal_server_error(e):
    return f"Internal server error: {str(e)}", 500

if __name__ == "__main__":
    print("Template folder:", app.template_folder)
    print("Static folder:", app.static_folder)
    print("Routes:")
    print(app.url_map)
    init_db()
    app.run(debug=True)