from django.core.management.base import BaseCommand
from django.contrib.auth.models import User


class Command(BaseCommand):
    help = "Create demo users"

    def handle(self, *args, **kwargs):

        # ADMIN
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin", email="admin@example.com", password="admin"
            )

        # USER
        if not User.objects.filter(username="user").exists():
            user = User.objects.create_user(username="user", password="user123")

            user.userprofile.role = "USER"
            user.userprofile.save()

        # FOOD CRITIC
        if not User.objects.filter(username="critic").exists():
            critic = User.objects.create_user(username="critic", password="critic123")

            critic.userprofile.role = "CRITIC"
            critic.userprofile.save()

        # RESTAURANT OWNER
        if not User.objects.filter(username="owner").exists():
            owner = User.objects.create_user(username="owner", password="owner123")

            owner.userprofile.role = "RESTAURANT_OWNER"
            owner.userprofile.save()

        self.stdout.write(self.style.SUCCESS("Demo users created successfully!"))
