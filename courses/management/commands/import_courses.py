'''
courseloader.py
Upload courses to a database from a csv file
Authors: Matthew Eagleman, Google AI
Date Created: 10/26/2026
'''
import pandas as pd
from django.core.management.base import BaseCommand
from courses.models import Course

class Command(BaseCommand): #Makes it so that you can call it as a command using manage.py
    help = 'Imports course data from an Excel file into the database.'

    def add_arguments(self, parser):
        parser.add_argument('excel_file', type=str, help='The path to the Excel file')

    def handle(self, *args, **kwargs):
        file_path = kwargs['excel_file'] #Gets the file path from the terminal
        
        try:
            # Read the Excel file into a pandas DataFrame
            df = pd.read_excel(file_path)
            
            # Use bulk_create for efficient mass insertion
            courses_to_create = []
            
            for _, row in df.iterrows(): # Iterates through each row of the excel file
                course = Course( # Creates a course object for each row, and populates it with the appropriat info from the columns
                    subject=row['Course'],
                    course_number=int(row['Number']),
                    registrar_course_number=int(row['Course nbr']),
                    title=row['Course title'],
                    topic=row['Course topic'],
                    class_number=int(row['Class nbr']),
                    section_number=int(row['Sec. nbr']),
                    credits_min=int(row['Min Hrs']),
                    credits_max=int(row['Max Hrs']),
                    seats_available=int(row['Seats avl']),
                    total_enrolled=int(row['Total enrl']),
                    enroll_cap=int(row['Enroll cap']),
                    type=row['Component'],
                    consent=row['Consent'],
                    enrollable=row['Enrollable'],
                    instructor=row['Instructor'],
                    start_time=row['Start'],
                    end_time=row['End'],
                    days=row['Meeting days'],
                    begin_date=row['Begin date'],
                    end_date=row['End date'],
                    location=row['Location'],
                    room=row['Room'],
                    uploaded_by_user_id=0,
                    is_public=True,
                )
                print(course) # prints the course its adding. we can get rid of this, but i kinda like seeing everything being added
                courses_to_create.append(course)
            Course.objects.bulk_create(courses_to_create) #Adds courses to the database in one, optimized query
            self.stdout.write(self.style.SUCCESS(f'Successfully imported {len(courses_to_create)} courses.'))
        # Catching errors
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'File not found at: {file_path}'))
        except KeyError as e:
            self.stdout.write(self.style.ERROR(f'Missing column in Excel file: {e}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'An unexpected error occurred: {e}'))