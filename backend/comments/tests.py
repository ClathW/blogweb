from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

from articles.models import Article, Category
from .models import Comment

User = get_user_model()


class CommentModelTests(TestCase):
    """评论模型测试"""

    def setUp(self):
        self.user = User.objects.create_user(username='commenter', password='test123456')
        self.category = Category.objects.create(name='技术')
        self.article = Article.objects.create(
            title='Test', content='Content', author=self.user, category=self.category, status='published'
        )

    def test_create_comment(self):
        comment = Comment.objects.create(
            content='Great article!',
            article=self.article,
            user=self.user,
        )
        self.assertEqual(comment.content, 'Great article!')
        self.assertEqual(comment.article, self.article)
        self.assertFalse(comment.is_deleted)
        self.assertIsNone(comment.parent)

    def test_comment_str(self):
        comment = Comment.objects.create(content='Nice!', article=self.article, user=self.user)
        self.assertIn('commenter', str(comment))
        self.assertIn('Nice!', str(comment))

    def test_nested_comment(self):
        parent = Comment.objects.create(content='Parent', article=self.article, user=self.user)
        reply = Comment.objects.create(content='Reply', article=self.article, user=self.user, parent=parent)
        self.assertEqual(reply.parent, parent)
        self.assertEqual(parent.replies.count(), 1)


class CommentAPITests(TestCase):
    """评论API测试"""

    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='commenter', password='test123456')
        self.user2 = User.objects.create_user(username='other', password='test123456')
        self.admin = User.objects.create_user(username='admin', password='admin123', role='admin')
        self.category = Category.objects.create(name='技术')
        self.article = Article.objects.create(
            title='Test Article', content='Content', author=self.user, category=self.category, status='published'
        )

    def test_list_comments_empty(self):
        res = self.client.get(f'/api/articles/{self.article.id}/comments/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 0)

    def test_create_comment_authenticated(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.post(
            f'/api/articles/{self.article.id}/comments/create/',
            {'content': 'Good read!'}, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res.data['message'], '评论发表成功')

    def test_create_comment_unauthenticated(self):
        res = self.client.post(
            f'/api/articles/{self.article.id}/comments/create/',
            {'content': 'Good!'}, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_comment_empty_content(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.post(
            f'/api/articles/{self.article.id}/comments/create/',
            {'content': ''}, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_content_too_long(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.post(
            f'/api/articles/{self.article.id}/comments/create/',
            {'content': 'A' * 1001}, format='json'
        )
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_comment_updates_article_count(self):
        self.client.force_authenticate(user=self.user)
        self.client.post(f'/api/articles/{self.article.id}/comments/create/', {'content': 'C1'}, format='json')
        self.client.post(f'/api/articles/{self.article.id}/comments/create/', {'content': 'C2'}, format='json')
        self.article.refresh_from_db()
        self.assertEqual(self.article.comment_count, 2)

    def test_list_comments(self):
        Comment.objects.create(content='C1', article=self.article, user=self.user)
        Comment.objects.create(content='C2', article=self.article, user=self.user2)
        res = self.client.get(f'/api/articles/{self.article.id}/comments/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)

    def test_list_comments_excludes_deleted(self):
        comment = Comment.objects.create(content='Visible', article=self.article, user=self.user)
        deleted = Comment.objects.create(content='Gone', article=self.article, user=self.user, is_deleted=True)
        res = self.client.get(f'/api/articles/{self.article.id}/comments/')
        self.assertEqual(len(res.data), 1)

    def test_list_comments_excludes_deleted_replies(self):
        parent = Comment.objects.create(content='Parent', article=self.article, user=self.user)
        Comment.objects.create(content='Visible reply', article=self.article, user=self.user, parent=parent)
        Comment.objects.create(
            content='Deleted reply',
            article=self.article,
            user=self.user,
            parent=parent,
            is_deleted=True,
        )
        res = self.client.get(f'/api/articles/{self.article.id}/comments/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data[0]['replies']), 1)
        self.assertEqual(res.data[0]['replies'][0]['content'], 'Visible reply')

    def test_list_comments_excludes_unpublished_article(self):
        draft = Article.objects.create(
            title='Draft',
            content='Content',
            author=self.user,
            category=self.category,
            status='draft',
        )
        res = self.client.get(f'/api/articles/{draft.id}/comments/')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_own_comment(self):
        comment = Comment.objects.create(content='My comment', article=self.article, user=self.user)
        self.client.force_authenticate(user=self.user)
        res = self.client.delete(f'/api/comments/{comment.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertTrue(comment.is_deleted)

    def test_delete_others_comment_forbidden(self):
        comment = Comment.objects.create(content='Not mine', article=self.article, user=self.user)
        self.client.force_authenticate(user=self.user2)
        res = self.client.delete(f'/api/comments/{comment.id}/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_can_delete_any_comment(self):
        comment = Comment.objects.create(content='User comment', article=self.article, user=self.user)
        self.client.force_authenticate(user=self.admin)
        res = self.client.delete(f'/api/comments/{comment.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertTrue(comment.is_deleted)

    def test_delete_comment_updates_article_count(self):
        c1 = Comment.objects.create(content='C1', article=self.article, user=self.user)
        c2 = Comment.objects.create(content='C2', article=self.article, user=self.user)
        self.article.comment_count = 2
        self.article.save()
        self.article.refresh_from_db()
        self.assertEqual(self.article.comment_count, 2)
        self.client.force_authenticate(user=self.user)
        self.client.delete(f'/api/comments/{c2.id}/')
        self.article.refresh_from_db()
        self.assertEqual(self.article.comment_count, 1)

    def test_comment_on_nonexistent_article(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.post('/api/articles/99999/comments/create/', {'content': 'Hi'}, format='json')
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)

    # Admin comment tests
    def test_admin_list_comments(self):
        Comment.objects.create(content='C1', article=self.article, user=self.user)
        Comment.objects.create(content='C2', article=self.article, user=self.user2)
        self.client.force_authenticate(user=self.admin)
        res = self.client.get('/api/admin/comments/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data['count'], 2)

    def test_admin_list_comments_forbidden(self):
        self.client.force_authenticate(user=self.user)
        res = self.client.get('/api/admin/comments/')
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)

    def test_admin_list_comments_rejects_invalid_pagination(self):
        self.client.force_authenticate(user=self.admin)
        res = self.client.get('/api/admin/comments/?page_size=0')
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_admin_delete_comment(self):
        comment = Comment.objects.create(content='Bad comment', article=self.article, user=self.user)
        self.client.force_authenticate(user=self.admin)
        res = self.client.delete(f'/api/admin/comments/{comment.id}/')
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        comment.refresh_from_db()
        self.assertTrue(comment.is_deleted)
