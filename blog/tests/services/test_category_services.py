from django.test.testcases import TestCase

from blog.services import category_create,category_update
from blog.models import Category

#To run: python manage.py test blog.tests.services.test_category_services.CategoryCreateServiceTest
class CategoryCreateServiceTest(TestCase):

    def setUp(self):

        self.data = {'name':'test category name', 'description':"test category description..."}

    def test_category_create_service_returns_category_model_instance(self):

        category = category_create(data=self.data)
        self.assertIsInstance(category, Category)

    def test_service_sets_fields_correctly(self):   

        category = category_create(data=self.data)
        self.assertEqual(category.description, self.data['description'])
        self.assertEqual(category.name, self.data['name'])

    def test_service_added_new_category_to_db(self):

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
        self.assertEqual(category_created_by_service, category_from_db)

#python manage.py test blog.tests.services.test_category_services.CategoryUpdateServiceTest
class CategoryUpdateServiceTest(TestCase):

    def setUp(self):
        
        self.category = Category.objects.create(name='category update service name', description='category update service description')

    def test_category_update_service_sets_fields_correctly_right_after_assignment(self):

        data_for_update = {'name':'updated name', 'description':'updated description'}
        updated_category = category_update(data=data_for_update, category=self.category)

        self.assertEqual(updated_category.name, 'updated name')
        self.assertEqual(updated_category.description, 'updated description')

    def test_service_returns_same_object_before_after_update(self):
        
        category_obj_before_update = self.category

        data_for_update = {'name':'updated name', 'description':'updated category'}

        category_update(data=data_for_update, category=self.category)
        self.category.refresh_from_db()

        self.assertEqual(category_obj_before_update, self.category)
   
    def test_service_updates_correctly_after_getting_refreshed_category_from_db(self):

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

    def test_service_only_change_provided_filelds_for_partial_update(self):

        name_before_update = self.category.name   

        data_for_partial_update = {'description':'ONLY description FIELD CHANGED',}

        category_update(data=data_for_partial_update, category=self.category)    

        self.category.refresh_from_db()

        self.assertEqual(self.category.name, name_before_update)
        self.assertEqual(self.category.description, 'ONLY description FIELD CHANGED')
