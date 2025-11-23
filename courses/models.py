from django.db import models

# Create your models here.

# Where we define model classes that are used to pull out data from the database and present to the user

# Model of all the data pertaining to a Course
class Course(models.Model):    
    # === Exportable fields from the registrar === #
    
    # muffin note, -- means i added blank = true, ---- means I got rid of blank = true

    # identify the course
    subject = models.CharField(max_length=4) # the subject abbreviation the course belongs to (ex. EECS) -- can be expanded into its full name based on this abbreviation later if needec -- 2 to 4 chars of letters (can include an "&")
    course_number = models.PositiveIntegerField(max_length=3)  #-- the course number (ex. 168) -- all fall between 001 and 999 and can be repeated across subjects
    registrar_course_number = models.PositiveIntegerField(blank=True, null=True) #-- seems to be a 6 digit number identifying the combination of subject and course number -- unsure of its exact use
    title = models.CharField(max_length=100) # title of the course (ex. Programming I) 
    topic = models.CharField(max_length=100, blank=True, null=True) # some courses may have a topic (ex. Python) -- distinguishses "Special Topics:" courses (ex. Laser Engineering)
    class_number = models.PositiveIntegerField(blank=True, null=True) # unique 5 digit identifier for each class that can be enrolled in (ex. 40523)
    section_number = models.PositiveIntegerField(blank=True, null=True) #-- 4 digits used to identify the different sections of the same class (ex. "1000" or "1100")
    
    # course attributes
    credits_min = models.PositiveIntegerField(default=0,blank=True, null=True) #-- minimum number of credit hours (ex. "1")
    credits_max = models.PositiveIntegerField(default=0,blank=True, null=True) #-- maximum number of credit hours (ex. "5")
    seats_available = models.IntegerField(default=0,blank=True, null=True) #-- seats available (up to three digit int) I changed this because some of the available seats register as -1? not sure why -Matthew
    total_enrolled = models.PositiveIntegerField(default=0,blank=True, null=True) #-- total enrolled (up to three digit int)
    enroll_cap = models.PositiveIntegerField(default=0,blank=True, null=True) #-- enroll cap (up to three digit int)
    # acad carrer -- unsure what this is referencing (it always seems to be UGDL) -- Should we add this field?
    type = models.CharField(max_length=3,blank=True, null=True) #-- component -- the three letter abbreviation for the "Type" of class (ex. "LEC", "LBN", "DIS", "IND", or "LAB")
    consent = models.CharField(max_length=100,blank=True, null=True) #-- consent -- the type of consent needed to enroll in the course (ex. "None", "Department", or "Instructor")
    enrollable = models.CharField(max_length=3,blank=True, null=True) #-- enrollable (ex. "Yes" or "No") -- should we make this a boolean field? -- seems to be "No" for the lectures that require a lab
    instructor = models.CharField(max_length=50, blank=True, null=True) # instructor name formatted in "Last, First" (ex. "Davidson, Andrew") -- can be blank, like for some Labs
    start_time = models.CharField(max_length=8) # start time formatted as 00:00 AM/PM (ex. "09:00 AM") -- may also be "APPT"
    end_time = models.CharField(max_length=8) #---- end time formatted as 00:00 AM/PM (ex. "10:50 AM") -- may be blank in the case that start_time is APPT
    days = models.CharField(max_length=11)  #---- string indicating the days the course is offered. Substrings of "SuMTuWThFSa" (most commonly "MWF" or "TuTh") -- blank in the case of APPT
    begin_date = models.CharField(max_length=6,blank=True, null=True) #-- the day the course begins in the format of MMM-DD (ex. "JAN-20")
    end_date = models.CharField(max_length=6,blank=True, null=True) #-- the day the course end in the format of MMM-DD (ex. "MAY-15")
    location = models.CharField(max_length=50,blank=True, null=True) #-- a shortened name for the campus/location where the course is offered (ex. "LAWRENCE" or "EDWARDS")
    room = models.CharField(max_length=50, blank=True, null=True) # the name of the room the course takes place in (ex. "EATN 2010") -- contains the abbreviation of the building in the name
    uploaded_by = models.CharField(max_length=100) #This should be set to "admin" if its a public course, or whatever user uploaded it if it is private.

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
        topic = str(self.topic)
        topic_str = f" {topic}" if topic.lower() != "nan" else ""
        return f"{self.subject} {self.course_number} - {self.title}{topic_str} ({self.class_number})"
        # Ex. EECS 138 - Introduction to Computing: Python (40523)
        # The topic is only displayed when present ('nan' is how an empty excel cell is read by the importing program)

#  ===== After making changes to the models =====

# Create migrations for your model changes
#   python manage.py makemigrations

# Apply the migration to the database
#   python manage.py migrate

# Run the Server Again
#   python manage.py runserver