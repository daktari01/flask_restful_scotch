# /tests/test_auth.py

import unittest
import json
from app import create_app, db

class AuthTestCase(unittest.TestCase):
    """Test case for the authentication blueprint."""

    def setUp(self):
        """Set up test variables."""
        self.app = create_app(config_name="testing")
        # Initialize the test client
        self.client = self.app.test_client
        # This is the user test json data with a predefined email and password
        self.user_data = {
            'email': 'test@example.com',
            'password': 'test_password'
        }

        with self.app.app_context():
            # Create all tables
            db.session.close()
            db.drop_all()
            db.create_all()

    def test_registration(self):
        """Test user registration works correcty."""
        res = self.client().post('/auth/register', data=self.user_data)
        print(res)
        # Get the results returned in json format
        result = json.loads(res.data.decode())
        # Assert that the request contains a success message and a 201 status code
        self.assertEqual(result['message'], "You registered successfully. Please log in.")
        self.assertEqual(res.status_code, 201)

    def test_already_registered_user(self):
        """Test that a user cannot be registered twice."""
        res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        second_res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(second_res.status_code, 202)
        # Get the results returned in json format
        result = json.loads(second_res.data.decode())
        self.assertEqual(
            result['message'], "User already exists. Please login.")

    def test_user_login(self):
        """Test registered user can login"""
        res = self.client().post('/auth/register', data=self.user_data)
        self.assertEqual(res.status_code, 201)
        login_res = self.client().post('/auth/register', data=self.user_data)
        # Get the results in json format
        result = json.loads(login_res.decode())
        # Test that response contains success message
        self.assertEqual(result['message'], "You logged in successfully.")
        # Assert that the status code is 200
        self.assertEqual(login_res.status_code, 200)
        self.assertTrue(result['access_token'])

    def test_non_registered_user_login(self):
        """Test non registered users cannot login"""
        # Define a dictionary to represent an unregistered user
        not_a_user = {
            'email': 'not_a_user@example.com',
            'password': 'nope'
        }
        # Send a request to /auth/register with the information above
        res = self.client().post('/auth/register', data=not_a_user)
        # Get the result in json
        result = json.loads(res.data.decode()) 
        # Assert that the response contains an error message and an error 
        # status_code 401 (Unauthorized)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(
            result['message'], "Invalid email or password. Please try again")
