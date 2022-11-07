import secrets

from django.contrib.auth.models import Group, User
from django.core.mail import send_mail
from rest_framework.serializers import EmailField, ModelSerializer
from rest_framework.validators import UniqueValidator


class RegisterSerializer(ModelSerializer):
    email = EmailField(
        required=True, validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name")
        extra_kwargs = {
            "first_name": {"required": True},
            "last_name": {"required": True},
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        password = secrets.token_urlsafe(16)
        user.set_password(password)

        driver_group = Group.objects.get(name="Driver")
        user.groups.add(driver_group)

        user.save()

        # TODO: Move this to a different thread
        send_mail(
            "Account created for the Shatoru App",
            "Your Shatoru account has been successfully created by the Admin.\n\n"
            "Your login credentials are as stated below:\n"
            f"Username: {user.username}\n"
            f"Password: {password}\n"
            "\nPlease reset your password on your first login.\n",
            "shatoru.umd@gmail.com",
            [user.email],
            fail_silently=False,
        )

        return user
