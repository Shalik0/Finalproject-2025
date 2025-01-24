from ext import app, db
from models import Product

products = [
    {"name": "booomba", "price": "500$", "img": "doe.jpg", "link": "https://tbcconcept.ge/ge"},
    {"name": "side eye", "price": "100%", "img": "doe.jpg"},
]

with app.app_context():
    db.drop_all()
    db.create_all()

for product in products:
    print(f"Adding product: {product['name']}")
    new_product = Product(
        name=product["name"],
        price=product["price"],
        img=product["img"],
        link=product.get("link")
    )
    db.session.add(new_product)


db.session.commit()
print("Products added successfully!")