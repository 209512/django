from django import forms
from todo.models import Todo, Comment

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description','start_date', 'end_date', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '할 일 제목'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': '자세한 내용'}),
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'is_completed': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class TodoUpdateForm(forms.ModelForm):
    class Meta:
        model = Todo
        fields = ['title', 'description','start_date', 'end_date', 'is_completed']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
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