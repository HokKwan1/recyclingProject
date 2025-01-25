from django.core.management.base import BaseCommand
from django.conf import settings
from portal.models import *
from homepage.models import *
from datetime import datetime
from django.contrib.auth.models import Group, User
from django.utils.timezone import make_aware

import sqlite3
import os
import csv


class Command(BaseCommand):
    def handle(self, *args, **kwargs):
        resetDatabaseSequences()
        seedPortalRole()
        seedAuthUsers()
        seedRequest()

# Reset the id sequence in table, make sure all the row are starting with id =1


def resetDatabaseSequences():
    print('Reset Database')

    # Open Connection
    conn = sqlite3.connect('db.sqlite3')
    cursor = conn.cursor()

    cursor.execute(
        f'delete from sqlite_sequence where name = "homepage_request"')

    cursor.execute(
        f'delete from sqlite_sequence where name = "portal_role"')

    cursor.execute(
        f'delete from sqlite_sequence where name = "portal_userrole"')

    cursor.execute(
        f'delete from sqlite_sequence where name = "auth_user"')
    
    cursor.execute(
        f'delete from sqlite_sequence where name = "homepage_request"')

    # Commit the above queries and close the connection
    conn.commit()
    cursor.close()
    conn.close()
    print('Reset Database -- COMPLETED')


def seedPortalRole():
    print('Create Role')
    file_path = os.path.join(settings.BASE_DIR, 'portal',
                             'static', 'portal', 'data', 'role.csv')

    with open(file_path, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # skip the header and move the pointer to the next row
        csv_reader.__next__()

        Role.objects.all().delete()

        for row in csv_reader:
            Role.objects.create(role_name=row[1])
    print('Seeding role table -- COMPLETED')


def seedAuthUsers():
    print('Create Users')
    file_path = os.path.join(settings.BASE_DIR, 'portal',
                             'static', 'portal', 'data', 'volunteers.csv')

    with open(file_path, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # skip the header and move the pointer to the next row
        csv_reader.__next__()

        User.objects.all().delete()

        for row in csv_reader:
            last_login = make_aware(
                datetime.strptime(row[2], '%m/%d/%Y %H:%M'))
            date_joined = make_aware(
                datetime.strptime(row[9], '%m/%d/%Y %H:%M'))

            user = User.objects.create(
                password=row[1],
                last_login=last_login,
                is_superuser=(True if row[3] == '1' else False),
                username=row[4],
                last_name=row[5],
                email=row[6],
                is_staff=(True if row[7] == '1' else False),
                is_active=(True if row[8] == '1' else False),
                date_joined=date_joined,
                first_name=row[10]
            )

            UserRole.objects.create(
                user=user, role=Role.objects.get(role_name='Admin' if row[7] == '1' else 'Volunteer'))
    print('Seeding Auth User table -- COMPLETED')


def seedRequest():
    print("Create Requests")
    file_path = os.path.join(settings.BASE_DIR, 'portal',
                             'static', 'portal', 'data', 'requests.csv')

    with open(file_path, encoding="utf8") as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        # skip the header and move the pointer to the next row
        csv_reader.__next__()

        Request.objects.all().delete()

        for row in csv_reader:
            date_created = make_aware(
                datetime.strptime(row[11], '%Y-%m-%d %H:%M:%S')
            )

            date_completed = (
                make_aware(datetime.strptime(row[12], '%Y-%m-%d %H:%M:%S'))
                if row[12].strip() else None
            )

            user = AuthUser.objects.get(id=row[14])

            Request.objects.create(
                first_name=row[1],
                last_name=row[2],
                email=row[3],
                phone=row[4],
                address=row[5],
                city=row[6],
                state=row[7],
                country=row[8],
                postal_code=row[9],
                status=row[10],
                date_created=date_created,
                date_completed=date_completed,
                token=row[13],
                claimed_by=user
            )
    print('Seeding Request table -- COMPLETED')
