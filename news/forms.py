from django import forms

news_sources = [
	('ESPN', 'ESPN'),
	('Yahoo','Yahoo'),
	('FantasyPros','FantasyPros'),
]
'''
teams = [
	('', ''),
	('ARI', 'ARI'),
	('ATL','ATL'),
	('CAR','CAR'),
	('CHI', 'CHI'),
	('DAL','DAL'),
	('DET','DET'),
	('GB', 'GB'),
	('LAR','LAR'),
	('MIN','MIN'),
	('NO', 'NO'),
	('NYG','NYG'),
	('PHI','PHI'),
	('SF', 'SF'),
	('SEA','SEA'),
	('TB','TB'),
	('WAS', 'WAS'),
	('BAL','BAL'),
	('BUF','BUF'),
	('CIN', 'CIN'),
	('CLE','CLE'),
	('DEN','DEN'),
	('HOU', 'HOU'),
	('IND','IND'),
	('JAX','JAX'),
	('KC', 'KC'),
	('LAV','LAV'),
	('LAC',':AC'),
	('MIA', 'MIA'),
	('NE','NE'),
	('NYJ','NYJ'),
	('PIT', 'PIT'),
	('TEN','TEN'),
]
'''
class FilterForm(forms.Form):
	player_or_team = forms.CharField(max_length=200, required=False)
	news_source = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=news_sources,
    )

class PredictionForm(forms.Form):
	player = forms.CharField(max_length=200)
