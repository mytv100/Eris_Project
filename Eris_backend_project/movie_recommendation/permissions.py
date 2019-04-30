from rest_framework import permissions


class UserPermission(permissions.BasePermission):

    # after SignUp( if user is authenticated, user can't see the API to which this permission class applies)
    def has_permission(self, request, view):
        if not (request.user.is_authenticated or request.user.is_superuser):
            return True
        else:
            return False


    """
    회원가입 탈퇴 정보변경 같은거 로그인 상태에 따라, request.method의 종류에 따라
    """