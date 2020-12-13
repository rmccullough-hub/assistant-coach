from django import forms

# Forms
news_sources = [
	('ESPN', 'ESPN'),
	('Yahoo','Yahoo'),
	('FantasyPros','FantasyPros'),
]

class FilterForm(forms.Form):
	player_or_team = forms.CharField(max_length=200, required=False)
	news_source = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=news_sources,
    )

class PredictionForm(forms.Form):
	player = forms.CharField(max_length=200)
