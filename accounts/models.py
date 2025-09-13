from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from django.db.models.signals import post_save  # new
from django.dispatch import receiver  # new
from django.urls import reverse
from django.contrib.auth.models import Permission
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from app.models import Model, SlugModel, UUIDModel


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None
    first_name = None
    last_name = None
    email = models.EmailField(
        _("email address"), unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects: UserManager = UserManager()


class Team(SlugModel):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE, related_name='teams')

    memberships = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        through='Membership',
        through_fields=(
            'team',
            'holder'))

    def get_absolute_url(self):
        return reverse("team_detail", kwargs={'team_slug': self.slug})


class Membership(UUIDModel):
    permissions = models.ManyToManyField(
        Permission,
        verbose_name=_("permissions"),
        blank=True,
    )

    email = models.EmailField(_("Email Address"))

    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE, related_name='invitations')

    class State(models.TextChoices):
        PENDING = "P", _("Pending")
        ACCEPTED = "A", _("Accepted")

    status = models.CharField(
        max_length=1,
        choices=State,
        default=State.PENDING,
    )

    holder = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='memberships')

    team = models.ForeignKey(Team,
                             on_delete=models.CASCADE, related_name='members')

    def get_absolute_url(self):
        return reverse("membership_detail", kwargs={'membership_uuid': self.uuid, 'team_slug': self.team.slug})

    def __str__(self):
        return f"{self.team} | {self.holder}"


class Profile(Model):  # new
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    # add additional fields for Profile

    first_name = models.CharField(max_length=100)

    last_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Profile | {str(self.user)}"


@receiver(post_save, sender=User)  # new
def create_or_update_user_profile(sender, instance, created, **kwargs):
    Profile.objects.get_or_create(user=instance)
