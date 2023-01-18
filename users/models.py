from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.models import BaseUserManager
from django_passwords.fields import PasswordField
from registration.models import RegistrationProfile
from registration.backends.default.views import RegistrationView
from registration import signals

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.utils.crypto import get_random_string
from django.core.mail import send_mail

from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from django.utils.decorators import method_decorator
from django.views.decorators.debug import sensitive_post_parameters
from django.contrib.auth.models import User

class TeamUserManager(BaseUserManager):
    def create_user(self, email, role, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), role=role)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, role, password):
        user = self.create_user(email, role, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
class TeamUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    password = PasswordField()
    role = models.CharField(max_length=20, choices=(('admin', 'Admin'), ('trainer', 'Trainer'), ('captain', 'Captain'), ('player', 'Player')))
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = TeamUserManager
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role']

    def get_short_name(self):
        return self.email

class RandomPasswordAuthenticationForm(AuthenticationForm):
    email = forms.EmailField()

    def save(self, request, user):
        # Generate a random password
        password = get_random_string()

        # Set the user's password
        user.set_password(password)
        user.save()

         # Send the password to the user's email
        subject = 'Your new password'
        message = f'Your new password is {password}. Please change it as soon as possible.'
        #TODO:email for host
        from_email = 'noreply@example.com'
        recipient_list = [user.email]
        send_mail(subject, message, from_email, recipient_list)

        # Log the user in
        return user

class RandomPasswordLoginView(LoginView):
    form_class = RandomPasswordAuthenticationForm
    template_name = 'login.html'

    @method_decorator(sensitive_post_parameters('password'))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def form_invalid(self, form):
        if 'email' in form.errors:
            form.add_error(None, 'Invalid email address')
        elif 'password' in form.errors:
            form.add_error(None, 'Invalid password')
        return super().form_invalid(form)

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = form.get_user()
        if user is None:
            form.add_error(None, 'Invalid email or password')
            return self.form_invalid(form)
        login(self.request, user)
        return super().form_valid(form)

    def create_user(self, email, password):
        # Create a new user with the provided email and password
        user = User.objects.create_user(email=email, password=password)
        return user

class RandomPasswordRegistrationView(RegistrationView):
    form_class = RandomPasswordRegistrationForm
    template_name = 'register.html'

    def register(self, form):
        new_user = RegistrationProfile.objects.create_inactive_user(
            form.cleaned_data['email'],
            form.cleaned_data['password'],
            form.cleaned_data['role'],
            send_email=True
        )
        signals.user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=self.request)
        return new_user

class RandomPasswordLoginView(LoginView):
    form_class = RandomPasswordAuthenticationForm
    template_name = 'login.html'

    def form_valid(self, form):
        email = form.cleaned_data['email']
        password = form.cleaned_data['password']
        user = form.get_user()
        if user is None or not user.is_active:
            form.add_error(None, 'Invalid email or password')
            return self.form_invalid(form)
        login(self.request, user)
        return super().form_valid(form)