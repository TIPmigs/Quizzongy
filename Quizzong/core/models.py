from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError
from django.urls import reverse

# Create a custom UserManager to manage the user creation
class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            # Generate a unique fallback email
            base_email = "noid@noemail.github"
            email = base_email
            counter = 1
            while self.model.objects.filter(email=email).exists():
                email = f"{counter}{base_email}"
                counter += 1

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True, null=True, blank=True) 
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    github_username = models.CharField(max_length=100, blank=True, null=True)
    github_id = models.CharField(max_length=100, blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']


    def __str__(self):
        return self.username

class Quiz(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    available_from = models.DateTimeField()
    available_until = models.DateTimeField()
    due_date = models.DateTimeField()
    time_limit = models.DurationField()
    
    created_at = models.DateTimeField(auto_now_add=True)  # Tracks when the quiz is created
    updated_at = models.DateTimeField(auto_now=True)  # Tracks when the quiz is last updated

    class Meta():
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"

    def get_absolute_url(self):
        return reverse("quiz_detail", kwargs={"id": self.id})

    def clean(self):
        if self.available_from > self.due_date:
            raise ValidationError("'Available from' cannot be after the due date.")
        if self.available_until < self.due_date:
            raise ValidationError("'Available until' cannot be before the due date.")

    def __str__(self):
        return self.title
    
class Question(models.Model):
    SHORT = 'short'
    LONG = 'long'
    MC_SINGLE = 'mc_single'
    MC_MULTIPLE = 'mc_multiple'

    TYPES = [
        (SHORT, 'Short Answer'),
        (LONG, 'Long Answer'),
        (MC_SINGLE, 'Multiple Choice (Single Answer)'),
        (MC_MULTIPLE, 'Multiple Choice (Multiple Answers)'),
    ]

    quiz = models.ForeignKey(Quiz, related_name="questions", on_delete=models.CASCADE)
    text = models.TextField()
    type = models.CharField(max_length=20, choices=TYPES)
    points = models.PositiveIntegerField()
    order = models.PositiveIntegerField(default=0)

    correct_answer = models.TextField(blank=True, null=True)  # Used only for SHORT/LONG types
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.type in [self.MC_SINGLE, self.MC_MULTIPLE]:
            correct_options = self.options.filter(is_correct=True).count()

            if correct_options == 0:
                raise ValidationError("Multiple Choice questions must have at least one correct option.")

            if self.type == self.MCQ_SINGLE and correct_options > 1:
                raise ValidationError("Single-answer MCQs must have only one correct option.")

        elif self.type in [self.SHORT, self.LONG]:
            if not self.correct_answer:
                raise ValidationError("Short and Long answer questions must have a correct_answer.")

    def __str__(self):
        return f"{self.text[:50]} ({self.get_type_display()})"

class Option(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text
