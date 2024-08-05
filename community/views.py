from rest_framework import generics
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status
from .permissions import IsAuthorOrReadOnly
from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
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
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

# 게시글 좋아요 기능
class PostLikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id, *args, **kwargs):
        post = Post.objects.get(id=post_id)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            return Response({'message': 'Like removed'}, status=status.HTTP_200_OK)
        else:
            post.likes.add(user)
            return Response({'message': 'Like added'}, status=status.HTTP_200_OK)
        
# 댓글 좋아요 기능
class CommentLikeToggleView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id, *args, **kwargs):
        comment = Comment.objects.get(id=comment_id)
        user = request.user

        if user in comment.likes.all():
            comment.likes.remove(user)
            return Response({'message': 'Like removed'}, status=status.HTTP_200_OK)
        else:
            comment.likes.add(user)
            return Response({'message': 'Like added'}, status=status.HTTP_200_OK)

# 사용자가 작성한 커뮤니티 글 조회
class UserPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 현재 사용자가 작성한 게시글만 필터링
        return Post.objects.filter(author=self.request.user)

# 사용자가 작성한 커뮤니티 댓글 조회
class UserCommentsView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 현재 사용자가 작성한 댓글만 필터링
        return Comment.objects.filter(author=self.request.user)

# 사용자가 좋아요 누른 커뮤니티 게시글 조회
class UserLikedPostsView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # 현재 사용자가 좋아요 누른 게시글만 필터링
        return Post.objects.filter(likes=self.request.user)
