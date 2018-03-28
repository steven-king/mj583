from django.db import models


GENDER_CHOICES=(
    ('male', 'Male'),
    ('female', 'Female'),
)


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Country(models.Model):
    name = models.CharField(max_length=100)
    alpha_code = models.CharField(max_length=3, blank=True, null=True)
    numeric_code = models.CharField(max_length=3, blank=True, null=True)
    lat = models.CharField(max_length=10, blank=True, null=True)
    lng = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def to_json(self):
        return {
            "name": self.name,
            "alpha_code": self.alpha_code,
            "numeric_code": self.numeric_code,
            "lat": self.lat,
            "lng": self.lng,
        }
    



class Person(models.Model):
    name = models.CharField(max_length=100)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    dob = models.DateField()

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class Winner(models.Model):
    person = models.ForeignKey(Person, "CASCADE")
    category = models.ForeignKey(Category, "CASCADE")
    country = models.ForeignKey(Country, "CASCADE")
    year = models.PositiveIntegerField()

    def __str__(self):
        return "{} {} - {} ({})".format(self.person.name, self.category, self.country, self.year)
    
    def to_json(self):
        return {
            "name": self.person.name,
            "gender": self.person.gender,
            "category": self.category.name,
            "country": self.country.to_json(),
            "year": self.year,
        }