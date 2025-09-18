from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.db import models
from django.db.models.signals import post_save  # new
from django.dispatch import receiver  # new
from django.urls import reverse
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
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
    is_email_verified = models.BooleanField(
        _("verified"),
        default=False,
        help_text=_(
            "Designates whether this user's email has been verified."
        ),
    )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects: UserManager = UserManager()

    def has_perm(self, perm, obj=None):
        # Implement your custom permission logic here
        # For example, check if the user is a superuser or has a specific role
        # if self.is_superuser:
        #     return True
        # # Add other custom checks
        if ' ' in perm:
            try:
                team_slug, model, codename = perm.split()
                membership = self.memberships.get(team__slug=team_slug)  # type: ignore
                permission = membership.permissions.get(
                    codename=codename, content_type__model=model)
                if permission:
                    return True
            except ObjectDoesNotExist:
                return False
            except ValueError:
                return False
        return super().has_perm(perm, obj)


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
    class Meta:
        ordering = ['email']
        unique_together = ('email', 'team')

    groups = models.ManyToManyField(
        Group,
        verbose_name=_("groups"),
        blank=True,
    )

    email = models.EmailField(_("Email Address"))

    invited_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE, related_name='invitations')

    class Status(models.TextChoices):
        PENDING = "P", _("Pending")
        ACCEPTED = "A", _("Accepted")

    status = models.CharField(
        max_length=1,
        choices=Status,
        default=Status.PENDING,
    )

    holder = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE, related_name='memberships', blank=True, null=True)

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


def get_expiry():
    # Calculate a datetime 2 weeks and 3 hours from now
    return timezone.now() + timedelta(hours=12)
