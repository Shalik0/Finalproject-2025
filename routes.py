from flask import render_template, redirect, request
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from os import path
from uuid import uuid4

from sqlalchemy.sql.functions import current_user

from forms import ProductForm, RegisterForm, LoginForm
from models import Product, User
from ext import app, db

users = {
    "john":{"name": "John", "surname": "Doe", "age": "23", "img": "doe.jpg", "role": "admin"},
    "joella": {"name": "Joella", "surname": "Donna", "age": "20", "img": "doe.jpg", "role": "user"},
}


@app.route('/')
def home():
    return render_template('base.html')

@app.route('/')
def index():
    products = Product.query.all()
    return render_template('index.html', products=products, users=users)

@app.route("/search")
def search():
    name = request.args.get("srch")
    products = Product.query.filter(Product.name.ilike(f"%{name}%")).all()
    return render_template("products.html", products=products, users=users)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/products')
def show_products():
    products = Product.query.all()
    return render_template('products.html', products=products)

@app.route("/profile/<username>")
def profile(username):
    print("PRINTED", username)
    return render_template("profile.html", found_user=users.get(username))

@app.route('/register', methods=["GET","POST"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        password=form.password.data,
                        role="Guest")

        new_user.create()
        return redirect("/login")

    return render_template('register.html', form=form)

@app.route('/registerAdmin', methods=["GET","POST"])
def registerAdmin():
    form = RegisterForm()

    if form.validate_on_submit():
        new_user = User(username=form.username.data,
                        password=form.password.data,
                        role="Admin")

        new_user.create()
        return redirect("/login")

    return render_template('registerAdmin.html', form=form)

@app.route('/login', methods=["GET","POST"])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter(User.username == form.username.data).first()
        if user != None and user.check_password(form.password.data):

            login_user(user)
        return redirect("/products")

    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/products")

@app.route('/create_product', methods=["GET","POST"])
@login_required
def create_product():
    form = ProductForm()

    if form.validate_on_submit():
        file=form.img.data
        filename, filetype = path.splitext(file.filename)
        filename = uuid4 ()
        filepath = path.join(app.root_path,"static",f"{filename}{filetype}" )
        file.save(filepath)

        new_product= Product(name=form.name.data,
                            price=form.price.data,
                            img=f"{filename}{filetype}",
                            link = form.link.data)
        new_product.create()
        return redirect("/products")

    return render_template('create_product.html', form=form)

@app.route('/product/<int:product_id>')
def product_details(product_id):
    product = Product.query.get(product_id)
    return render_template('create_product.html', product=product)

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)

    if form.validate_on_submit():
        product.name = form.name.data
        product.price = form.price.data

        if form.img.data:
            file = form.img.data
            filename, filetype = path.splitext(file.filename)
            filename = str(uuid4())
            filepath = path.join(app.root_path, "static", f"{filename}{filetype}")
            file.save(filepath)
            product.img = f"{filename}{filetype}"

        product.save()
        return redirect('/products')

    return render_template('create_product.html', form=form, product=product, is_edit=True)


@app.route('/delete_product/<int:product_id>')
@login_required
def delete_product(product_id):
    product = Product.query.get(product_id)

    product.delete()

    return redirect('/products')
