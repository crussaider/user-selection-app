from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, username: str, password: str, email: str, role: str, offer: bool = False,
                    first_name: str = "", last_name: str = "", ):
        if not username:
            raise ValueError("User must have username")
        if not email:
            raise ValueError("User must have email address")
        if not role:
            raise ValueError("User must have role")

        user = self.model(
            first_name=first_name,
            last_name=last_name,
            username=username,
            email=self.normalize_email(email),
            role=role,
            offer=offer,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username: str, password: str, email: str, offer: bool = False, first_name: str = "",
                         last_name: str = ""):
        user = self.create_user(first_name=first_name, last_name=last_name, username=username, email=email,
                                role="crm_admin", offer=offer, password=password)
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # Роли пользователя
    ROLE_CHOICES = [
        ("user", "Пользователь"),
        ("manager", "Менеджер"),
        ("crm_admin", "CRM-администратор"),
    ]
    # Связь роль-аватар
    ROLE_AVATARS = {
        "user": "avatars/user.png",
        "manager": "avatars/manager.png",
        "crm_admin": "avatars/crm_admin.png"
    }

    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=50, unique=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    offer = models.BooleanField(default=False)
    avatar = models.ImageField(upload_to="avatars/", )

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def save(self, *args, **kwargs):
        """
        Устанавливает права и аватар в зависимости от роли пользователя, после чего сохраняет пользователя.
        В случае если аватар не стандартный, то не меняет его.
        """
        if self.role in ["user", "manager"]:
            self.is_admin = False
            self.is_active = False
            self.is_staff = False
            self.is_superuser = False

        elif self.role == "crm_admin":
            self.is_admin = True
            self.is_active = True
            self.is_staff = True
            self.is_superuser = True

        if not self.avatar or self.avatar in self.ROLE_AVATARS.values():
            self.avatar = self.ROLE_AVATARS[self.role]
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
