from main import app
import unittest
import pyrebase

# working code

class RoutingTest(unittest.TestCase):      
    def test_home(self):
        tester = app.test_client(self)
        pages = ['/','/login', '/signup', '/index']
        for page in pages:
            response = tester.get(page, content_type='html/text')
            self.assertEqual(response.status_code, 200)
    def test_other(self):
        tester = app.test_client(self)
        response = tester.get('test', content_type='html/text')
        self.assertEqual(response.status_code, 404)
    print("routing test case passed")

class TestIntro(unittest.TestCase):

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_intro(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'<a href="http://127.0.0.1:5000/login"><button class="button">Log in</button></a>', response.data)
        self.assertIn(b'<a href="http://127.0.0.1:5000/signup"><button class="button">Sign up</button></a>', response.data)

class TestRegister(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        self.app = app.test_client()

    # executed after each test
    def tearDown(self):
        pass

    def test_register(self):
        result = self.app.get('/signup')
        self.assertEqual(result.status_code, 200)
        self.assertIn(b'Pyrebase-Flask-Login', result.data)

class TestLogin(unittest.TestCase):
     
    def setUp(self):
        config = {
            "apiKey": "AIzaSyAHNUwFLMVv91t3ntaXYTCglULRlIg0oJw",
            "authDomain": "pricecompareg28.firebaseapp.com",
            "databaseURL": "https://pricecompareg28-default-rtdb.firebaseio.com/" ,
            "projectId": "pricecompareg28",
            "storageBucket": "pricecompareg28.appspot.com",
            "messagingSenderId": "30273225015",
            "appId": "1:30273225015:web:efd069b091f2c35dea9ab2",
            "measurementId": "G-FFNVTMBVDV",
        }
        self.firebase = pyrebase.initialize_app(config)
        self.db = self.firebase.database()

    def test_login_valid(self):
        email = "testname@yaho.com"
        password = "Qwerty123"
        auth = self.firebase.auth()
        user = auth.sign_in_with_email_and_password(email, password)
        self.assertEqual(user['email'], email)
        print("Valid login test passed")

    def test_login_invalid(self):
        email = "notworking@email.com"
        password = "notworkingpassword"
        auth = self.firebase.auth()
        with self.assertRaises(Exception):
            auth.sign_in_with_email_and_password(email, password)
        print("Invalid login test passed")

class TestRegistration(unittest.TestCase):
    
    @classmethod
    def setUpClass(self):
        # Initialize Pyrebase app with config
        config = {
            "apiKey": "AIzaSyAHNUwFLMVv91t3ntaXYTCglULRlIg0oJw",
            "authDomain": "pricecompareg28.firebaseapp.com",
            "databaseURL": "https://pricecompareg28-default-rtdb.firebaseio.com/" ,
            "projectId": "pricecompareg28",
            "storageBucket": "pricecompareg28.appspot.com",
            "messagingSenderId": "30273225015",
            "appId": "1:30273225015:web:efd069b091f2c35dea9ab2",
            "measurementId": "G-FFNVTMBVDV",
        }
        self.firebase = pyrebase.initialize_app(config)

    def test_register_with_valid_info(self):
        # Test registration with valid name, email, and password
        name = "Testuse"
        email = "testuse1248@example.com"
        password = "Password123"
        auth = self.firebase.auth()
        user = auth.create_user_with_email_and_password(email, password)
        # self.assertIsNotNone(user)
        self.assertEqual(user['email'], email)
        print("Valid registration test passed")

    def test_register_with_existing_email(self):
        # Test registration with an email that already exists
        name = "Testuse"
        email = "testuse123@example.com"
        password = "Password123"
        auth = self.firebase.auth()
        with self.assertRaises(Exception):
            auth.create_user_with_email_and_password(email, password)
        print("existing registration test passed")
        
class TestSearch(unittest.TestCase):

    def setUp(self):
        app.testing = True
        self.app = app.test_client()

    def test_search_with_valid_query(self):
        data = {'search_box': 'product'}
        response = self.app.post('/search', data=data)
        self.assertEqual(response.status_code, 200)
        print("Valid search test passed")

    def test_search_with_invalid_query(self):
        data = {'search_box': '#product'}
        response = self.app.post('/search', data=data)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Please enter a valid product name', response.data)
        print("Invalid search test passed")

if __name__ == '__main__':
    unittest.main()

# if __name__ == "__main__":
    # suite = unittest.TestLoader().loadTestsFromTestCase(TestRegister)
    # unittest.TextTestRunner(verbosity=2).run(suite)
    # unittest.main()

