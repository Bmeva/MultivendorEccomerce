from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator


class userform(forms.ModelForm):

    #there is no password and confirm password on the User model so we would create custom fields for them
    password = forms.CharField(widget = forms.PasswordInput())
    confirm_password = forms.CharField(widget = forms.PasswordInput(), help_text="Your password must contain at least 8 characters.")
    class Meta:
        model = User # we are replicating the fields of User model
        fields = ['first_name', 'last_name', 'username', 'email', 'password'] 


    def clean(self):
        cleaned_data = super(userform, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Passwords does not match')


class UserProfileForm(forms.ModelForm):
    primaryAddress = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'start typing...', 'required': 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator]) #on the vprofile.htm we called the profile_picture to display so this code would give the button a style css
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    #we are able to use the profile_pcture and cover_photo bcos these are fields in the UserProfileForm we already declared as the class name
    #latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly': 'readonly'})) # making the latitude as read only
    latitude = forms.CharField(widget=forms.TextInput)
    longitude = forms.CharField(widget=forms.TextInput)# making the longitude as read only
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'cover_photo', 'primaryAddress', 'address_line_1', 'address_line_2', 'country', 'state', 'city', 'pin_code', 'latitude', 'longitude', ]

    """ Another way to set the latitude and longitude to read only
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'latitude' or field == 'longitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
    """



class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name'] # icreated this form becouse i want to use it for the userprofile settings
        # but i dont want the user to change their email and password thats why i used only these fields