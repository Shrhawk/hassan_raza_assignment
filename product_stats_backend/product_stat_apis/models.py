from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from product_stat_apis.custom_manager import UserManager

CHOICES_IN_GENDER = [
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
]

CHOICES_IN_ROLE = [
    ("Admin", "Admin"),
    ("User", "User"),
]


class User(AbstractUser):
    """
    User model for the application with email as the unique identifier instead of username and
    other fields like age.

    """

    username = None
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=50, unique=True)
    age = models.IntegerField()
    gender = models.CharField(max_length=10, choices=CHOICES_IN_GENDER, default="Male")
    country = models.ForeignKey(
        "Country",
        on_delete=models.SET_NULL,
        related_name="country_in_user",
        null=True,
        blank=True,
    )
    city = models.ForeignKey(
        "City",
        on_delete=models.SET_NULL,
        related_name="city_in_user",
        null=True,
        blank=True,
    )
    role = models.CharField(max_length=10, choices=CHOICES_IN_ROLE)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name", "age", "gender"]


class UserSales(models.Model):
    """
    User sales model for the application to store the sales data of the user.
    """

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="user_in_sales"
    )
    sale_date = models.DateField()
    product_name = models.CharField(max_length=100)
    sale_number = models.IntegerField()
    revenue = models.FloatField()


class Country(models.Model):
    """
    Country model for the application to store the country data.
    """

    name = models.CharField(max_length=500)


class City(models.Model):
    """
    City model for the application to store the city data.
    """

    country = models.ForeignKey(
        Country, on_delete=models.CASCADE, related_name="country_in_city"
    )
    name = models.CharField(max_length=500)
