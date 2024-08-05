from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand


class Command(BaseCommand):
    help = 'Добавление пользователя в группу модераторов'

    # Группы и разрешения
    my_groups = {
        'moderator_mail': [
            'client.view_client_list',
            'mailer.view_mailingmessage',
            'mailer.change_mailingsettings',
            'mailer.view_mailingsettings',
            'users.change_user',
            'users.view_user',
        ],
        'moderator_blog': [
            'blog.view_post',
            'blog.change_post',
            'blog.delete_post',
            'blog.add_post',
        ]
    }

    def handle(self, *args, **options):

        # Создаем группы
        user_input = input('Создать группы [Y/n]:\n').strip().lower()
        if user_input == 'y' or user_input == '':
            self.create_groups(self.my_groups)
            self.stdout.write(self.style.SUCCESS(f'Созданы группы: {", ".join(self.my_groups.keys())}'))

        # Выбираем пользователя
        user = None
        while not user:
            try:
                user_input = int(input('Введите pk пользователя:\n').strip())
                user = self.get_user(user_input)
                if user:
                    self.print_user(user)
                else:
                    self.stdout.write(self.style.ERROR('Пользователь не найден'))
            except ValueError:
                self.stdout.write(self.style.ERROR('Некорректный ввод, введите число'))

        # Выбираем группу
        all_groups = list(Group.objects.all())
        for i, group in enumerate(all_groups):
            self.stdout.write(f'{i}: {group.name}')

        group = None
        while not group:
            try:
                user_input = int(input('Выберите группу для пользователя:\n').strip())
                group = self.get_group(all_groups, user_input)
                group.user_set.add(user)
                self.stdout.write(self.style.SUCCESS(f'Пользователь {user} добавлен в группу {group}'))
            except ValueError:
                self.stdout.write(self.style.ERROR('Некорректный ввод, введите число'))
            except IndexError:
                self.stdout.write(self.style.ERROR('Выберите правильный индекс группы'))

    @staticmethod
    def create_groups(groups: dict) -> None:
        """ Создаем группы и привязываем разрешения к ним """
        for group_name, permissions in groups.items():
            group, _ = Group.objects.get_or_create(name=group_name)
            for perm in permissions:
                app_label, codename = perm.split('.')
                permission, created = Permission.objects.get_or_create(codename=codename, content_type__app_label=app_label)
                if created:
                    print(f'Создано разрешение: {codename}')
                group.permissions.add(permission)
            group.save()

    @staticmethod
    def get_user(user_id: int):
        """ Получаем пользователя по id """
        user_model = get_user_model()
        try:
            return user_model.objects.get(pk=user_id)
        except user_model.DoesNotExist:
            return None

    @staticmethod
    def print_user(user) -> None:
        """ Выводим информацию о пользователе """
        print(f'Пользователь выбран:\npk: {user.pk} email: {user.email} username: {user.username}')

    @staticmethod
    def get_group(groups, index: int):
        """ Получаем группу по индексу """
        if index >= len(groups) or index < 0:
            raise IndexError('Неверный индекс группы')
        return groups[index]