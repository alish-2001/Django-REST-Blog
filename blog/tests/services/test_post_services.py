from django.test.testcases import TestCase

from users.models import User
from blog.services import post_create,post_update
from blog.models import Post,Category

#To Run: python manage.py test blog.tests.services.test_post_services.PostCreateServiceTest
class PostCreateServiceTest(TestCase):

    def setUp(self):

        self.category = Category.objects.create(name='test category', description='test category description')
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='password')
        self.data = {'title':'test post title', 'body':"test post description...",'category':self.category}

    def test_post_create_service_returns_post_model_instance(self):

        post = post_create(user=self.user, data=self.data)
        self.assertIsInstance(post, Post)

    def test_post_create_service_sets_fields_correctly(self):   

        post = post_create(user=self.user, data=self.data)
        self.assertEqual(post.user.username, self.user.username)
        self.assertEqual(post.title, self.data['title'])
        self.assertEqual(post.body, self.data['body'])

    def test_post_create_service_added_new_post_to_db(self):

        self.assertEqual(Post.objects.count(), 0)
        post = post_create(user=self.user, data=self.data)
        self.assertEqual(Post.objects.count(), 1)

    def test_post_create_service_assigned_user_to_post(self):

        post = post_create(user=self.user, data=self.data)
        self.assertEqual(post.user, self.user)

    def test_post_create_service_allows_different_users(self):

        another_user = User.objects.create_user(username='anotheruser', email='anotheruser@anotheruser.com', password='password')   
        post1 = post_create(user=self.user,data=self.data)
        post2 = post_create(user=another_user, data=self.data)
        self.assertNotEqual(post1.user, post2.user)

    def test_post_create_service_returns_same_object_as_db(self):

        post_created_by_service = post_create(user=self.user, data=self.data)
        post_from_db = Post.objects.get(pk=post_created_by_service.pk)
        self.assertEqual(post_created_by_service,post_from_db)

    def test_post_create_service_sets_default_value_correctly(self):

        post = post_create(user=self.user, data=self.data)
        self.assertEqual(post.status, 'drf')

    def test_post_create_service_allows_same_user_to_create_multiple_posts(self):
        
        post = post_create(user=self.user, data=self.data)
        post = post_create(user=self.user, data=self.data)
        self.assertEqual(Post.objects.filter(user=self.user).count(), 2)

#To Run: python manage.py test blog.tests.services.test_post_services.PostServiceUpdateTest
class PostServiceUpdateTest(TestCase):

    def setUp(self):
        
        self.category = Category.objects.create(name='post update service category name', description='post update service category body')
        self.user = User.objects.create_user(username='testuser', email='testuser@test.com', password='password')
        self.data = {'title':'some title', 'body':'post update service title', 'category':self.category}

        self.initial_post = Post.objects.create(
            category = self.category, 
            user = self.user,
            title = self.data['title'],
            body = self.data['body'],
            status = 'drf',
            )

    def test_post_update_service_sets_fields_correctly_right_after_assignment(self):

        category_for_update = Category.objects.create(name='category for update', description='updated category description')
        data_for_update = {'title':'updated title', 'body':'updated body', 'category':category_for_update, 'status':'pub'}
        updated_post = post_update(data=data_for_update, user=self.initial_post.user, post=self.initial_post)

        self.assertEqual(updated_post.title, 'updated title')
        self.assertEqual(updated_post.body, 'updated body')
        self.assertEqual(updated_post.category, category_for_update)
        self.assertEqual(updated_post.status, 'pub')
        self.assertEqual(updated_post.user, self.user)

    def test_post_update_service_returns_same_object_before_after_update(self):
        
        post_obj_before_update = self.initial_post
        
        category_for_update = Category.objects.create(name='category for update', description='updated category description')
        data_for_update = {'title':'updated title', 'body':'updated body', 'category':category_for_update, 'status':'pub'}
        post_update(data=data_for_update, user=self.initial_post.user, post=self.initial_post)

        self.initial_post.refresh_from_db()

        self.assertEqual(post_obj_before_update, self.initial_post)
   
    def test_post_update_service_updates_correctly_after_get_refreshed_post_from_db(self):

        category_for_update = Category.objects.create(name='category for update', description='updated category description')
        data_for_update = {'title':'updated title', 'body':'updated body', 'category':category_for_update, 'status':'pub'}
        updated_post = post_update(data=data_for_update, user=self.initial_post.user, post=self.initial_post)

        refreshed_post = Post.objects.get(pk=updated_post.pk)

        self.assertEqual(refreshed_post.title, 'updated title')
        self.assertEqual(refreshed_post.body, 'updated body')
        self.assertEqual(refreshed_post.category, category_for_update)
        self.assertEqual(refreshed_post.status, 'pub')

    def test_post_update_service_not_create_new_post(self):

        before = Post.objects.count()

        category_for_update = Category.objects.create(name='category for update', description='updated category description')
        data_for_update = {'title':'updated title', 'body':'updated body', 'category':category_for_update, 'status':'pub'}

        post_update(data=data_for_update, user=self.initial_post.user, post=self.initial_post)
        self.assertEqual(Post.objects.count(), before)

    def test_post_update_service_only_change_provided_filelds_for_partial_update(self):

        title_before_update = self.data['title']        
        data_for_partial_update = {'body':'ONLY BODY FIELD CHANGED',}

        post_update(data=data_for_partial_update, user=self.initial_post.user, post=self.initial_post)    

        self.initial_post.refresh_from_db()

        self.assertEqual(self.initial_post.title, title_before_update)
        self.assertEqual(self.initial_post.body, 'ONLY BODY FIELD CHANGED')

    