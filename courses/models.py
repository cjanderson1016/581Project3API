from django.db import models

# Create your models here.

# Where we define model classes that are used to pull out data from the database and present to the user

# Model of all the data pertaining to a Course
class Course(models.Model):    
    # === Exportable fields from the registrar === #
    
    # identify the course
    subject = models.CharField(max_length=100, blank=True) # the subject abbreviation the course belongs to (ex. EECS) -- can be expanded into its full name based on this abbreviation later if needec -- 2 to 4 chars of letters (can include an "&")
    course_number = models.PositiveIntegerField(max_length=3)  # the course number (ex. 168) -- all fall between 001 and 999 and can be repeated across subjects
    registrar_course_number = models.PositiveIntegerField(max_length=6) # seems to be a 6 digit number identifying the combination of subject and course number -- unsure of its exact use
    title = models.CharField(max_length=100) # title of the course (ex. Programming I) 
    topic = models.CharField(max_length=100, blank=True) # some courses may have a topic (ex. Python) -- distinguishses "Special Topics:" courses (ex. Laser Engineering)
    class_number = models.PositiveIntegerField(max_length=5, unique=True) # unique 5 digit identifier for each class that can be enrolled in (ex. 40523)
    section_number = models.PositiveIntegerField(max_length=4) # 4 digits used to identify the different sections of the same class (ex. "1000" or "1100")
    
    # course attributes
    credits_min = models.PositiveIntegerField(default=0, max_length=1) # minimum number of credit hours (ex. "1")
    credits_max = models.PositiveIntegerField(default=0, max_length=1) # maximum number of credit hours (ex. "5")
    seats_available = models.PositiveIntegerField(default=0, max_length=3) # seats available (up to three digit int)
    total_enrolled = models.PositiveIntegerField(default=0, max_length=3) # total enrolled (up to three digit int)
    enroll_cap = models.PositiveIntegerField(default=0, max_length=3) # enroll cap (up to three digit int)
    # acad carrer -- unsure what this is referencing (it always seems to be UGDL) -- Should we add this field?
    type = models.CharField(max_length=3) # component -- the three letter abbreviation for the "Type" of class (ex. "LEC", "LBN", "DIS", "IND", or "LAB")
    consent = models.CharField(max_length=100) # consent -- the type of consent needed to enroll in the course (ex. "None", "Department", or "Instructor")
    enrollable = models.CharField(max_length=3) # enrollable (ex. "Yes" or "No") -- should we make this a boolean field? -- seems to be "No" for the lectures that require a lab
    instructor = models.CharField(max_length=50, blank=True) # instructor name formatted in "Last, First" (ex. "Davidson, Andrew") -- can be blank, like for some Labs
    start_time = models.CharField(max_length=8) # start time formatted as 00:00 AM/PM (ex. "09:00 AM") -- may also be "APPT"
    end_time = models.CharField(max_length=8, blank=True) # end time formatted as 00:00 AM/PM (ex. "10:50 AM") -- may be blank in the case that start_time is APPT
    days = models.CharField(max_length=11, blank=True)  # string indicating the days the course is offered. Substrings of "SuMTuWThFSa" (most commonly "MWF" or "TuTh") -- blank in the case of APPT
    begin_date = models.CharField(max_length=6) # the day the course begins in the format of MMM-DD (ex. "JAN-20")
    end_date = models.CharField(max_length=6) # the day the course end in the format of MMM-DD (ex. "MAY-15")
    location = models.CharField(max_length=50) # a shortened name for the campus/location where the course is offered (ex. "LAWRENCE" or "EDWARDS")
    room = models.CharField(max_length=50, blank=True) # the name of the room the course takes place in (ex. "EATN 2010") -- contains the abbreviation of the building in the name

    # Optional attributes to add that are exported
    # room_cap = models.PositiveIntegerField(default=0, max_length=3) # the capacity of the room the course is in (up to three digit int)
    # wait cap
    # wait total
    # comb section ID
    # CS Enroll cap
    # CS Enroll total
    # CS Wait Cap
    # CS Wait Total

    # === Fields not exported by the registrar === #

    school = models.CharField(max_length=100, blank=True) # the school the course belongs to (ex. School of Engineering) -- could be derived from subject?
    department = models.CharField(max_length=50, blank=True) # the department (ex. Electrical Engineering & Compoter Science) -- could be derived from subject?
    building = models.CharField(max_length=100, blank=True) # the abbreviation can be extracted from "room" and then expanded

    # Optional course information to add -- these would most likely have to be manually added since they are not exported in the excel
    # KU Core/Core 34 information ("Satisifies")
    # description = models.TextField(blank=True)
    # prerequisites = models.TextField(blank=True)
    # corequisites = models.TextField(blank=True)
    

    def __str__(self):
        return f"{self.subject} {self.course_number} - {self.title}"
