from django.db import models
from accounts.models import User, UserProfile
from loginout.utils import send_notification
from datetime import time, date, datetime


# Create your models here.
class vendor(models.Model):
    user = models.OneToOneField(User, related_name='user', on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile, related_name='userprofile', on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length=50)
    office_phone = models.CharField(max_length=16, blank=True)
    #vendor_slug = models.SlugField(max_length=100, blank=True)#if you add a slug field after you have already created your model and added data then you need to add the slug 
    #manaually for all the items you have saved on your admin panel. after that change blank = True to unique = True
    vendor_slug = models.SlugField(max_length=100, unique=True)
    vendor_license = models.ImageField(upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.vendor_name

    def is_open(self):
        today_date = date.today()
        today = today_date.isoweekday() #gets 1, 2,3 etc according to the number of the week
        current_day_opening_hour = openingHour.objects.filter(Vendor=self, day = today)
        now = datetime.now()

        is_open = None
        if current_day_opening_hour.exists():
            for i in current_day_opening_hour:
                if i.from_hour and i.to_hour:  # Check if the values are not empty
                    start_time = datetime.strptime(i.from_hour, "%I:%M %p").time() 
                                    
                    end_time = datetime.strptime(i.to_hour, "%I:%M %p").time()

                    if start_time <= now.time() <= end_time:
                        is_open = True
                        break
                    else:
                        is_open = False
                else:
                    is_open = False  # Handle the case where there is no time values are empty
                    break
        else:
            is_open = None
        return is_open

    
      

    def save(self, *args, **kwargs): #gets tiggered when the save button is clicked on the admin 
        #dashboard. it checks the approval status of the is_approved for the vendor and sends a mail

        if self.pk is not None:
            #update
            orig = vendor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'accounts/emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }

                if self.is_approved == True:

                    #send notification email
                    mail_subject = "Congrats your restaurant has been approved"
                    send_notification(mail_subject, mail_template, context)
                else:
                    #send notification email
                    mail_subject = "Your application has been rejected"
                    send_notification(mail_subject, mail_template, context)



        return super(vendor, self).save(*args, **kwargs) #the super funtion allows you to access
    #the save methord of the vendor class

DAYS = [
    (1, ("Monday")),
    (2, ("Tuesday")),
    (3, ("Wednesday")),
    (4, ("Thursday")),
    (5, ("Friday")),
    (6, ("Saturday")),
    (7, ("Sunday")),
]
HOUR_OF_DAY_24 = [(time(h, m).strftime('%I:%M %p'), time(h, m).strftime('%I:%M %p')) for h in range(0, 24) for m in (0, 30)]
class openingHour(models.Model):
    Vendor = models.ForeignKey(vendor, on_delete=models.CASCADE)
    day = models.IntegerField(choices=DAYS)
    from_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank = True)
    to_hour = models.CharField(choices=HOUR_OF_DAY_24, max_length=10, blank = True)
    is_closed = models.BooleanField(default = False)

    
    class Meta:
        ordering = ('day', '-from_hour') #The - would order it properly if you have multiple entries for the same day
        unique_together = ('day', 'from_hour', 'to_hour') #It checks if you are adding same time for a particular day
   
    def  __str__(self):
        return self.get_day_display() #this inbuilt function would make you see the lables in the DAYS list