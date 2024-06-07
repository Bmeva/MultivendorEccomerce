from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from .models import User, UserProfile



@receiver(post_save, sender=User) # this is a decorator that connects the receiver to the sender
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
   
    print(created)
    if created:
        UserProfile.objects.create(user=instance)# once the created flag is true it brings up the profile creation module
       
    else: # this else block checks if it is an update and not created. so it handles when you go to user profile and edits not create
        try:
            profile = UserProfile.objects.get(user = instance)
            profile.save()
        except: # the else and try bllock checks if there is no user profile at all. for exmaple you go and delete the user profile in one page and try to update it in another page
            #it would simply create another profile if the profile dont exist
            UserProfile.objects.create(user=instance)

#post_save.connect(post_save_create_profile_receiver, sender=User) #this is also a decorator and would also work but in pre_save we used the upper style
            

@receiver(pre_save, sender=User) 
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username, 'this user is being saved')



#post_save.connect(post_save_create_profile_receiver, sender=User)


    


    
    
   
    

# Create your models here.
