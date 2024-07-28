# webapp/user/models.py
from django.db import models
import uuid
import time
import logging
from django_rest_passwordreset.signals import reset_password_token_created
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.contrib.auth.models import Group, Permission
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models.signals import pre_save
from utils.common.generators import generate_random_code
from django.conf import settings
from utils.common.generators import ChoiceMenu
from utils.models import CommonFields

logger = logging.getLogger("django")

class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, email=None, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        if not mobile_number:
            raise ValueError("The Mobile Number field must be set")

        email = self.normalize_email(email)
        user = self.model(email=email, mobile_number=mobile_number, **extra_fields)
        user.username = generate_random_code()
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email=email, mobile_number=mobile_number, password=password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True, help_text='Enter a valid email address.')
    username = models.CharField(max_length=30, unique=True, verbose_name="Username", help_text='Auto-generated username')
    mobile_number = models.CharField(max_length=15, unique=True, null=True, blank=True, verbose_name="Mobile number")

    designation = models.CharField(max_length=100, null=True, blank=True, choices=ChoiceMenu.DESIGNATION)
    user_scope = models.CharField(max_length=20, null=True, choices=ChoiceMenu.USER_SCOPES, default="6")
    email_verified = models.BooleanField(default=False)  # Check field for verify user email
    mobile_verified = models.BooleanField(default=False)  # Check  field for verify user Mobile number
    referred_by = models.CharField(max_length=50, null=True, blank=True)

    # Django fields
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    groups = models.ManyToManyField(Group, blank=True, related_name="custom_users_groups")
    user_permissions = models.ManyToManyField(Permission, blank=True, related_name="custom_users_permissions")

    uuid = models.UUIDField(default=uuid.uuid4, editable=False)  # Common UUID field for all models with autogenerate
    status = models.BooleanField(default=True)  # Common Status field for check active or disabled status of object
    is_deleted = models.BooleanField(default=False)  # Soft delete field
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    created_by = models.CharField(max_length=40, null=True, blank=True)  # Store created user UUID
    updated_by = models.CharField(max_length=40, null=True, blank=True)  # Store Updated user UUID

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'mobile_number']

    def __str__(self):
        return self.username

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}" if self.last_name else self.first_name

    def get_user_scope_display(self):
        return dict(ChoiceMenu.USER_SCOPES).get(self.user_scope, 'Unknown')

    def wallet_balance(self):
        deposits = self.wallet.filter(txn_type='CR').aggregate(total_deposits=models.Sum('points'))[
                       'total_deposits'] or 0
        withdrawals = self.wallet.filter(txn_type='DR').aggregate(total_withdrawals=models.Sum('points'))[
                          'total_withdrawals'] or 0
        balance = deposits - withdrawals
        user_balance = float(balance) if balance is not None else 0.0
        return user_balance

    class Meta:
        verbose_name = "CustomUser"  # Singular name
        verbose_name_plural = "CustomUsers"  # Plural name


class Notifications(CommonFields):
    msg_id = models.CharField(max_length=40, null=True, blank=True)
    date = models.DateField(null=True, auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name="notifications")
    title = models.CharField(max_length=200, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    is_viewed = models.BooleanField(default=False, blank=True)
    data = models.JSONField(null=True, blank=True)
    logs = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Notification {self.pk}"


class Wallet(CommonFields):
    wlt_types = (("CR", "Credit"), ("DR", "Debit"))
    # Model fields
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, related_name="wallet")
    points = models.FloatField(default=0.00)
    remarks = models.TextField(null=True, blank=True)
    from_user = models.CharField(max_length=120, null=True, blank=True)
    code = models.CharField(max_length=225, null=True, blank=True, unique=True)
    txn_type = models.CharField(max_length=25, null=True, choices=wlt_types)
    txn_id = models.CharField(max_length=225, null=True, blank=True)
    txn_data = models.JSONField(null=True, blank=True)
    logs = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"Wallet - {self.pk}"


# Generate Random codes using Signals

def set_username(sender, instance, **kwargs):
    if not instance.username:
        instance.username = generate_random_code()

pre_save.connect(set_username, sender=CustomUser)


# Function to Update referral Points
def add_referral_pont(obj):
    try:
        referred_user = CustomUser.objects.get(username=obj.referred_by, is_deleted=False)
        if referred_user:
            points = Wallet.objects.create(txn_type="CR", user=referred_user, points=5.0,
                                           from_user=obj.first_name, created_by=str(obj.uuid))
            logger.info(f"add_referral_pont | Added referral points : {points} for user : {referred_user}")
            return True
    except Exception as ex:
        logger.error(f"add_referral_pont | Something went wrong {ex}")
        return None


# Generate Random codes using Signals
@receiver(pre_save, sender=CustomUser)
def add_referral_point(sender, instance, **kwargs):
    try:
        if instance.referred_by:
            add_referral_pont(instance)

    except Exception as ex:
        if not instance.referred_by:
            instance.referred_by = "T001"


# Generate Random codes using Signals
@receiver(pre_save, sender=Wallet)
def wallet_code_gen(sender, instance, **kwargs):
    try:
        if not instance.code:
            instance.code = generate_random_code()

    except Exception as ex:
        if not instance.code:
            instance.code = "ERROR_CODE" + str(time.time_ns())


@receiver(reset_password_token_created)
def handle_password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):
    app_url = get_app_url("public")

    subject = 'Password reset for Temple Address Portal'
    from_email = settings.DEFAULT_FROM_EMAIL
    to_email = reset_password_token.user.email

    context = {
        'token': reset_password_token.key,
        'url': app_url,
        'user': reset_password_token.user.username
    }
    html_content = render_reset_password_email(context)
    text_content = strip_tags(html_content)

    send_email(subject, text_content, html_content, from_email, to_email)


def get_app_url(schema_name):
    if settings.LIVE_MODE:
        return f"{settings.API_URL}" if schema_name == "public" else f"https://{schema_name}.{settings.API_URL}"
    return settings.APP_URL if settings.APP_URL else "http://localhost:3000/password-reset"


def render_reset_password_email(context):
    return render_to_string('user/forgot_password_email_template.html', context)


def send_email(subject, text_content, html_content, from_email, to_email):
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to_email])
    msg.attach_alternative(html_content, "text/html")
    msg.send()
