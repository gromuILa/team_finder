from django.core.management.base import BaseCommand
from users.models import User, Skill
from projects.models import Project


class Command(BaseCommand):
    help = 'Seed initial test data'

    def handle(self, *args, **options):
        skills_data = ['Python', 'Django', 'JavaScript', 'React', 'PostgreSQL', 'Docker', 'CSS', 'Figma']
        skills = {}
        for name in skills_data:
            skill, _ = Skill.objects.get_or_create(name=name)
            skills[name] = skill
        self.stdout.write('Skills created.')

        users_data = [
            {'email': 'admin@example.com', 'name': 'Алексей', 'surname': 'Иванов', 'password': 'admin123', 'is_staff': True, 'is_superuser': True},
            {'email': 'maria@yandex.ru', 'name': 'Мария', 'surname': 'Петрова', 'password': 'password'},
            {'email': 'ivan@example.com', 'name': 'Иван', 'surname': 'Сидоров', 'password': 'password123'},
            {'email': 'anna@example.com', 'name': 'Анна', 'surname': 'Кузнецова', 'password': 'password123'},
        ]

        created_users = []
        for ud in users_data:
            if User.objects.filter(email=ud['email']).exists():
                user = User.objects.get(email=ud['email'])
                self.stdout.write(f'User {ud["email"]} already exists.')
            else:
                is_staff = ud.pop('is_staff', False)
                is_superuser = ud.pop('is_superuser', False)
                password = ud.pop('password')
                user = User.objects.create_user(**ud, password=password)
                user.is_staff = is_staff
                user.is_superuser = is_superuser
                user.about = f'Разработчик, участник TeamFinder. Люблю создавать полезные проекты.'
                user.github_url = 'https://github.com/example'
                user.save()
                self.stdout.write(f'Created user {ud["email"]}.')
            created_users.append(user)

        if len(created_users) >= 2:
            created_users[1].skills.add(skills['Python'], skills['Django'], skills['PostgreSQL'])
        if len(created_users) >= 3:
            created_users[2].skills.add(skills['JavaScript'], skills['React'], skills['CSS'])
        if len(created_users) >= 4:
            created_users[3].skills.add(skills['Figma'], skills['CSS'])

        projects_data = [
            {
                'owner': created_users[1] if len(created_users) > 1 else created_users[0],
                'name': 'TaskTracker Pro',
                'description': 'Веб-приложение для управления задачами с поддержкой Kanban-досок и командной работы.',
                'status': 'open',
            },
            {
                'owner': created_users[2] if len(created_users) > 2 else created_users[0],
                'name': 'OpenRecipes',
                'description': 'Платформа для обмена рецептами с AI-рекомендациями на основе имеющихся ингредиентов.',
                'status': 'open',
            },
            {
                'owner': created_users[3] if len(created_users) > 3 else created_users[0],
                'name': 'FitBuddy',
                'description': 'Приложение для отслеживания тренировок и поиска партнёров для занятий спортом.',
                'status': 'closed',
            },
            {
                'owner': created_users[0],
                'name': 'DevPortfolio',
                'description': 'Генератор портфолио для разработчиков с интеграцией GitHub.',
                'status': 'open',
            },
        ]

        for pd in projects_data:
            if not Project.objects.filter(name=pd['name']).exists():
                project = Project.objects.create(**pd)
                project.participants.add(pd['owner'])
                self.stdout.write(f'Created project: {pd["name"]}')

        self.stdout.write(self.style.SUCCESS('Seed data created successfully!'))
        self.stdout.write('Admin: admin@example.com / admin123')
        self.stdout.write('Test user: maria@yandex.ru / password')
