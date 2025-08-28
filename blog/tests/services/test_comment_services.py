from django.test.testcases import TestCase

from blog.models import Comment,Post,Category
from users.models import User
from blog.services import comment_create

#To Run: python manage.py test blog.tests.services.test_comment_services.CommentCreateServiceTest
class CommentCreateServiceTest(TestCase):

    def setUp(self):

        self.comment_data = {'title':'new comment title', 'text':'new comment text'}
        self.category = Category.objects.create(name='test name', description='test post comment create service')
        self.user = User.objects.create_user(username='commenter', email='commenter@test.com', password='password')
        self.post_data = {'title':'test title', 'body':'test body'}

        self.post = Post.objects.create(
            category = self.category, 
            user = self.user,
            title = self.post_data['title'],
            body = self.post_data['body'],
            status = 'drf',
        )
        

    def test_service_returns_comment_model_instance(self):
       
        comment = comment_create(user=self.user, data=self.comment_data, post=self.post)

        self.assertIsInstance(comment, Comment)


    def test_service_sets_fields_correctly(self):   

        comment = comment_create(user=self.user, data=self.comment_data, post=self.post)

        self.assertEqual(comment.title, 'new comment title')
        self.assertEqual(comment.text, 'new comment text')
        self.assertEqual(comment.post, self.post)

        
    def test_service_added_new_comment_to_db(self):

        self.assertEqual(Comment.objects.count(), 0)
        comment_create(user=self.user, data=self.comment_data, post=self.post)

        self.assertEqual(Comment.objects.count(), 1)


    def test_service_assigned_user_to_comment(self):


        comment = comment_create(user=self.user, data=self.comment_data, post=self.post)

        self.assertIs(comment.user, self.user)
        self.assertEqual(comment.user.username, self.user.username)


    def test_service_allows_different_users_for_same_post(self):

        another_user = User.objects.create_user(username='anotheruser', email='anotheruser@anotheruser.com', password='password')   
        comment1 = comment_create(user=self.user, data=self.comment_data, post=self.post)
        comment2 = comment_create(user=another_user, data=self.comment_data, post=self.post)

        self.assertNotEqual(comment1.user, comment2.user)
        self.assertEqual(comment1.post, comment2.post)


    def test_service_returns_same_object_as_db(self):

        comment_created_by_service = comment_create(user=self.user, data=self.comment_data, post=self.post)
        comment_from_db = Comment.objects.get(pk=comment_created_by_service.pk)

        self.assertEqual(comment_created_by_service.title, comment_from_db.title)
        self.assertEqual(comment_created_by_service.text, comment_from_db.text)
        self.assertEqual(comment_created_by_service.pk, comment_from_db.pk)


    def test_service_sets_default_value_correctly(self):

        comment = comment_create(user=self.user, data=self.comment_data, post=self.post)

        self.assertEqual(comment.status, 'w')


    def test_service_allows_same_user_to_comment_for_different_posts(self):
        
        post1 = self.post
        post2 = Post.objects.create(
            category = self.category, 
            user = self.user,
            title = self.post_data['title'],
            body = self.post_data['body'],
            status = 'drf',
        )
      

        comment1 = comment_create(user=self.user, data=self.comment_data, post=post1)
        comment2 = comment_create(user=self.user, data=self.comment_data, post=post2)

        self.assertNotEqual(post1.pk, post2.pk)
        self.assertEqual(post1.user, post2.user)
        self.assertNotEqual(comment1.post, comment2.post)
