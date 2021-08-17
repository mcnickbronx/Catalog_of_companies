from import_export import resources
from import_export.fields import Field
from import_export.fields import widgets

from .models import Place, Open, Review, Highlights, Question

class DecimalWidget(widgets.NumberWidget):
    def clean(self, value, row=None, *args, **kwargs):
        if type(value) == str:
            value = value.replace(',','.')
            return value
        else:
            return value

class PlaceWidget(widgets.NumberWidget):
    def clean(self, value, row=None, *args, **kwargs):
        try:
            place = Place.objects.get(pk=value)
        except Place.DoesNotExist:
            value = None
        return value



class PlaceResource(resources.ModelResource):
    id = Field(attribute='id', column_name='ID')   
    city = Field(attribute='city', column_name='City')
    region = Field(attribute='region', column_name='Region')
    business_names = Field(attribute='business_names', column_name='Business Names')
    company_name  = Field(attribute='company_name', column_name='Company Name')
    
    rating = Field(attribute='rating', column_name='Rating', widget=DecimalWidget())
    review = Field(attribute='review', column_name='Review') 
    category = Field(attribute='category', column_name='Category') 
    address = Field(attribute='address', column_name='Address') 
    latitude = Field(attribute='latitude', column_name='Latitude') 
    longitude = Field(attribute='longitude', column_name='Longitude') 
    phone = Field(attribute='phone', column_name='Phone') 
    website = Field(attribute='website', column_name='Website')
    link_to_menu = Field(attribute='link_to_menu', column_name='Link to menu') 
    location = Field(attribute='location', column_name='Location') 
    critic_reviews = Field(attribute='critic_reviews', column_name='Critic Reviews') 
    nearby = Field(attribute='nearby', column_name='Nearby')

    from_these_lists = Field(attribute='from_these_lists', column_name='From these lists') 
    reviews_sorting = Field(attribute='reviews_sorting', column_name='Reviews Sorting') 
    product_title = Field(attribute='product_title', column_name='Product Title') 
    product_url = Field(attribute='product_url', column_name='Product Url') 
    photos_menu = Field(attribute='photos_menu', column_name='Photos Menu') 
    photos_owner = Field(attribute='photos_owner', column_name='Photos Owner') 
    photos_inside = Field(attribute='photos_inside', column_name='Photos Inside') 
    about = Field(attribute='about', column_name='About') 
    about_details = Field(attribute='about_details', column_name='About Details')

    details = Field(attribute='details', column_name='Details') 
    facebook = Field(attribute='facebook', column_name='Facebook') 
    instagram = Field(attribute='instagram', column_name='Instagram') 
    linkedin = Field(attribute='linkedin', column_name='Linkedin') 
    twitter = Field(attribute='twitter', column_name='Twitter') 
    youtube = Field(attribute='youtube', column_name='Youtube') 
    pinterest = Field(attribute='pinterest', column_name='Pinterest')

    service_options = Field(attribute='service_options', column_name='Service Options') 
    offerings = Field(attribute='offerings', column_name='Offerings') 
    dining_options = Field(attribute='dining_options', column_name='Dining Options') 
    amenities = Field(attribute='amenities', column_name='Amenities') 
    atmosphere = Field(attribute='atmosphere', column_name='Atmosphere') 
    crowd = Field(attribute='crowd', column_name='Crowd') 
    accessibility = Field(attribute='accessibility ', column_name='Accessibility') 
    planning = Field(attribute='planning', column_name='Planning') 
    payments = Field(attribute='payments', column_name='Payments')
     
    price = Field(attribute='price', column_name='Price') 
    services = Field(attribute='services', column_name='Services')  

    class Meta:
        model = Place
        fields = ('id','city','region','business_names','rating','review','category','address','latitude','longitude','phone','website','link_to_menu','location','critic_reviews','nearby','from_these_lists','reviews_sorting','product_title','product_url','photos_menu','photos_owner','photos_inside','about','about_details','details','facebook','instagram','linkedin','twitter','youtube','pinterest','service_options','offerings','dining_options','amenities','atmosphere','crowd','accessibility','planning','payments','price','services')
        #export_order = ('id','city','region','business_names','rating','review','category','address','latitude','longitude','phone','website','link_to_menu','location','critic_reviews','nearby','from_these_lists','reviews_sorting','product_title','product_url','photos_menu','photos_owner','photos_inside','about','about_details','details','facebook','instagram','linkedin','twitter','youtube','pinterest','service_options','offerings','dining_options','amenities','atmosphere','crowd','accessibility','planning','payments','price','services')


class OpenResource(resources.ModelResource):
    place = Field(attribute='place_id', column_name='ID')
    day = Field(attribute='day', column_name='Day')
    open_interval = Field(attribute='open_interval', column_name='Open Interval')
    class Meta:
        model = Open

class ReviewResource(resources.ModelResource):
    place = Field(attribute='place_id', column_name='ID', widget=PlaceWidget())
    reviewer_name = Field(attribute='reviewer_name', column_name='Reviewer Name')
    reviewer_profile_linkl = Field(attribute='reviewer_profile_linkl', column_name='Reviewer Profile Link')
    rating_stars = Field(attribute='rating_stars', column_name='Rating (stars)', widget=DecimalWidget())
    review_date = Field(attribute='review_date', column_name='Review Date')
    review_text = Field(attribute='review_text', column_name='Review Text')
    review_pictures = Field(attribute='review_pictures', column_name='Review Pictures')
    class Meta:
        model = Review

class HighlightsResource(resources.ModelResource):
    place = Field(attribute='place_id', column_name='ID')
    listing_name = Field(attribute='listing_name', column_name='Listing name')
    food_name = Field(attribute='food_name', column_name='Food name')
    product_picture = Field(attribute='product_picture', column_name='Product picture')
    class Meta:
        model = Highlights

class QuestionResource(resources.ModelResource):
    place = Field(attribute='place_id', column_name='ID', widget=PlaceWidget())
    asked_by = Field(attribute='asked_by', column_name='Asked by')
    answered_by = Field(attribute='answered_by', column_name='Answered by')
    asked_by_profile = Field(attribute='asked_by_profile', column_name='Asked by profile')
    answered_by_profile = Field(attribute='answered_by_profile', column_name='Answered by profile')
    question_date = Field(attribute='question_date', column_name='Question Date')
    question = Field(attribute='question', column_name='Question')
    answer = Field(attribute='answer', column_name='Answer')
    class Meta:
        model = Question
