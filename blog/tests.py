from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse 

from .models import Post


class BlogTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secret"
        )

        cls.post = Post.objects.create(
            title="Un buen título",
            body="Contenido del cuerpo agradable",
            author=cls.user,
        )

    def test_post_model(self):
        self.assertEqual(self.post.title, "Un buen título")
        self.assertEqual(self.post.body, "Contenido del cuerpo agradable")
        self.assertEqual(self.post.author.username, "testuser")
        self.assertEqual(str(self.post), "Un buen título")
        self.assertEqual(self.post.get_absolute_url(), "/post/1/")

    def test_url_exists_at_correct_location_listview(self):  # nuevo
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)

    def test_url_exists_at_correct_location_detailview(self):  # nuevo
        response = self.client.get("/post/1/")
        self.assertEqual(response.status_code, 200)

    def test_post_listview(self):  # nuevo
        response = self.client.get(reverse("home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contenido del cuerpo agradable")
        self.assertTemplateUsed(response, "home.html")

    def test_post_detailview(self):  # nuevo
        response = self.client.get(reverse("post_detail",
          kwargs={"pk": self.post.pk}))
        no_response = self.client.get("/post/100000/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(no_response.status_code, 404)
        self.assertContains(response, "Un buen título")
        self.assertTemplateUsed(response, "post_detail.html")