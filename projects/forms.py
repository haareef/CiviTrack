from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Project, Branch, SubBranch, ReleasedHistory


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].label = 'DOB (Password)'
        self.fields['password1'].help_text = 'Enter 8 digits (Ex: 25042004)'
        self.fields['password2'].label = 'Confirm Password'


class UserLoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'input-field', 'placeholder': 'Email'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'input-field', 'placeholder': 'Password'}), label='DOB (Password)')


class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['name', 'amount', 'start_date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter project name'}),
            'amount': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Ex: 2000000', 'step': '0.01'}),
            'start_date': forms.DateInput(attrs={'class': 'input-field', 'type': 'date'}),
        }


class BranchForm(forms.ModelForm):
    class Meta:
        model = Branch
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter branch name'}),
        }


class SubBranchForm(forms.ModelForm):
    class Meta:
        model = SubBranch
        fields = ['name', 'amount', 'date']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'input-field', 'placeholder': 'Enter sub-branch name'}),
            'amount': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Amount', 'step': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'input-field', 'type': 'date'}),
        }


class ReleasedHistoryForm(forms.ModelForm):
    class Meta:
        model = ReleasedHistory
        fields = ['amount', 'date']
        widgets = {
            'amount': forms.NumberInput(attrs={'class': 'input-field', 'placeholder': 'Enter amount', 'step': '0.01'}),
            'date': forms.DateInput(attrs={'class': 'input-field', 'type': 'date'}),
        }
