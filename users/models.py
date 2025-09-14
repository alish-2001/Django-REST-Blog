from django.utils import timezone
from django.db import models, transaction
from django.contrib.auth.models import AbstractUser,BaseUserManager

class BaseModel(models.Model):
    created_at = models.DateTimeField(db_index=True, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class UserManager(BaseUserManager):

    def create_user(self, email:str, password: str = None):

        if not email: 
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)

        user = self.model(email=email, username=email, is_staff=False)

        if password:
            user.set_password(password)
        
        else:
            raise ValueError("Password must be set")
        

        try:
            with transaction.atomic():
                user.save(using = self._db)

        except:
            raise ValueError("A user with that email/username exists")
        
        return user
    
    def create_superuser(self, email:str, password: str = None,):

        if not email: 
            raise ValueError("Users must have an email address")
        
        email = self.normalize_email(email)

        user = self.model(

            email = email, 
            username = email,
            is_staff = True,
            is_verified = True,
            is_superuser = True,
            role = 'staff',
        )

        if password:
            user.set_password(password)
        
        else:
            raise ValueError("Password must be set")
        
        try:
            with transaction.atomic():
                user.save(using = self._db)

        except:
            raise ValueError("A user with that email/username exists")

        return user

class User(AbstractUser, BaseModel):

    class Role(models.TextChoices):
        NORMAL = "normal", "Normal User"
        AUTHOR = "author", "Author"
        STAFF = "staff", "Staff"
    
    class Gender(models.TextChoices):
        MALE = "M", "Male"
        FEMALE = "F", "Female"

    email = models.EmailField(unique=True, db_index=True)
    gender = models.CharField(choices=Gender, null=True, blank=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    role = models.CharField(max_length=10, choices=Role, default=Role.NORMAL)
    image = models.ImageField(upload_to='users_images/', null=True, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    bio = models.TextField(null=True, blank=True)

    objects = UserManager()

    EMAIL_FIELD = "email"
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

class OTPVerification(BaseModel):

    class VerificationType(models.TextChoices):
        EMAIL = "email", "Email"
        PHONE = "phone", "Phone"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    code = models.CharField(max_length=5)
    expired_at = models.DateTimeField()
    verification_type = models.CharField(max_length=5, choices=VerificationType, default=VerificationType.EMAIL)

    @property
    def is_expired(self):
        return timezone.now() >= self.expired_at
