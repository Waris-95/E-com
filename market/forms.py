from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, HiddenField
from wtforms.validators import Length, EqualTo, Email, DataRequired, ValidationError
from market.models import User

# Register form class
class RegisterForm(FlaskForm):

    def validate_username(self, username_to_check):
        user = User.query.filter_by(username=username_to_check.data).first()
        if user:
            raise ValidationError('Username already exists. Please try a different username')

    username = StringField(label='Username:', validators=[Length(min=5, max=30), DataRequired()])
    email_address = StringField(label='Email:', validators=[Email(), DataRequired()])
    password1 = PasswordField(label='Password:', validators=[Length(min=8), DataRequired()])
    password2 = PasswordField(label='Confirm Password:', validators=[EqualTo('password1'), DataRequired()])
    submit_field = SubmitField(label='Signup')

    def validate_email_address(self, email_address):
        user = User.query.filter_by(email_address=email_address.data).first()
        if user:
            raise ValidationError('Email address already in use. Please choose different one')
        
# Login form class 
class LoginForm(FlaskForm):
    username = StringField(label="Username:", validators=[DataRequired()])
    password = PasswordField(label="Password:", validators=[DataRequired()])
    submit = SubmitField(label='Login')

# Purchase Item form
class PurchaseItemForm(FlaskForm):
    # purchased_item = HiddenField('Purchased Item')
    submit = SubmitField(label='Confirm order')
class SellItemForm(FlaskForm):
    submit = SubmitField(label='Sell')
