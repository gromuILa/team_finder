import io
import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.files.base import ContentFile
from PIL import Image, ImageDraw, ImageFont


AVATAR_COLORS = [
    '#4A90D9', '#7B68EE', '#3CB371', '#CD853F', '#20B2AA',
    '#9370DB', '#E67E22', '#16A085', '#8E44AD', '#2980B9',
]


def generate_avatar(letter):
    size = 200
    color = random.choice(AVATAR_COLORS)
    img = Image.new('RGB', (size, size), color=color)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.truetype('arial.ttf', 100)
    except Exception:
        font = ImageFont.load_default()
    text = letter.upper()
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]
    x = (size - w) / 2 - bbox[0]
    y = (size - h) / 2 - bbox[1]
    draw.text((x, y), text, fill='white', font=font)
    buf = io.BytesIO()
    img.save(buf, format='PNG')
    return buf.getvalue()


class UserManager(BaseUserManager):
    def create_user(self, email, name, surname, password=None, **extra):
        if not email:
            raise ValueError('Email is required')
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, surname=surname, **extra)
        user.set_password(password)
        avatar_data = generate_avatar(name[0] if name else 'U')
        user.avatar.save(f'avatar_{email}.png', ContentFile(avatar_data), save=False)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, surname, password=None, **extra):
        extra.setdefault('is_staff', True)
        extra.setdefault('is_superuser', True)
        return self.create_user(email, name, surname, password, **extra)


class Skill(models.Model):
    name = models.CharField(max_length=124, unique=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=124)
    surname = models.CharField(max_length=124)
    avatar = models.ImageField(upload_to='avatars/', blank=True)
    phone = models.CharField(max_length=12, blank=True)
    github_url = models.URLField(blank=True)
    about = models.TextField(max_length=256, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    skills = models.ManyToManyField(Skill, blank=True, related_name='users')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'surname']

    objects = UserManager()

    def __str__(self):
        return f'{self.surname} {self.name}'

    def get_full_name(self):
        return f'{self.name} {self.surname}'
