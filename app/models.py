# app/models.py
import jwt

from app import db
from flask_bcrypt import Bcrypt
from datetime import datetime,timedelta

class User(db.Model):
    """This class defines the users table"""
    __tablename__ = 'users'
    
    # Define the columns of the users table starting with the primary key
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(256), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    bucketlists = db.relationship('Bucketlist', order_by='Bucketlist.id', 
                                    cascade='all, delete-orphan')
                                    
    def __init__(self, email, password):
        """Initialize the user with an email and password"""
        self.email = email
        self.password = Bcrypt().generate_password_hash(password).decode()
        
    def password_is_valid(self, password):
        """Checks the password against its hash to validate the uses's password"""
        return Bcrypt.check_password_hash(self.password, password)
        
    def save(self):
        """
        Save a user to the database. 
        This includes creating a new user and editing one
        """
        db.session.add(self)
        db.session.commit()

    def generate_token(self, user_id):
        """Generates the access token"""
        try:
            # Set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=5),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # Create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET'),
                algorithm='HS256'
            )
            return jwt_string
        except Exception as e:
            # Return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the authorization header"""
        try:
            # Try to decode the token using the SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # If the token is expired, return error string
            return "Your token is expired. Please login to get a new token"
        except jwt.InvalidTokenError:
            # If the token is invalid, return an error string
            return "Invalid token. Register or login to get a valid one."

class Bucketlist(db.Model):
    """This class represents the bucketlist table"""
    __tablename__ = 'bucketlists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
                onupdate=db.func.current_timestamp())
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self,name):
        """Initialize with name"""
        self.name = name

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod
    def get_all(user_id):
        return Bucketlist.query.filter_by(created_by=user_id)

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        return "<Bucketlist: {}>".format(self.name)

