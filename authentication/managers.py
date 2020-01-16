from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, name, username, phone, email, user_type, data, password):
        if not username:
            raise ValueError("Provide a Username!")
        if not phone:
            raise ValueError("Provide a Phone Number!")
        if not email:
            raise ValueError("Provide an Email!")
        if not password:
            raise ValueError("Enter Password!")
        if not data:
            raise ValueError("Provide profile data")
        user = self.model(
            name = name,
            username = username,
            phone = phone,
            user_type = user_type,
            data = data,
            email = self.normalize_email(email)
        )
        user.set_password(password)
        user.save(using=self._db)
        return user