from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User 

class RegistrationView(MethodView):
    """Class to register new user"""
    def post(self):
        """Handle POST request for this view. Url => /auth/register"""
        
        # Query to see if user already exists
        user = User.query.filter_by(email=request.data['email']).first()
        
        if not user:
            # There is no user, so try registering
            try:
                post_data = request.data
                # Register the user
                email = post_data['email']
                password = post_data['password']
                user = User(email=email, password=password)
                user.save()
                
                response = {
                    'message': 'You registered successfully. Please log in'
                }
                # return a response to notify the user of the successful registration
                return make_response(jsonify(response)), 201
            except Exception as e:
                # Return a string message containing the occurred error
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
        else:
            # Return a message saying that the user already exists
            response = {
                'message': 'User already exists. Please login'
            }
            return make_response(jsonify(response)), 202
            
registration_view = RegistrationView('register_view')
# Define the rule for the registration. url => /auth/register
# Add the rule to blueprint
auth_blueprint.add_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])

    