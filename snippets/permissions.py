from rest_framework import permissions

# 自定义权限类
class IsOwnerOrReadOnly(permissions.BasePermission):
  
    # 只有创建代码片段的用户能够更新或删除代码片段
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.owner == request.user