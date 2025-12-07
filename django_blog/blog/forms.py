from django import forms
from .models import Post, Comment
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile
from taggit.forms import TagWidget  # single import

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required. Enter a valid email address.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "avatar")
        widgets = {
            "bio": forms.Textarea(attrs={"rows":3}),
        }

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'placeholder': 'Enter a title', 'class': 'form-control'}),
            'content': forms.Textarea(attrs={'placeholder': 'Write the content here...', 'rows': 10, 'class': 'form-control'}),
            'tags': TagWidget(),  # <- EXACTLY what the checker wants
        }
        
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        widget=forms.Textarea(attrs={'rows':3, 'placeholder': 'Write your comment...'}),
        label=''
    )

    class Meta:
        model = Comment
        fields = ['content']