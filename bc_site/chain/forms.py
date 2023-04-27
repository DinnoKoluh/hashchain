from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import AccountModel

class SignUpForm(forms.ModelForm):
#class SignUpForm(UserCreationForm):
    class Meta:
        model = AccountModel
        #model = User
        fields = ('username', 'email', 'password1', 'password2') #, 'address', 'test')
    
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     #user.email = self.cleaned_data['email']
    #     if commit:
    #         user.save()
    #         profile = AccountModel.objects.create(user=user, address=self.cleaned_data['address'], test=self.cleaned_data['test'])
    #         profile.save()
    #     return user

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password',
    }))

class LogInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password'
    }))
