from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=50)
    pid = models.CharField(unique=True, max_length=12)
    grade = models.IntegerField(unique=False, null=True)

    #image_url = models.ImageField(max_length=100)
    class Meta(object):
            ordering = ('pid', 'name')

    def __str__(self):
        return U'%s %s' %(self.name, self.pid)


class Course(models.Model):
    name = models.CharField(max_length=50)
    call_number = models.CharField(unique=False, max_length=4)
    instructor = models.CharField(max_length=50)
    description = models.CharField(max_length=200)
    term = models.CharField(max_length=200)
    date = models.DateField()
    #students = models.ForeignKey(Student, null=True, on_delete=models.CASCADE)
    students = models.ManyToManyField(Student)


    class Meta(object):
        verbose_name_plural = "Courses"
        ordering = ('-date', 'name')

    def __str__(self):
        return U'%s %s' %(self.call_number, self.name)

    def save(self, *args, **kwargs):
        self.name = self.name.upper()
        super(Course, self).save(*args, **kwargs)
