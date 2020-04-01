from django import forms 
from .models import Comment

# Creating the forms for Share 

class EmailPostForm(forms.Form):    
    name = forms.CharField(max_length=25)    
    email = forms.EmailField()    
    to_email = forms.EmailField()    
    comments = forms.CharField(required=False, widget=forms.Textarea)

# Comment form 

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')


