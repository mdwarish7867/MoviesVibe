from django import forms
from home.models import Movie, Review, ContactMessage, Genre

class MovieForm(forms.ModelForm):
    genres = forms.ModelMultipleChoiceField(
        queryset=Genre.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        error_messages={
            'required': 'Please select at least one genre.',
        }
    )
    
    class Meta:
        model = Movie
        fields = '__all__'
        widgets = {
            'release_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'genres': forms.CheckboxSelectMultiple(attrs={'class': 'form-check-input'}),
            'type': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        
    def clean(self):
        cleaned_data = super().clean()
        # Ensure at least one genre is selected
        genres = cleaned_data.get('genres')
        if not genres:
            self.add_error('genres', 'Please select at least one genre.')
        return cleaned_data

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.NumberInput(attrs={'min': 0, 'max': 10, 'step': 0.5}),
        }

class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'message']