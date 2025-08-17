from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.utils import timezone
from ticketing.models import Match, TicketCategory, News, UserProfile
from datetime import timedelta


class Command(BaseCommand):
    help = 'Populate database with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')

        # Create admin user
        if not User.objects.filter(username='admin').exists():
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@borangersfc.com',
                password='admin123'
            )
            self.stdout.write('Created admin user (admin/admin123)')

        # Create ticket categories
        categories = [
            {'name': 'VIP', 'price': 50000, 'description': 'Premium seating with refreshments'},
            {'name': 'Regular', 'price': 15000, 'description': 'Standard stadium seating'},
            {'name': 'Student', 'price': 8000, 'description': 'Discounted tickets for students'},
            {'name': 'Family', 'price': 40000, 'description': 'Family package for 4 people'},
        ]
        
        for cat_data in categories:
            category, created = TicketCategory.objects.get_or_create(
                name=cat_data['name'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created ticket category: {category.name}')

        # Create sample matches
        matches = [
            {
                'home_team': 'Bo Rangers FC',
                'away_team': 'East End Lions',
                'date_time': timezone.now() + timedelta(days=7),
                'venue': 'Bo Stadium',
                'status': 'upcoming'
            },
            {
                'home_team': 'Bo Rangers FC', 
                'away_team': 'Mighty Blackpool',
                'date_time': timezone.now() + timedelta(days=14),
                'venue': 'Bo Stadium',
                'status': 'upcoming'
            },
            {
                'home_team': 'FC Kallon',
                'away_team': 'Bo Rangers FC',
                'date_time': timezone.now() - timedelta(days=7),
                'venue': 'National Stadium',
                'status': 'completed',
                'home_score': 1,
                'away_score': 2
            }
        ]
        
        for match_data in matches:
            match, created = Match.objects.get_or_create(
                home_team=match_data['home_team'],
                away_team=match_data['away_team'],
                date_time=match_data['date_time'],
                defaults=match_data
            )
            if created:
                self.stdout.write(f'Created match: {match}')

        # Create sample news
        admin_user = User.objects.get(username='admin')
        news_articles = [
            {
                'title': 'Bo Rangers FC Prepares for New Season',
                'content': 'The team is gearing up for an exciting new season with new signings and renewed determination.',
                'category': 'club_news',
                'author': admin_user
            },
            {
                'title': 'Victory Against FC Kallon',
                'content': 'Bo Rangers FC secured a brilliant 2-1 victory against FC Kallon in an exciting match.',
                'category': 'match_report',
                'author': admin_user
            }
        ]
        
        for news_data in news_articles:
            news, created = News.objects.get_or_create(
                title=news_data['title'],
                defaults=news_data
            )
            if created:
                self.stdout.write(f'Created news article: {news.title}')

        self.stdout.write(self.style.SUCCESS('Successfully populated sample data!'))
