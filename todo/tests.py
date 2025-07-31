from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from todo.models import Todo
from datetime import date # date 객체를 사용하기 위해 import
from django.utils import timezone # RuntimeWarning 해결을 위해 import

User = get_user_model()


class TodoTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # 테스트에 필요한 사용자 데이터 미리 생성
        cls.user = User.objects.create_user(username='testuser', password='password123')
        cls.superuser = User.objects.create_superuser(username='superuser', password='password123')
        # Todo 객체 생성
        cls.todo = Todo.objects.create(
            user=cls.user,
            title='Test Todo',
            description='This is a test description.',
            start_date='2025-08-01',
            end_date='2025-08-05'
        )

    def test_todo_list_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cbv_todo_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Todo')

    def test_todo_detail_view_auth(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('cbv_todo_info', args=[self.todo.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Todo')

    def test_todo_detail_view_no_auth(self):
        response = self.client.get(reverse('cbv_todo_info', args=[self.todo.id]))
        # 로그인하지 않은 사용자는 로그인 페이지로 리다이렉트
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, f'/accounts/login/?next=/cbv/todo/{self.todo.id}/')

    def test_todo_create_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('cbv_todo_create'), {
            'title': 'New Todo',
            'description': 'New description.',
            'start_date': '2025-08-06',
            'end_date': '2025-08-10'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Todo.objects.filter(title='New Todo').exists())

    def test_todo_update_view(self):
        self.client.login(username='testuser', password='password123')
        response = self.client.post(reverse('cbv_todo_update', args=[self.todo.id]), {
            'title': 'Updated Todo',
            'description': 'Updated description.',
            'start_date': '2025-08-01',
            'end_date': '2025-08-05'
        })
        self.assertEqual(response.status_code, 302)
        self.todo.refresh_from_db()
        self.assertEqual(self.todo.title, 'Updated Todo')

    def test_todo_delete_view_auth(self):
        self.client.login(username='testuser', password='password123')
        # start_date와 end_date를 추가하여 객체 생성
        todo_to_delete = Todo.objects.create(
            user=self.user,
            title='Temp',
            description='Temp',
            start_date=date.today(),  # 오늘 날짜를 사용
            end_date=date.today()
        )
        response = self.client.post(reverse('cbv_todo_delete', args=[todo_to_delete.id]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(id=todo_to_delete.id).exists())

    def test_todo_delete_view_wrong_user(self):
        self.client.login(username='superuser', password='password123')
        # start_date와 end_date를 추가하여 객체 생성
        todo_to_delete = Todo.objects.create(
            user=self.user,
            title='Temp',
            description='Temp',
            start_date=date.today(),  # 오늘 날짜를 사용
            end_date=date.today()
        )
        response = self.client.post(reverse('cbv_todo_delete', args=[todo_to_delete.id]))
        # 슈퍼유저도 삭제 가능하므로 302
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Todo.objects.filter(id=todo_to_delete.id).exists())