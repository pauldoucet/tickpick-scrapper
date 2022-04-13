from django.db import models


class TestTable(models.Model):
    date = models.TextField(db_column='Date', blank=True, primary_key=True)
    venueid = models.TextField(db_column='VenueID', blank=True, null=True)
    dateevent = models.TextField(db_column='DateEvent', blank=True, null=True)
    quantity = models.TextField(db_column='Quantity', blank=True, null=True)
    price = models.TextField(db_column='Price', blank=True, null=True)

    def __str__(self):
    	return "date=" + self.date + ", price=" + self.price + ", venueid=" + self.venueid

    class Meta:
        db_table = 'test_table'

class TweetTable(models.Model):
    id = models.TextField(db_column='id', blank=True, primary_key=True)

    def __str__(self):
        return self.id

    class Meta:
        db_table = 'tweet_table'