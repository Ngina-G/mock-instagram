from django.db import models  
from django.forms import ModelForm  
from .models import Profile  
  
  
class UserImageForm(ModelForm):  
    class Meta:  
        model = Profile
        exclude = ['bio']