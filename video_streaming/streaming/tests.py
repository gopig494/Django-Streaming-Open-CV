from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.contrib.auth.models import User
from streaming.models import Video
from streaming.views import delete_video

class ViewTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.video = Video.objects.create(name='Test Video', userid=self.user)

    def test_delete_video_view(self):
        request = self.factory.get('/delete_video/{}/'.format(self.video.id))
        request.user = self.user
        response = delete_video(request, self.video.id)
        self.assertEqual(response.status_code, 302)  # Redirects after deleting video

class VideoListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='testpassword')
        self.video = Video.objects.create(name='Test Video',  video_url='test_video.mp4', userid=self.user)

    def test_video_list_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('video_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.video.name)

class SignUpViewTest(TestCase):
    def test_signup_view(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'streaming/signup.html')

        response = self.client.post(reverse('signup'), {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'testuser@example.com',
            'password': 'testpassword',
            'confirm_password': 'testpassword'
        })
      

class LoginViewTest(TestCase):
    def test_login_view(self):
        User.objects.create_user(username='testuser', password='testpassword')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'streaming/login.html')

        response = self.client.post(reverse('login'), {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })

class LogoutViewTest(TestCase):
    def test_logout_view(self):
        self.client.login(username='testuser', password='testpassword')
        response = self.client.get(reverse('logout'))
   
