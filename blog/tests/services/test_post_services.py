from django.test.testcases import TestCase


from users.models import User
from blog.services import post_create,post_update
from blog.models import Post,Category

class PostCreateServiceTests(TestCase):

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

    def test_post_create_allows_same_user_to_create_multiple_posts(self):
        
        post = post_create(user=self.user, data=self.data)
        post = post_create(user=self.user, data=self.data)
        self.assertEqual(Post.objects.filter(user=self.user).count(), 2)

