from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


CHOICES_SOUNDS = [('i','i'),('I','I'),('e','e'),('ԑ','ԑ'),('ᴂ','ᴂ'),('a','a'),('ᴧ','ᴧ'),('o','o'),('ᶷ','ᶷ'),('u','u')]

class startquizzForm(forms.Form):
    number_of_word = forms.IntegerField(label='No. of Words',max_value=10,min_value=1)
    sounds = forms.MultipleChoiceField(label='Choose your vowels',widget=forms.CheckboxSelectMultiple(attrs={'class' : 'myfieldclass2'}),choices=CHOICES_SOUNDS,required=False,)
    number_of_gusses = forms.IntegerField(label='No. of Guesses',max_value=5,min_value=0)

    def clean_sounds(self,*args, **kwargs):
        sounds = self.cleaned_data.pop("sounds")
        y = 0
        for x in sounds:
            y = y+1
        if y >= 2 :
            return sounds     
        else:
            raise forms.ValidationError("please chose 2 sounds ")
        
    


class sugestionForm(forms.Form):
    quiz_num = forms.CharField(widget = forms.HiddenInput(), required = False)
    qst_num = forms.CharField(widget = forms.HiddenInput(), required = False)
    sugestions = forms.CharField(label='sugestions',widget=forms.RadioSelect(choices=CHOICES_SOUNDS))


class UserForm(UserCreationForm):

        class Meta:
          model = User
          fields = ["username","email","password1","password2"]