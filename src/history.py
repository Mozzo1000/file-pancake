import json
import os

class History():
    def __init__(self):
        history_location = os.path.join(os.path.expanduser("~"), '.pancake')
        self.history_file = history_location + '/history.json'

        default_history = {}
        default_history['history'] = []
        default_history['history'].append({'location': '~', 'weight': '1000'})

        if not os.path.exists(history_location):
            os.makedirs(history_location)

        if not os.path.exists(self.history_file):
            with open(self.history_file, 'w') as outfile:
                json.dump(default_history, outfile)

        self.global_history = self.load()

    def load(self):
        with open(self.history_file, 'r') as json_file:
            return json.load(json_file)

    def save(self):
        with open(self.history_file, 'w') as outfile:
            json.dump(self.global_history, outfile)

    def add_visit(self, folder):
        exists = False
        for i in self.global_history['history']:
            if folder in i['location']:
                exists = True
        if not exists:
            self.global_history['history'].append({'location': folder, 'weight': '1'})

    
    def update_visit_amount(self, folder, amount=1):
        pass
