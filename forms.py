from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileSize, FileAllowed
from wtforms.fields import StringField,PasswordField,IntegerField,SubmitField
from wtforms.fields.simple import URLField
from wtforms.validators import DataRequired, length, ValidationError, equal_to

class ProductForm(FlaskForm):

    name = StringField("შეიყვანეთ ბრენდის სახელი", validators=[DataRequired(),
                                                                 length(min=3,max=32)])
    price = IntegerField("ფასდაკლების რაოდენობა", validators=[DataRequired()])
    img = FileField("ბრენდის სურათი", validators=[FileRequired(),
                                                    FileSize(1000 * 1000, message="შეამცირეთ ფაილის ზომა"),
                                                    FileAllowed(["jpg","png","jpeg"])])
    link = URLField("შეიყვანეთ ფასდაკლების ლინკი", validators=[DataRequired()])
    submit = SubmitField("შენახვა")

class RegisterForm(FlaskForm):
    username = StringField("მომხმარებელი", validators=[DataRequired()])
    password = PasswordField("პაროლი", validators=[DataRequired(),
                                                   length(min=8)])
    repeat_password = PasswordField("გაიმეორეთ პაროლი", validators=[equal_to("password")])
    register = SubmitField("რეგისტრაცია")

class LoginForm(FlaskForm):
    username = StringField("მომხმარებელი", validators=[DataRequired()])
    password = PasswordField("პაროლი", validators=[DataRequired(),
                                                   length(min=8)])
    login = SubmitField("ავტორიზაცია")