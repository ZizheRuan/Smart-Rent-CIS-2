from django.db import models

# Create your models here.
class Property(models.Model):
    address = models.CharField(max_length=200)
    house_img = models.URLField(max_length=200)
    loc_rating = models.DecimalField(max_digits=5, decimal_places=1)
    fac_rating = models.DecimalField(max_digits=5,decimal_places=1)
    tran_rating = models.DecimalField(max_digits=5,decimal_places=1)
    comment=models.CharField(max_length=20, blank=True)
    no_bed = models.IntegerField(blank=True)
    no_bath = models.IntegerField(blank=True)
    house_type = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.address



class Agency(models.Model):
    name = models.CharField(max_length=30)
    agent_img = models.URLField(max_length=200)
    company = models.CharField(max_length=20, blank=True)
    company_logo = models.URLField(max_length=200)
    fri_rating = models.DecimalField(max_digits=5,decimal_places=1)
    res_rating = models.DecimalField(max_digits=5,decimal_places=1)
    bond_rating = models.DecimalField(max_digits=5,decimal_places=1)
    comment=models.CharField(max_length=20, blank=True)

    def __str__(self):
        return self.name

class Resource(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE)
    agency = models.ForeignKey(Agency, on_delete=models.CASCADE)
    link = models.URLField(max_length=200)
    price = models.CharField(max_length=20)

    # def __str__(self):
    #     return 'Address: %s. || Agency: %s. || Price: %s.' % (self.property, self.agency, self.price)

