''' Entry model definition and methods'''

import requests
from . import db

class Entry(db.Model):
    __tablename__ = 'entries'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time, nullable=False)
    text = db.Column(db.String(255), nullable=False)
    calories = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    '''
    bidirectional relationship between the User and Entry model 
    '''
    user = db.relationship('User', back_populates='entries')

    def __init__(self, date, time, text, calories=None, user_id=None):
        self.date = date
        self.time = time
        self.text = text
        self.calories = calories
        self.user_id = user_id

    '''
        calculate calories if calories is not given as input by the user
        API call to https://www.nutritionix.com
    '''
    def calculate_calories(self):
        if self.calories is None:
            api_url = 'https://trackapi.nutritionix.com/v2/natural/nutrients'
            headers = {
                'Content-Type': 'application/json', 
                'x-app-id': '630dceac', 
                'x-app-key': '8e923dd3df9048bc4c9da8e92928d4bb'
            }
            payload = {'query': self.text}

            try:
                response = requests.post(api_url, json=payload, headers=headers)
                if response.status_code == 200:
                    '''extracting calories from response data'''
                    self.calories = response.json()['foods'][0]['nf_calories']
                else:
                    self.calories = None
            except requests.exceptions.RequestException:
                self.calories = None

    @property
    def is_calorie_intake_less_than_expected(self):
        '''check if the calorie intake is less than expected daily calorie intake'''
        if self.calories is None:
            self.calculate_calories()

        '''total calories consumed on a given date'''
        total_calories = Entry.query.filter_by(user_id=self.user_id, date=self.date).with_entities(db.func.sum(Entry.calories)).scalar()
        return total_calories <= self.user.expected_daily_calories

    '''serialize entry data'''
    def serialize(self):
        return {
            'id': self.id,
            'date': self.date.strftime('%Y-%m-%d'),
            'time': self.time.strftime('%H:%M:%S'),
            'text': self.text,
            'calories': self.calories,
            'is_calorie_intake_less_than_expected': self.is_calorie_intake_less_than_expected,
            'user_id': self.user_id
        }

    '''delete entry'''   
    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''save entry'''
    def save(self):
        if self.calories is None:
            self.calculate_calories()
        db.session.add(self)
        db.session.commit()
