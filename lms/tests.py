from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.files.uploadedfile import SimpleUploadedFile

from lms.models import Course, Lesson, CourseSubscription, CoursePayment

User = get_user_model()


class CourseModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpass123")
        self.course = Course.objects.create(
            name="Python Basics",
            price=100,
            description="Learn Python from scratch",
            owner=self.user,
        )

    def test_course_with_preview(self):
        image = SimpleUploadedFile("preview.jpg", b"file_content", content_type="image/jpeg")
        course = Course.objects.create(
            name="Django Course",
            price=200,
            preview=image,
            owner=self.user,
        )
        self.assertTrue(course.preview.name.startswith("course/preview"))

class CourseSubscriptionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpass123")
        self.course = Course.objects.create(
            name="Python Basics",
            price=100,
            owner=self.user,
        )
        self.subscription = CourseSubscription.objects.create(
            user=self.user,
            course=self.course,
        )

    def test_subscription_creation(self):
        self.assertEqual(self.subscription.user, self.user)
        self.assertEqual(self.subscription.course, self.course)
        self.assertEqual(str(self.subscription), f"{self.user.email} - {self.course.name}")


class CoursePaymentModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(email="test@example.com", password="testpass123")
        self.course = Course.objects.create(
            name="Python Basics",
            price=100,
            owner=self.user,
        )
        self.payment = CoursePayment.objects.create(
            amount=100,
            user=self.user,
            course=self.course,
            session_id="test_session_123",
            link="https://payment.example.com",
        )

    def test_payment_creation(self):
        self.assertEqual(self.payment.amount, 100)
        self.assertEqual(self.payment.user, self.user)
        self.assertEqual(self.payment.course, self.course)
        self.assertEqual(str(self.payment.amount), "100")  # Проверка __str__