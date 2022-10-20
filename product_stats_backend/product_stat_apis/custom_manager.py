from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, age, gender, role, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        :param email: email
        :param password: password
        :param age: age
        :param gender
        :param role: role
        :param extra_fields: extra fields
        :return: user
        """
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(
            email=email, age=age, gender=gender, role=role, **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, age, gender, **extra_fields):
        """
        Creates and saves a user with the given email and password.
        :param email: email
        :param password: password
        :param age: age
        :param gender: gender
        :param extra_fields: extra fields
        :return: user
        """
        return self._create_user(email, password, age, gender, **extra_fields)

    def create_superuser(
        self, email: str, password: str, age: int, gender: str, **extra_fields
    ) -> object:
        """
        Creates and saves a superuser with the given email and password.
        :param email: email
        :param password: password
        :param age: age
        :param gender : gender
        :param extra_fields: extra fields
        :return: superuser
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self._create_user(
            email, password, age, gender, role="Admin", **extra_fields
        )
