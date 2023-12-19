from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    name = models.CharField(null=False, max_length=30)
    description = models.CharField(null=False, max_length=100)

    def __str__(self):
        return self.name + " " + self.description

class CarModel(models.Model):
    SEDAN = 'sedan'
    SUV = 'suv'
    WAGON = 'wagon'
    TYPES = [
        (SEDAN, "Sedan"),
        (SUV, "SUV"),
        (WAGON, "WAGON")
    ]
    car_make = models.ForeignKey(CarMake, null=True, on_delete=models.CASCADE)
    name = models.CharField(null=False, max_length=30)
    dealer_id = models.IntegerField(null=False)
    type = models.CharField(null=False, max_length=20, choices=TYPES, default=SEDAN)
    year = models.DateField(null=True)

    def __str__(self):
        return self.car_make + " " + self.name + " " + self.dealer_id + " " + self.type + " " + self.year

# <HINT> Create a plain Python class `CarDealer` to hold dealer data


# <HINT> Create a plain Python class `DealerReview` to hold review data
