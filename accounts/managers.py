from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            auth_provider="email"
            **extra_fields
        )

        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_google_user(self, email, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            authProvider="google",
            **extra_fields
        )

        user.set_password(None)
        user.save(using=self._db)

        return user