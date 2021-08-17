from django.db import models
from django.db.models import F
from django.core.validators import MaxValueValidator, MinValueValidator

'''
class City(models.Model):
    name = models.CharField(max_length=2500, unique=True, indexed=True)

class Category(models.Model):
    name = models.CharField(max_length=2500, unique=True, indexed=True)
'''


class Place(models.Model):
    id = models.IntegerField(primary_key=True)
    city = models.CharField(max_length=500, db_index=True)
    region = models.CharField(max_length=500, null=True, blank=True)
    business_names = models.CharField(max_length=1000)
    company_name = models.CharField(max_length=1000)

    rating = models.FloatField(max_length=500, null=True, blank=True)
    review = models.CharField(max_length=500, null=True, blank=True)
    category = models.CharField(max_length=500, null=True, blank=True)
    address = models.CharField(max_length=500, null=True, blank=True)
    latitude = models.FloatField(max_length=500, null=True, blank=True)
    longitude = models.FloatField(max_length=500, null=True, blank=True)
    phone = models.CharField(max_length=500, null=True, blank=True)
    website = models.URLField(max_length=500, null=True, blank=True)
    link_to_menu = models.CharField(max_length=500, null=True, blank=True)
    location = models.CharField(max_length=500, null=True, blank=True)
    critic_reviews = models.CharField(max_length=500, null=True, blank=True)
    nearby = models.CharField(max_length=500, null=True, blank=True)
    from_these_lists = models.CharField(max_length=500, null=True, blank=True)
    reviews_sorting = models.CharField(max_length=500, null=True, blank=True)

    # url list
    product_title = models.TextField(max_length=5000, null=True, blank=True)
    product_url = models.TextField(max_length=5000, null=True, blank=True)
    photos_menu = models.TextField(max_length=5000, null=True, blank=True)
    photos_owner = models.TextField(max_length=5000, null=True, blank=True)
    photos_inside = models.TextField(max_length=5000, null=True, blank=True)

    about = models.TextField(max_length=5000, null=True, blank=True)
    about_details = models.TextField(max_length=5000, null=True, blank=True)
    details = models.TextField(max_length=5000, null=True, blank=True)

    # social
    facebook = models.URLField(max_length=500, null=True, blank=True)
    instagram = models.URLField(max_length=500, null=True, blank=True)
    linkedin = models.URLField(max_length=500, null=True, blank=True)
    twitter = models.URLField(max_length=500, null=True, blank=True)
    youtube = models.URLField(max_length=500, null=True, blank=True)
    pinterest = models.URLField(max_length=500, null=True, blank=True)

    service_options = models.TextField(max_length=5000, null=True, blank=True)
    offerings = models.TextField(max_length=5000, null=True, blank=True)
    dining_options = models.TextField(max_length=5000, null=True, blank=True)
    amenities = models.TextField(max_length=5000, null=True, blank=True)
    atmosphere = models.TextField(max_length=5000, null=True, blank=True)
    crowd = models.TextField(max_length=5000, null=True, blank=True)
    accessibility = models.TextField(max_length=5000, null=True, blank=True)
    planning = models.TextField(max_length=5000, null=True, blank=True)
    payments = models.TextField(max_length=5000, null=True, blank=True)

    price = models.CharField(max_length=500, null=True, blank=True, db_index=True)
    services = models.TextField(max_length=5000, null=True, blank=True)

    def get_photos_inside(self):
        return str(self.photos_inside).replace(']', '').replace('[', '').replace('"', '').replace("'", '').split(',')

    def get_photos_menu(self):
        return str(self.photos_menu).replace(']', '').replace('[', '').replace('"', '').replace("'", '').split(',')

    def get_photos_owner(self):
        return str(self.photos_owner).replace(']', '').replace('[', '').replace('"', '').replace("'", '').split(',')

    def get_product_url(self):
        return str(self.product_url).replace(']', '').replace('[', '').replace('"', '').replace("'", '').split(',')

    def get_product_title(self):
        return str(self.product_title).replace(']', '').replace('[', '').replace('"', '').replace("'", '').split(',')

    def get_product_slider(self):
        images = str(self.product_url).replace(']', '').replace('[', '').replace('"', '').replace("'", '').split(',')
        titles = str(self.product_title).replace(']', '').replace('[', '').replace('"', '').replace("'", '').split(',')
        sliders = []
        for i, v in enumerate(images):
            try:
                val = titles[i]
            except IndexError:
                continue
            sliders.append({'image': v, 'title': titles[i]})
        return sliders

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return '[' + str(self.id) + '] ' + self.company_name


class Open(models.Model):
    id = models.AutoField(primary_key=True)
    day = models.CharField(max_length=500)
    open_interval = models.CharField(max_length=500)
    place = models.ForeignKey(Place, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Open hours"
        # unique_together = ('day', 'open_interval', 'place')

    def __str__(self):
        id = str(self.place)
        if id == 'None': id = '[None]'
        return id + ' | ' + self.day + " | " + self.open_interval


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    reviewer_name = models.CharField(max_length=500)
    reviewer_profile_link = models.URLField(max_length=500)
    rating_stars = models.FloatField(validators=[MinValueValidator(1.0), MaxValueValidator(5.0)])
    review_date = models.CharField(max_length=500, null=True, blank=True)
    review_text = models.TextField(max_length=5000, null=True, blank=True)
    review_pictures = models.TextField(max_length=5000, null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='+', null=True, blank=True)

    def get_images(self):
        if self.review_pictures:
            st = self.review_pictures.split(',')
            if len(st[0]) == 0:
                return None
            return st
        return None

    class Meta:
        # unique_together = ('reviewer_name', 'reviewer_profile_link', 'place', 'review_text')
        pass

    def __str__(self):
        id = str(self.place)
        if id == 'None': id = '[None] '
        return id + self.reviewer_name + " | " + str(self.rating_stars)


class Highlights(models.Model):
    id = models.AutoField(primary_key=True)
    listing_name = models.CharField(max_length=500)
    food_name = models.CharField(max_length=500, null=True, blank=True)
    product_picture = models.TextField(max_length=5000, null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='+')

    class Meta:
        verbose_name_plural = "Highlights"
        # unique_together = ('id', 'food_name')

    def __str__(self):
        id = str(self.place)
        if id == 'None': id = '[None] '
        return id + str(self.food_name) + " | " + str(self.listing_name)


class Question(models.Model):
    id = models.AutoField(primary_key=True)
    asked_by = models.CharField(max_length=500)
    answered_by = models.CharField(max_length=500, null=True, blank=True)
    asked_by_profile = models.URLField(max_length=500, null=True, blank=True)
    answered_by_profile = models.TextField(max_length=5000, null=True, blank=True)
    question_date = models.CharField(max_length=500, null=True, blank=True)
    question = models.TextField(max_length=5000, null=True, blank=True)
    answer = models.TextField(max_length=5000, null=True, blank=True)
    place = models.ForeignKey(Place, on_delete=models.CASCADE, related_name='+', null=True, blank=True)

    class Meta:
        # unique_together = ('id', 'asked_by', 'question_date', 'question','answer')
        pass

    def __str__(self):
        id = str(self.place)
        if id == 'None': id = '[None] '
        return id + str(self.asked_by) + " | " + str(self.question_date)
