from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class UserManager(BaseUserManager):
    # 일반 user 생성
    def create_user(self, email, nickname, password):
        if not email:
            raise ValueError('must have user email')
        if not nickname:
            raise ValueError('must have user nickname')
        user = self.model(
            email = self.normalize_email(email),
            nickname = nickname,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # 관리자 user 생성
    def create_superuser(self, email, nickname, password):
        user = self.create_user(
            email,
            password = password,
            nickname = nickname,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(default='', max_length=100, null=False, blank=False, unique=True)
    nickname = models.CharField(default='', max_length=100, null=False, blank=False, unique=True)

    is_active = models.BooleanField(default=True)    
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    
    # 헬퍼 클래스 사용
    objects = UserManager()

    # 사용자의 username field는 email
    USERNAME_FIELD = 'email'
    # 필수로 작성해야 하는 field
    REQUIRED_FIELDS = ['nickname']

    def __str__(self):
        return self.email
