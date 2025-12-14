from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, SelectField, DateTimeField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, Email, Length, NumberRange, ValidationError
from wtforms.widgets import DateTimeInput
from datetime import datetime, timedelta
from models import User

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Length(max=20)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    is_service_provider = BooleanField('I am a service provider')
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username already taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email already registered. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class AuctionForm(FlaskForm):
    title = StringField('Service Title', validators=[DataRequired(), Length(max=200)])
    description = TextAreaField('Description', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('home_repair', 'Home Repair'),
        ('cleaning', 'Cleaning'),
        ('tutoring', 'Tutoring'),
        ('delivery', 'Delivery'),
        ('design', 'Design & Creative'),
        ('tech_support', 'Tech Support'),
        ('beauty', 'Beauty & Wellness'),
        ('automotive', 'Automotive'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    location = StringField('Location', validators=[DataRequired(), Length(max=200)])
    starting_bid = FloatField('Starting Bid (₹)', validators=[DataRequired(), NumberRange(min=1)])
    end_time = DateTimeField('End Time', validators=[DataRequired()], widget=DateTimeInput())
    
    # GPS Location fields
    location_type = SelectField('Service Area', choices=[
        ('local', 'Local Area (10km radius)'),
        ('city', 'City Wide (50km radius)'),
        ('state', 'State Wide (unlimited)')
    ], validators=[DataRequired()], default='city')
    city = StringField('City', validators=[DataRequired(), Length(min=2, max=100)])
    state = SelectField('State', choices=[
        ('andhra-pradesh', 'Andhra Pradesh'),
        ('arunachal-pradesh', 'Arunachal Pradesh'),
        ('assam', 'Assam'),
        ('bihar', 'Bihar'),
        ('chhattisgarh', 'Chhattisgarh'),
        ('goa', 'Goa'),
        ('gujarat', 'Gujarat'),
        ('haryana', 'Haryana'),
        ('himachal-pradesh', 'Himachal Pradesh'),
        ('jharkhand', 'Jharkhand'),
        ('karnataka', 'Karnataka'),
        ('kerala', 'Kerala'),
        ('madhya-pradesh', 'Madhya Pradesh'),
        ('maharashtra', 'Maharashtra'),
        ('manipur', 'Manipur'),
        ('meghalaya', 'Meghalaya'),
        ('mizoram', 'Mizoram'),
        ('nagaland', 'Nagaland'),
        ('odisha', 'Odisha'),
        ('punjab', 'Punjab'),
        ('rajasthan', 'Rajasthan'),
        ('sikkim', 'Sikkim'),
        ('tamil-nadu', 'Tamil Nadu'),
        ('telangana', 'Telangana'),
        ('tripura', 'Tripura'),
        ('uttar-pradesh', 'Uttar Pradesh'),
        ('uttarakhand', 'Uttarakhand'),
        ('west-bengal', 'West Bengal'),
        ('delhi', 'Delhi'),
        ('mumbai', 'Mumbai'),
        ('kolkata', 'Kolkata'),
        ('chennai', 'Chennai')
    ], validators=[DataRequired()])
    
    submit = SubmitField('Create Auction')

    def validate_end_time(self, end_time):
        if end_time.data <= datetime.utcnow():
            raise ValidationError('End time must be in the future.')
        if end_time.data > datetime.utcnow() + timedelta(days=30):
            raise ValidationError('End time cannot be more than 30 days from now.')

class BidForm(FlaskForm):
    amount = FloatField('Your Bid (₹)', validators=[DataRequired(), NumberRange(min=0.01)])
    submit = SubmitField('Place Bid')
