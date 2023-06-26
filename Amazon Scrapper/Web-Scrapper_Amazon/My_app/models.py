from django.db import models
from .scrape import get_link_data

# Create your models here.

class Link(models.Model):
    name = models.CharField(max_length=220, blank=True) 
    url = models.URLField()
    current_price = models.FloatField(blank=True)
    old_price = models.FloatField(default=0)
    price_difference = models.FloatField(default=0)
    update = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def _str_(self):                                # This is used to string representation of that object.
        return str(self.name)

    class Meta:                                     # It indicate that how do we want to order our objects. 
        ordering = ('price_difference', '-created') 

    def save(self, *args, **kwargs):
        name, price = get_link_data(self.url)
        old_price = self.current_price
        if self.current_price:
            if price != old_price:
                diff = price - old_price
                self.price_difference = round(diff, 2)
                self.old_price = old_price
                self.current_price = price
        else:
            self.old_price = 0
            self.price_difference = 0

        self.name = name
        self.current_price = price 

        super().save(*args, **kwargs)
