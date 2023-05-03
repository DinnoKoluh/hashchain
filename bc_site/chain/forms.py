from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import Account, Tx, Block

class SignUpForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2') #, 'address', 'test')
    
    # https://stackoverflow.com/questions/34849328/extending-usercreationform-password-not-saved
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username', 'size': 30,
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'placeholder': 'Your email address', 'size': 30,
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password', 'size': 30,
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Repeat password', 'size': 30,
    }))

class LogInForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your username'
    }))

    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Your password'
    }))

class TxForm(forms.ModelForm):
    """
    Form for submitting tx's.
    """
    class Meta:
        model = Tx
        fields = ('to_address', 'amount', 'message')
    to_address = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Input address', 'size': 80, 'maxlength': 64,
    }))

    amount = forms.FloatField(widget=forms.TextInput(attrs={
        'placeholder': '0',
    }))

class BlockForm(forms.ModelForm):
    """
    Mining block, doesn't need any fields, just the mining.
    """
    class Meta:
        model = Block
        exclude = ()
    txs = forms.ModelMultipleChoiceField(
        required=False,
        queryset=Tx.objects.filter(executed=False),
        widget=forms.CheckboxSelectMultiple,
    )