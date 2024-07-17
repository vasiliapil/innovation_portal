from django import forms

from .models import Comment, Topic, Post

class CreateTopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = [
            'Τίτλος', 'Περιγραφή'
        ]
        


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'Περιεχόμενο'
        ]