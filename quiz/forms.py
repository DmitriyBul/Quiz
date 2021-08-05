from django import forms
from .models import UsersAnswer


class UserAnswerForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user')
        self.question = kwargs.pop('question')
        super(UserAnswerForm, self).__init__(*args, **kwargs)

    class Meta:
        model = UsersAnswer
        fields = ('answer',)
        exclude = ('user', 'question')
