from django.test import TestCase
from .models import Post, Profile, Comment
# Create your tests here.

class CommentTestClass(TestCase):
    '''
        Set up method
    '''
    def setUp(self):
        self.great= Comment(name='Great')

    def tearDown(self):
        Comment.objects.all().delete()

    # Testing instance
    def test_instance(self):
        self.assertTrue(isinstance(self.great, Comment))

    def test_update_method(self):
        self.great.update_comment(name='Great')
        self.assertTrue(self.great.name, 'Wow')

    def test_delete_method(self):
        self.great.delete_comment()
        comments = Comment.objects.all()
        self.assertTrue(len(comments)==0)

class PostTestClass(TestCase):
    '''
        Set up
    '''

    def setUp(self):
        self.great= Comment(name='Great')
        self.great.save_comment()

        self.new_image= Image(image_name='Bay pizza', image_description='Tasty pizzas are the best', image_location=self.london, image_category=self.food)
        self.new_image.save_image()

    def tearDown(self):
        Location.objects.all().delete()
        Category.objects.all().delete()
        Image.objects.all().delete()

