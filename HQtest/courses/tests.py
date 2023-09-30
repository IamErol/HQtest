from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient
from .models import Product, ProductAccess, Lesson, LessonView


PRODUCT_URL = reverse('courses:product_access-list')
PRODUCT_STATS_URL = reverse('courses:all_products-list')


def create_user(username='TestUser', password='TestPassword', is_admin=False):
    """Create a new user."""
    if is_admin == True:
        user = User.objects.create(username=username, password=password,
                                   is_staff=True, is_superuser=True)
    else:
        user = User.objects.create(username=username, password=password)
    return user

def product_detail_url(product_id):
    """Get url for detail view."""

    return reverse('courses:product_access-detail', args=[product_id])

def create_prouct(owner, name):
    """Create a new product."""

    return Product.objects.create(owner=owner, name=name)

def create_lesson(products, name, video_link='www.test.com', duration=600):
    """Create a new lesson."""
    lesson = Lesson.objects.create(name=name,
                                   video_link=video_link,
                                   duration_seconds=duration)
    lesson.products.set([products])
    lesson.save()
    return lesson

def create_product_access(user, product):
    """"Add access to a product."""

    return ProductAccess.objects.create(user=user, product=product)

def create_lesson_view(user, lesson, viewed_time_seconds,
                       watched, last_viewed_time):
    """Add lesson view details."""

    return LessonView.objects.create(user=user, lesson=lesson,
                                     viewed_time_seconds=viewed_time_seconds,
                                     watched=watched,
                                     last_viewed_time=last_viewed_time)


class TestUnauthorized(TestCase):
    """Test unauthorized user get requests."""

    def setUp(self):
        self.client = APIClient()

    def test_get_list_of_all_lessons(self):
        """Test unauthorized user get requests for lessons."""

        result = self.client.get(PRODUCT_URL)
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_of_product_lessons(self):
        """Test unauthorized user get requests for specific product lessons."""

        result = self.client.get(product_detail_url(1))
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_required_get_request(self):
        """Test authenticated user without admin permissions get request."""

        self.client = APIClient()
        user = create_user() #Authenticated user, but not admin.
        self.client.force_authenticate(user)
        result = self.client.get(PRODUCT_STATS_URL)
        self.assertEqual(result.status_code, status.HTTP_403_FORBIDDEN)


class TestAuthenticated(TestCase):
    """Test authenticated user get requests."""

    def setUp(self):
        self.user = create_user(is_admin=True)
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def test_get_all_products(self):
        """Test get product with all details."""

        expected_response =  {'id': 1,
                              'name': 'Test Product',
                              'total_lessons_watched': 0,
                              'total_seconds_watched': 10,
                              'total_students_with_access': 2,
                              'percentage_of_purchase': 66.7}

        #Total 3 user in the User table.
        student = create_user(username="testStudent")
        student2 = create_user(username="testStudent2")

        product = create_prouct(owner=self.user, name='Test Product')
        lesson = create_lesson(products=product, name="Test lesson",
                               video_link='www.test.com')

        # 2 students has access to the same product.
        product_access = create_product_access(product=product, user=student)
        product_access = create_product_access(product=product, user=student2)

        lesson_view = create_lesson_view(user=student, lesson=lesson,
                                         viewed_time_seconds=10, watched=False,
                                         last_viewed_time='2023-09-09 00:00:00')


        result = self.client.get(PRODUCT_STATS_URL)
        object = result.data[0]

        self.assertEqual(result.status_code, status.HTTP_200_OK)
        for k, v in expected_response.items():
            print(f'{k}: {v} object[k]{object[k]}')
            self.assertEqual(object[k], v)



