from ..forms import PostForm
from ..models import Post
from django.test import Client, TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


User = get_user_model()


class PostCreateEditFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовый пост ожидает редактирования',
        )
        # Создаем форму, если нужна проверка атрибутов
        cls.form = PostForm()

    def setUp(self):
        # Создаем авторизованный клиент
        self.authorized_client = Client()
        # Авторизуем пользователя
        self.authorized_client.force_login(PostCreateEditFormTests.user)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        # Подсчитаем количество записей в Post
        posts_count = Post.objects.count()
        form_data = {
            'text': 'Тестовый текст',
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('posts:post_create'),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse(
            'posts:profile', args=[PostCreateEditFormTests.user.username]))
        # Проверяем, увеличилось ли число постов
        self.assertEqual(Post.objects.count(), posts_count + 1)

    def test_edit_post(self):
        """Валидная форма редактирует запись в Post."""
        form_data = {
            'text': 'Тестовый пост дождался редактирования',
        }
        # Отправляем POST-запрос
        response = self.authorized_client.post(
            reverse('posts:post_edit', args=[PostCreateEditFormTests.post.id]),
            data=form_data,
            follow=True
        )
        # Проверяем, сработал ли редирект
        self.assertRedirects(response, reverse(
            'posts:post_detail', args=[PostCreateEditFormTests.post.id]))
        # Проверяем, изменился ли пост
        self.assertEqual(
            Post.objects.get(pk=PostCreateEditFormTests.post.pk).text,
            form_data['text']
        )

    def test_create_user(self):
        """Валидная форма создает запись нового пользователя."""
        # Создаем неавторизованный клиент
        guest_client = Client()
        # Подсчитаем количество записей в User
        users_count = User.objects.count()
        form_data = {
            'username': 'test_username',
            'password1': 'test_password',
            'password2': 'test_password',
        }
        # Отправляем POST-запрос
        guest_client.post(
            reverse('users:signup'),
            data=form_data,
            follow=True
        )
        # Проверяем, увеличилось ли число постов
        self.assertEqual(User.objects.count(), users_count + 1)
