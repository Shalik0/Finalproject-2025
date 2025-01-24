from ext import app
from routes import index, search, about, profile, register, login, logout, create_product, edit_product, delete_product


app.run(debug=True, host="0.0.0.0")