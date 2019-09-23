from users.models import User

class UserService(object):

    @classmethod
    def check_user_exists(cls,username):
        return User.objects.filter(username=username).exists()

    @classmethod
    def find_by_username(cls,username):
        if not username:
            return None
        if not User.objects.filter(username=username).exists():
            return None
        
        return User.objects.get(username=username)
