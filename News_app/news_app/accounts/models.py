from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from content.models import Publisher
# Create your models here.


class User(AbstractUser):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN', 'Admin'
        READER = 'READER', 'Reader'
        EDITOR = 'EDITOR', 'Editor'
        JOURNALIST = 'JOURNALIST', 'Journalist'

    base_role = Role.ADMIN

    role = models.CharField(max_length=50, choices=Role.choices)
    email = models.EmailField(max_length=254, unique=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)


class ReaderManger(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.READER)


class EditorManger(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.EDITOR)


class JournalistManger(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        results = super().get_queryset(*args, **kwargs)
        return results.filter(role=User.Role.JOURNALIST)


class Reader(User):
    base_role = User.Role.READER
    reader = ReaderManger()

    class Meta:
        proxy = True


class Editor(User):
    base_role = User.Role.EDITOR
    reader = EditorManger()

    class Meta:
        proxy = True


class Journalist(User):
    base_role = User.Role.JOURNALIST
    reader = JournalistManger()

    class Meta:
        proxy = True


class EditorProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=False)
    publishers = models.ManyToManyField(Publisher)

    def __str__(self):
        return self.full_name


@receiver(post_save, sender=Editor)
def create_editor_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'EDITOR':
        EditorProfile.objects.create(user=instance)


class JournalistProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=False)
    publishers = models.ManyToManyField(Publisher)

    def __str__(self):
        return self.full_name


@receiver(post_save, sender=Journalist)
def create_journalist_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'JOURNALIST':
        JournalistProfile.objects.create(user=instance)


class Article(models.Model):
    title = models.CharField(max_length=100, blank=False)
    content = models.TextField(blank=False)
    author = models.ForeignKey(
        JournalistProfile,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, blank=True, null=True)
    thumbnails = models.ImageField(
        upload_to='thumbnails/',
        null=True,
        blank=True,
    )

    def name(self):
        return self.id

    def __str__(self):
        return self.title


class Newsletter(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(JournalistProfile, on_delete=models.CASCADE, blank=True, null=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE, blank=True, null=True)
    articles = models.ManyToManyField(Article)
    editor = models.ForeignKey(EditorProfile, on_delete=models.CASCADE, blank=True, null=True)

    def name(self):
        return self.id

    def __str__(self):
        return self.title


class ReaderProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, blank=False)
    publishers = models.ManyToManyField(Publisher)
    journalists = models.ManyToManyField(JournalistProfile)

    def __str__(self):
        return self.full_name


@receiver(post_save, sender=Reader)
def create_reader_profile(sender, instance, created, **kwargs):
    if created and instance.role == 'READER':
        ReaderProfile.objects.create(user=instance)
