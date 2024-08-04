from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    객체의 작성자만 내용을 수정하거나 삭제할 수 있게 하는 커스텀 권한.
    """
    def has_object_permission(self, request, view, obj):
        # 읽기 권한은 모든 요청에 허용
        if request.method in permissions.SAFE_METHODS:
            return True
        # 쓰기 권한은 오직 작성자에게만 허용
        return obj.author == request.user
