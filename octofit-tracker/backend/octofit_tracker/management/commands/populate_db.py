from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models


from django.conf import settings
from pymongo import MongoClient

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Очистка коллекций
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client['octofit_db']
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Данные
        users = [
            {"name": "Clark Kent", "email": "superman@dc.com", "team": "dc"},
            {"name": "Bruce Wayne", "email": "batman@dc.com", "team": "dc"},
            {"name": "Diana Prince", "email": "wonderwoman@dc.com", "team": "dc"},
            {"name": "Tony Stark", "email": "ironman@marvel.com", "team": "marvel"},
            {"name": "Steve Rogers", "email": "captain@marvel.com", "team": "marvel"},
            {"name": "Peter Parker", "email": "spiderman@marvel.com", "team": "marvel"},
        ]
        teams = [
            {"name": "marvel", "members": ["Tony Stark", "Steve Rogers", "Peter Parker"]},
            {"name": "dc", "members": ["Clark Kent", "Bruce Wayne", "Diana Prince"]},
        ]
        activities = [
            {"user": "Clark Kent", "activity": "Flight", "duration": 60},
            {"user": "Tony Stark", "activity": "Suit Training", "duration": 45},
        ]
        leaderboard = [
            {"team": "marvel", "points": 300},
            {"team": "dc", "points": 250},
        ]
        workouts = [
            {"name": "Super Strength", "suggested_for": "dc"},
            {"name": "Tech Endurance", "suggested_for": "marvel"},
        ]

        db.users.insert_many(users)
        db.teams.insert_many(teams)
        db.activities.insert_many(activities)
        db.leaderboard.insert_many(leaderboard)
        db.workouts.insert_many(workouts)

        # Индекс уникальности email
        db.users.create_index([("email", 1)], unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data'))
