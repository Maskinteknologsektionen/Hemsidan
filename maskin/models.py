from django.db import models
from django.contrib.auth.models import User, Group
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.translation import ugettext_lazy as _
from datetime import date
from django.core.validators import MaxValueValidator, MinValueValidator


class SchoolYearManager(models.Manager):
    def current(self):
        try:
            return self.get(start__lte=date.today(), end__gte=date.today())
        except SchoolYear.DoesNotExist:
            return None


class SchoolYear(models.Model):
    name = models.CharField(verbose_name=_('name'), max_length=30, unique=True)
    member_group = models.OneToOneField(Group, verbose_name=_('Member group'), on_delete=models.CASCADE, null=True)
    start = models.DateField(verbose_name=_('start'), unique=True)
    end = models.DateField(verbose_name=_('end'), unique=True)

    objects=SchoolYearManager()

    def get_member_group(self):
        return self.member_group

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("School year")
        verbose_name_plural = _("School years")


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    member = models.ManyToManyField(SchoolYear, blank=True,  verbose_name=_("Member years"))
    phone = models.CharField(_("Phone number"), max_length=30, blank=True)
    PROGRAM_CHOICES=(
        ("M", _("Mechanical engingering")),
        ("DPU", _("Design and Product Development")),
        ("EMM", _("Energy-Environment-Management")),
        ("MASTER", _("Masterprogram")),
        ("OTHER", _("Other"))
    )
    program = models.CharField(_("Program"), max_length=10, blank=True, choices=PROGRAM_CHOICES)
    start_year = models.IntegerField(_("Start_year"), default=0)
    master = models.CharField(_("Master profile"), max_length=30, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()