from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.exceptions import ValidationError

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

    def clean(self):
        if self.available_from > self.due_date:
            raise ValidationError("'Available from' cannot be after the due date.")
        if self.available_until < self.due_date:
            raise ValidationError("'Available until' cannot be before the due date.")

    @property
    def total_points(self):
        return sum(
            question.points for question in
            list(self.shortanswerquestion_set.all()) +
            list(self.longanswerquestion_set.all()) +
            list(self.multiplechoicequestion_set.all())
        )

    def __str__(self):
        return self.title


class BaseQuestion(models.Model):
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE)
    text = models.TextField()
    points = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)  # Tracks when the question is created
    updated_at = models.DateTimeField(auto_now=True)  # Tracks when the question is last updated

    class Meta:
        abstract = True

    def __str__(self):
        return f"{self.text[:50]} ({self.points} pts)"


class ShortAnswerQuestion(BaseQuestion):
    pass


class LongAnswerQuestion(BaseQuestion):
    pass


class MultipleChoiceQuestion(BaseQuestion):
    def clean(self):
        if self.pk:
            if not self.choices.filter(is_correct=True).exists():
                raise ValidationError("At least one option must be marked correct.")


class Option(models.Model):
    question = models.ForeignKey(
        MultipleChoiceQuestion,
        related_name='choices',
        on_delete=models.CASCADE
    )
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text