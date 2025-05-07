from django.db import models


# Create your models here.

class Courses(models.Model):
    course_name = models.CharField(max_length=200)
    fee = models.CharField(max_length=200)
    contents = models.TextField()
    duration = models.CharField(max_length=200)
    field = models.CharField(max_length=200, default='software')

    def __str__(self):
        return self.course_name




class Registration(models.Model):
    genderchoices = (("M", "male"),
                     ("F", "Female"),
                     ("O", "Other"))

    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    gender = models.CharField(choices=genderchoices, max_length=100)
    dateofbirth = models.CharField(max_length=200)
    email = models.EmailField(max_length=200)
    phonenumber = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    hobbies = models.CharField(max_length=300)
    proflepicture = models.FileField(upload_to="documents")
    password = models.CharField(max_length=300, default='0000')
    is_verified = models.BooleanField(default=False)
    address = models.TextField(default="")

    def __str__(self):
        return self.firstname + " " + self.lastname


class Opted_course(models.Model):
    coursename = models.CharField(max_length=200)
    courseid = models.ForeignKey(Courses, on_delete=models.CASCADE)
    userid = models.ForeignKey(Registration, on_delete=models.CASCADE)
    joindate = models.CharField(max_length=200)

    def __str__(self):
        return str(self.userid)


class Temp_otp(models.Model):
    userid = models.ForeignKey(Registration, on_delete=models.CASCADE)
    otp = models.IntegerField()

    def __str__(self):
        return str(self.userid)
