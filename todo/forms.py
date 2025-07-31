from django import forms
from todo.models import Todo, Comment
from django_summernote.widgets import SummernoteWidget

class TodoForm(forms.ModelForm):
    completed_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Todo
        fields = ['title', 'description','start_date', 'end_date', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '제목을 입력해주세요.'}),
            'description': SummernoteWidget(),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TodoUpdateForm(forms.ModelForm):
    completed_image = forms.ImageField(required=False, widget=forms.ClearableFileInput(attrs={'class': 'form-control'}))
    class Meta:
        model = Todo
        fields = ['title', 'description','start_date', 'end_date', 'is_completed', 'completed_image']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': SummernoteWidget(),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['message']
        labels = {
            'message': '내용',
        }
        widgets = {
            'message': forms.Textarea(attrs={
                'rows': 3,
                'cols': 40,
                'class': 'form-control',
                'placeholder': '댓글 내용을 입력해주세요,'
            }),
        }