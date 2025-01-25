from django.core.management.base import BaseCommand
import csv
from faker import Faker
import random
from datetime import timedelta

fake = Faker()
state = "California"
cities = ["Los Angeles", "San Francisco", "San Diego", "Sacramento", "San Jose"]
statuses = ["pending", "completed"]


class Command(BaseCommand):
    help = "Generate fake recycling request data"

    def handle(self, *args, **kwargs):
        filename = "requests.csv"
        fieldnames = [
            "id", "first_name", "last_name", "email", "phone", "address", "city",
            "state", "country", "postal_code", "status", "date_created",
            "date_completed", "token", "claimed_by"
        ]

        statuses = ["pending", "in_progress", "completed"]
        rows = []

        for i in range(1, 201):
            date_created = fake.date_time_between(start_date="-3M", end_date="now")
            status = random.choice(statuses)
            date_completed = (
                fake.date_time_between(start_date=date_created, end_date=date_created + timedelta(seconds=fake.random_int(min=700, max=999999))).strftime("%Y-%m-%d %H:%M:%S") if status == "completed" else ""
            )
            first_name = fake.first_name()
            last_name = fake.last_name()
            email = f"{first_name.lower()}.{last_name.lower()}@example.com"

            rows.append({
                "id": i,
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "phone": fake.random_int(min=1000000000, max=9999999999),
                "address": fake.street_address(),
                "city": random.choice(cities),
                "state": state,
                "country": "USA",
                "postal_code": fake.postcode(),
                "status": status,
                "date_created": date_created.strftime("%Y-%m-%d %H:%M:%S"),
                "date_completed": date_completed,
                "token": fake.uuid4(),
                "claimed_by": random.randint(2, 23)
            })

        with open(filename, "w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

        self.stdout.write(self.style.SUCCESS(f"CSV file '{filename}' generated successfully."))
