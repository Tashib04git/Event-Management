import os
import django
from faker import Faker
import random
from datetime import date, timedelta

# Set up Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'event_management.settings')
django.setup()

from events.models import Category, Event, Participant


def populate_db():
    fake = Faker()

    # Create Categories
    category_names = ['Conference', 'Workshop', 'Meetup', 'Seminar', 'Hackathon']
    categories = []
    for name in category_names:
        cat, created = Category.objects.get_or_create(
            name=name,
            defaults={'description': fake.sentence()}
        )
        categories.append(cat)
    print(f"Created {len(categories)} categories.")

    # Create Events
    today = date.today()
    events = []
    for _ in range(20):
        offset = random.randint(-30, 60)
        event_date = today + timedelta(days=offset)
        event = Event.objects.create(
            name=fake.catch_phrase(),
            description=fake.paragraph(),
            date=event_date,
            time=f"{random.randint(8,18):02d}:{random.choice(['00','30'])}",
            location=fake.city() + ', ' + fake.country(),
            category=random.choice(categories)
        )
        events.append(event)
    print(f"Created {len(events)} events.")

    # Create Participants
    participants = []
    for _ in range(30):
        try:
            participant = Participant.objects.create(
                name=fake.name(),
                email=fake.unique.email()
            )
            participant.events.set(random.sample(events, random.randint(1, 4)))
            participants.append(participant)
        except Exception:
            pass
    print(f"Created {len(participants)} participants.")
    print("Database populated successfully!")


if __name__ == '__main__':
    populate_db()
