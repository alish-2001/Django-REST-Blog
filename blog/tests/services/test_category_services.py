from django.test.testcases import TestCase

from blog.services import category_create,category_update
from blog.models import Category

#To run: python manage.py test blog.tests.services.test_category_services.CategoryCreateServiceTest
class CategoryCreateServiceTest(TestCase):

    def setUp(self):

        self.data = {'name':'test category name', 'description':"test category description..."}

    def test_service_returns_category_instance(self):

        category = category_create(data=self.data)

        self.assertIsInstance(category, Category)

    def test_service_added_new_category_in_db(self):

        self.assertEqual(Category.objects.count(), 0)

        category_create(data=self.data)

        self.assertEqual(Category.objects.count(), 1)

    def test_service_sets_fields_correctly(self):   

        category = category_create(data=self.data)

        self.assertEqual(category.name, self.data['name'])
        self.assertEqual(category.description, self.data['description'])

    def test_service_returns_same_object_as_db(self):

        category_created_by_service = category_create(data=self.data)
        category_from_db = Category.objects.get(pk=category_created_by_service.pk)

        self.assertEqual(category_created_by_service.pk, category_from_db.pk,)
        self.assertEqual(category_created_by_service.name, category_from_db.name,)
        self.assertEqual(category_created_by_service.description, category_from_db.description)

#python manage.py test blog.tests.services.test_category_services.CategoryUpdateServiceTest
class CategoryUpdateServiceTest(TestCase):

    def setUp(self):
        
        self.category = Category.objects.create(name='category update service name', description='category update service description')

    def test_service_update_fields_correctly(self):

        data_for_update = {'name':'updated name', 'description':'updated description'}
        updated_category = category_update(data=data_for_update, category=self.category)

        self.assertEqual(updated_category.name, 'updated name')
        self.assertEqual(updated_category.description, 'updated description')

    def test_service_returns_same_object_before_after_update(self):
        
        category_obj_before_update = self.category
        data_for_update = {'name':'updated name', 'description':'updated category'}
        updated_category = category_update(data=data_for_update, category=self.category)

        self.assertIs(category_obj_before_update, updated_category)
   
    def test_service_update_changes_(self):

        data_for_update = {'name':'updated name', 'description':'updated description'}
        updated_category = category_update(data=data_for_update, category=self.category)

        refreshed_category = Category.objects.get(pk=updated_category.pk)

        self.assertEqual(refreshed_category.name, 'updated name')
        self.assertEqual(refreshed_category.description, 'updated description')

    def test_service_does_not_create_new_category(self):

        before = Category.objects.count()
        data_for_update = {'name':'updated name', 'description':'updated description',}
        category_update(data=data_for_update, category=self.category)

        self.assertEqual(Category.objects.count(), before)

    def test_service_supports_partial_update(self):

        name_before_update = self.category.name   
        data_for_partial_update = {'description':'ONLY description FIELD CHANGED',}
        category_update(data=data_for_partial_update, category=self.category) 

        self.category.refresh_from_db()

        self.assertEqual(self.category.name, name_before_update)
        self.assertEqual(self.category.description, 'ONLY description FIELD CHANGED')
