from django.test import TestCase
from django.test.client import Client
from django.contrib.auth import get_user_model
# Create your tests here.

class UserTest(TestCase):
    User = get_user_model()
    TEST_USERNAME =  "testuser"
    TEST_PASSWORD = "@@uzumymw@@"
    
    def setUp(self):

        user = self.User.objects.create(
            username = self.TEST_USERNAME,
            phone = "9840418556",
            user_type='buyer'
        )
        user.set_password(self.TEST_PASSWORD)
        user.save()
        

    def test_user_created(self):
        self.assertTrue(self.User.objects.filter(username = self.TEST_USERNAME).exists(),
                        "[❌] User creation test failed"
                        )
        print("[✅] User creation test passed")
        
    def test_user_login(self):
        client = Client()
        self.assertTrue(client.login(username=self.TEST_USERNAME,password=self.TEST_PASSWORD),
                        "\n[❌] User login test failed")
        print("\n[✅] User login test passed")






        