from django.core.management.base import BaseCommand
from user_selection.models import User
from django.db.utils import IntegrityError


class Command(BaseCommand):
    help = 'Create users'

    def handle(self, *args, **kwargs):
        users = [
            {'username': 'user', 'email': 'user@gmail.com', 'role': 'user', 'offer': False},
            {'username': 'manager', 'email': 'manager@gmail.com', 'role': 'manager', 'offer': False},
            {'username': 'crm_admin', 'email': 'crm_admin@gmail.com', 'role': 'crm_admin', 'offer': True},
        ]
        password = "test123"

        for user in users:
            try:
                db_user = User.objects.create_user(
                    username=user["username"],
                    email=user['email'],
                    role=user['role'],
                    offer=user['offer'],
                    password=password
                )
                self.stdout.write(self.style.SUCCESS(
                    f'User created. id = {db_user.id}, username = {db_user.username}, password = {password}, role = {db_user.role}.'
                ))
            except IntegrityError:
                self.stdout.write(self.style.ERROR(
                    f'User with username = {user["username"]} or email = {user["email"]} already exists'
                ))
