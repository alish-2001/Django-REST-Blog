from django.test.testcases import TestCase

from blog.services import category_create
from blog.models import Category

#To run: python manage.py test blog.tests.services.test_category_services.CategoryCreateServiceTest
class CategoryCreateServiceTest(TestCase):

    def setUp(self):

        self.data = {'name':'test category name', 'description':"test category description..."}


    def test_category_create_service_returns_category_model_instance(self):

        category = category_create(data=self.data)
        self.assertIsInstance(category, Category)


    def test_categoy_create_service_sets_fields_correctly(self):   

        category = category_create(data=self.data)
        self.assertEqual(category.description, self.data['description'])
        self.assertEqual(category.name, self.data['name'])


    def test_categoy_create_service_added_new_category_to_db(self):

        self.assertEqual(Category.objects.count(), 0)
        category_create(data=self.data)
        self.assertEqual(Category.objects.count(), 1)


    def test_categoy_create_service_sets_fields_correctly(self):   

        category = category_create(data=self.data)
        self.assertEqual(category.name, self.data['name'])
        self.assertEqual(category.description, self.data['description'])


    def test_category_create_service_returns_same_object_as_db(self):

        category_created_by_service = category_create(data=self.data)
        category_from_db = Category.objects.get(pk=category_created_by_service.pk)
        self.assertEqual(category_created_by_service, category_from_db)
