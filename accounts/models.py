import pytz
from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
from django.conf import settings

from phonenumber_field.modelfields import PhoneNumberField

from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField

from accounts.utils import get_next_id_with_prefix
from accounts.mixins import CreatedAndUpdatedAt


TIMEZONES = tuple(zip(pytz.all_timezones, pytz.all_timezones))


class ClientManager(BaseUserManager):
    def create_user(self, username, phone, first_name, last_name, middle_name, password=None):
        user = self.model(
            username=username,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, phone, first_name, last_name, middle_name, password):
        user = self.create_user(
            username=username,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Client(CreatedAndUpdatedAt, AbstractBaseUser):
    class TypeChoices(models.TextChoices):
        PRIMARY = ('primary', _('Primary'))
        REPEATED = ('repeated', _('Repeated'))
        EXTERNAL = ('external', _('External'))
        INDIRECT = ('indirect', _('Indirect'))

    class GenderChoices(models.TextChoices):
        MALE = ('male', _('Male'))
        FEMALE = ('female', _('Female'))
        UNKNOWN = ('unknown', _('Unknown'))

    username_validator = UnicodeUsernameValidator()

    id = models.BigIntegerField(_('ID'), primary_key=True, unique=True)
    username = models.CharField(
        _('Username'),
        max_length=150,
        unique=True,
        help_text=_('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'),
        validators=[username_validator],
        error_messages={
            'unique': _('A user with that username already exists.'),
        },
    )
    phone = PhoneNumberField(
        _('Phone number'),
        help_text=_('Use this format +33612345678'),
        unique=True
    )
    first_name = models.CharField(_('first name'), max_length=150)
    last_name = models.CharField(_('last name'), max_length=150)
    middle_name = models.CharField(_('Middle name'), max_length=150)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)
    status_changed_at = models.DateTimeField(_('Statis changed at'), null=True, blank=True)
    is_active = models.BooleanField(default=True)
    type = models.CharField(
        _('Type'),
        max_length=50,
        choices=TypeChoices.choices,
        blank=True,
    )
    gender = models.CharField(
        _('Gender'),
        max_length=50,
        choices=GenderChoices.choices,
        default=GenderChoices.UNKNOWN,
    )
    timezone = models.CharField(max_length=50, choices=TIMEZONES, default='UTC')
    is_admin = models.BooleanField(default=False)

    objects = ClientManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone', 'first_name', 'last_name', 'middle_name']

    __last_is_active = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__last_is_active = self.is_active

    class Meta:
        ordering = ('created_at',)
        verbose_name = _('Client')
        verbose_name_plural = _('Clients')

    def __str__(self):
        return self.username

    @property
    def is_staff(self):
        return self.is_admin

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def clean(self):
        super().clean()
        if AdditionalPhone.objects.filter(phone=self.phone).exists():
            raise ValidationError(_('Phone already used'))

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = get_next_id_with_prefix('user', '01')

        if self.is_active != self.__last_is_active:
            self.status_changed_at = timezone.now()

        super().save(*args, **kwargs)


class AdditionalPhone(models.Model):
    phone = PhoneNumberField(_('Phone number'), help_text=_('Use this format +33612345678'), unique=True)
    client = models.ForeignKey(
        Client, verbose_name=_('Client'), related_name='additional_phones', on_delete=models.CASCADE
    )

    def clean(self):
        if Client.objects.filter(phone=self.phone).exists():
            raise ValidationError(_('Phone already used'))

    class Meta:
        verbose_name = _('Additional phone')
        verbose_name_plural = _('Additional phones')

    def __str__(self):
        return str(self.phone)


class AdditionalEmail(models.Model):
    email = models.EmailField(_('Email address'), unique=True)
    client = models.ForeignKey(
        Client, verbose_name=_('Client'), related_name='additional_emails', on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Additional email')
        verbose_name_plural = _('Additional emails')

    def __str__(self):
        return self.email


class Url(models.Model):
    url = models.URLField(_('Site url'), unique=True)

    class Meta:
        verbose_name = _('Url')
        verbose_name_plural = _('Urls')

    def __str__(self):
        return self.url


class SocialNetwork(models.Model):
    client = models.OneToOneField(
        Client, verbose_name=_('Client'), related_name='social_networks', on_delete=models.CASCADE
    )
    vk = models.ManyToManyField(Url, related_name='social_network_vk', verbose_name=_('Vkontakte'), blank=True)
    fb = models.ManyToManyField(Url, related_name='social_network_fb', verbose_name=_('Facebook'), blank=True)
    ok = models.URLField(_('OK'), unique=True, blank=True)
    instagram = models.URLField(_('Instagram'), unique=True, blank=True)
    telegram = models.CharField(_('Telegram'), max_length=20, blank=True)
    whatsapp = PhoneNumberField(_('WhatsApp'), help_text=_('Use this format +33612345678'), blank=True)
    viber = PhoneNumberField(_('Viber'), help_text=_('Use this format +33612345678'), blank=True)

    class Meta:
        verbose_name = _('Social network')
        verbose_name_plural = _('Social networks')

    def __str__(self):
        return self.client.username


class Department(MPTTModel):
    id = models.BigIntegerField(_('ID'), primary_key=True, unique=True)
    name = models.CharField(_('Name'), max_length=100)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    clients = models.ManyToManyField(Client, through='ClientToDepartment')

    class MPTTMeta:
        order_insertion_by = ['name']

    class Meta:
        verbose_name = _('Department')
        verbose_name_plural = _('Departments')

    def __str__(self):
        return self.name

    def clean(self):
        parent_level = getattr(self.parent, self._mptt_meta.level_attr)
        if parent_level + 1 > settings.MAX_TREE_DEPTH_FOR_DEPARTMENT:
            raise ValidationError(_('Maximum level achieved'))

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = get_next_id_with_prefix('department', '03')

        super().save(*args, **kwargs)


class ClientToDepartment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    created_at = models.DateTimeField(_('Created at'), auto_now_add=True)

    class Meta:
        verbose_name = _('Client to department')
        verbose_name_plural = _('Clients to departments')

    def __str__(self):
        return self.client.username


class LegalEntity(CreatedAndUpdatedAt):
    id = models.BigIntegerField(_('ID'), primary_key=True, unique=True)
    full_name = models.CharField(_('Full name'), max_length=1024)
    short_name = models.CharField(_('Short name'), max_length=500)
    inn = models.BigIntegerField(
        _('INN'),
        validators=[
            MaxValueValidator(9999999999),
            MinValueValidator(1000000000)
        ])
    kpp = models.BigIntegerField(
        _('KPP'),
        validators=[
            MaxValueValidator(999999999),
            MinValueValidator(100000000)
        ])
    departments = TreeManyToManyField(Department)

    class Meta:
        verbose_name = _('Legal entity')
        verbose_name_plural = _('Legal entities')

    def __str__(self):
        return self.short_name

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = get_next_id_with_prefix('legal_entity', '02')

        super().save(*args, **kwargs)
