from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from .models import Article, Category

User = get_user_model()


class ArticleModelTests(TestCase):
    """文章模型测试"""

    def setUp(self):
        self.user = User.objects.create_user(username='author', password='test123456')
        self.category = Category.objects.create(name='技术')

    def test_create_article(self):
        article = Article.objects.create(
            title='Test Article',
            content='This is the content.',
            author=self.user,
            category=self.category,
            status='published',
        )
        self.assertEqual(article.title, 'Test Article')
        self.assertEqual(article.author, self.user)
        self.assertEqual(article.view_count, 0)
        self.assertEqual(article.comment_count, 0)
        self.assertFalse(article.is_deleted)
        self.assertEqual(str(article), 'Test Article')

    def test_article_default_status(self):
        article = Article.objects.create(
            title='Draft',
            content='Content',
            author=self.user,
            category=self.category,
        )
        self.assertEqual(article.status, 'draft')

    def test_category_str(self):
        self.assertEqual(str(self.category), '技术')

    def test_category_unique_name(self):
        with self.assertRaises(Exception):
            Category.objects.create(name='技术')


class ArticleAPITests(TestCase):
    """文章API测试"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='author', password='test123456')
        self.user2 = User.objects.create_user(username='other', password='test123456')
        self.admin = User.objects.create_user(username='admin', password='admin123', role='admin')
        self.category = Category.objects.create(name='技术')
        self.category2 = Category.objects.create(name='生活')

    def _create_article(self, title='Test Article', author=None, status='published'):
        return Article.objects.create(
            title=title,
            content='Content of ' + title,
            author=author or self.user,
            category=self.category,
            status=status,
        )

    def test_list_articles_empty(self):
        res = self.client.get('/api/articles/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 0)

    def test_list_articles(self):
        self._create_article('Article 1')
        self._create_article('Article 2')
        res = self.client.get('/api/articles/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 2)

    def test_list_articles_filter_by_category(self):
        self._create_article('Article 1')
        Article.objects.create(title='Article 2', content='Content', author=self.user, category=self.category2, status='published')
        res = self.client.get(f'/api/articles/?category={self.category.id}')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 1)

    def test_list_articles_pagination(self):
        for i in range(15):
            self._create_article(f'Article {i}')
        res = self.client.get('/api/articles/?page=1&page_size=10')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data['results']), 10)
        self.assertEqual(res.data['total_pages'], 2)

    def test_list_articles_excludes_deleted(self):
        article = self._create_article('Visible')
        deleted = self._create_article('Deleted')
        deleted.is_deleted = True
        deleted.save()
        res = self.client.get('/api/articles/')
        self.assertEqual(res.data['count'], 1)

    def test_list_articles_excludes_draft(self):
        self._create_article('Published')
        self._create_article('Draft', status='draft')
        res = self.client.get('/api/articles/')
        self.assertEqual(res.data['count'], 1)

    def test_article_detail(self):
        article = self._create_article('Detail Article')
        res = self.client.get(f'/api/articles/{article.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['title'], 'Detail Article')

    def test_article_detail_not_found(self):
        res = self.client.get('/api/articles/99999/')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_article_detail_increments_view_count(self):
        article = self._create_article('View Article')
        self.client.get(f'/api/articles/{article.id}/')
        article.refresh_from_db()
        self.assertEqual(article.view_count, 1)

    def test_create_article_authenticated(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.post('/api/articles/create/', {
            'title': 'New Article',
            'content': 'New content',
            'category': self.category.id,
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['message'], '文章发布成功')
        self.assertTrue(Article.objects.filter(title='New Article').exists())

    def test_create_article_unauthenticated(self):
        res = self.client.post('/api/articles/create/', {
            'title': 'New',
            'content': 'Content',
            'category': self.category.id,
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_article_empty_title(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.post('/api/articles/create/', {
            'title': '',
            'content': 'Content',
            'category': self.category.id,
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_article_empty_content(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.post('/api/articles/create/', {
            'title': 'Title',
            'content': '',
            'category': self.category.id,
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_article_auto_summary(self):
        self.client.force_authenticate(user=self.user)
        content = 'A' * 300
        res = self.client.post('/api/articles/create/', {
            'title': 'Summary Test',
            'content': content,
            'category': self.category.id,
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        article = Article.objects.get(title='Summary Test')
        self.assertEqual(len(article.summary), 200)

    def test_edit_own_article(self):
        article = self._create_article('Old Title')
        self.client.force_authenticate(user=self.user)
        res = self.client.put(f'/api/articles/{article.id}/edit/', {
            'title': 'New Title',
            'content': 'Updated content',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        article.refresh_from_db()
        self.assertEqual(article.title, 'New Title')

    def test_edit_others_article_forbidden(self):
        article = self._create_article('My Article')
        self.client.force_authenticate(user=self.user2)
        res = self.client.put(f'/api/articles/{article.id}/edit/', {
            'title': 'Hacked',
            'content': 'Bad content',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_edit_any_article(self):
        article = self._create_article('User Article')
        self.client.force_authenticate(user=self.admin)
        res = self.client.put(f'/api/articles/{article.id}/edit/', {
            'title': 'Admin Edited',
            'content': 'Admin content',
        }, format='json')
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_delete_own_article(self):
        article = self._create_article('Delete Me')
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(f'/api/articles/{article.id}/edit/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        article.refresh_from_db()
        self.assertTrue(article.is_deleted)

    def test_delete_others_article_forbidden(self):
        article = self._create_article('Not Yours')
        self.client.force_authenticate(user=self.user2)
        res = self.client.delete(f'/api/articles/{article.id}/edit/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_my_articles(self):
        self._create_article('Mine 1')
        self._create_article('Mine 2')
        Article.objects.create(title='Others', content='C', author=self.user2, category=self.category, status='published')
        self.client.force_authenticate(user=self.user)
        res = self.client.get('/api/articles/my/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 2)

    def test_category_list(self):
        res = self.client.get('/api/categories/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_admin_article_list(self):
        self._create_article('Article 1')
        self._create_article('Article 2')
        self.client.force_authenticate(user=self.admin)
        res = self.client.get('/api/admin/articles/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 2)

    def test_admin_article_list_forbidden(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get('/api/admin/articles/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_delete_article(self):
        article = self._create_article('Admin Delete Test')
        self.client.force_authenticate(user=self.admin)
        res = self.client.delete(f'/api/admin/articles/{article.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        article.refresh_from_db()
        self.assertTrue(article.is_deleted)

    def test_admin_delete_article_forbidden(self):
        article = self._create_article('No Admin')
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(f'/api/admin/articles/{article.id}/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
