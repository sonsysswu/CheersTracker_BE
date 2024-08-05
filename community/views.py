from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['title', 'content', 'category']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

# 게시글 좋아요 기능
class PostLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, post_id, *args, **kwargs):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        is_liked = request.user in post.likes.all()
        likes_count = post.likes.count()

        return Response({'is_liked': is_liked, 'likes_count': likes_count}, status=status.HTTP_200_OK)

    def post(self, request, post_id, *args, **kwargs):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            message = 'Like removed'
        else:
            post.likes.add(user)
            message = 'Like added'

        return Response({'message': message, 'likes_count': post.likes.count()}, status=status.HTTP_200_OK)

# 댓글 좋아요 기능
class CommentLikeToggleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, comment_id, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        is_liked = request.user in comment.likes.all()
        likes_count = comment.likes.count()

        return Response({'is_liked': is_liked, 'likes_count': likes_count}, status=status.HTTP_200_OK)

    def post(self, request, comment_id, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if user in comment.likes.all():
            comment.likes.remove(user)
            message = 'Like removed'
        else:
            comment.likes.add(user)
            message = 'Like added'

        return Response({'message': message, 'likes_count': comment.likes.count()}, status=status.HTTP_200_OK)

# 게시글 좋아요 삭제 기능
class PostUnlikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, post_id, *args, **kwargs):
        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            return Response({'message': 'Like removed', 'likes_count': post.likes.count()}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You have not liked this post yet.'}, status=status.HTTP_400_BAD_REQUEST)

# 댓글 좋아요 삭제 기능
class CommentUnlikeView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, comment_id, *args, **kwargs):
        try:
            comment = Comment.objects.get(id=comment_id)
        except Comment.DoesNotExist:
            return Response({'error': 'Comment not found.'}, status=status.HTTP_404_NOT_FOUND)

        user = request.user

        if user in comment.likes.all():
            comment.likes.remove(user)
            return Response({'message': 'Like removed', 'likes_count': comment.likes.count()}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'You have not liked this comment yet.'}, status=status.HTTP_400_BAD_REQUEST)

# 사용자가 작성한 커뮤니티 글 조회
class UserPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)

# 사용자가 작성한 커뮤니티 댓글 조회
class UserCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Comment.objects.filter(author=self.request.user)

# 사용자가 좋아요 누른 커뮤니티 게시글 조회
class UserLikedPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Post.objects.filter(likes=self.request.user)
