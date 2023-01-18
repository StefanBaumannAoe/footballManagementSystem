from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .custom_manager import TeamUserManager

class TeamUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=20, choices=(('admin', 'Admin'), ('trainer', 'Trainer'), ('captain', 'Captain'), ('player', 'Player')))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = TeamUserManager
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def get_short_name(self):
        return self.email