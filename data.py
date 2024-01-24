import requests

parameter = {
    "amount": "10",
    "type": "boolean",
    "category": "",
    "difficulty": "",
}


class APIResponse:

    def __init__(self):
        self.response = None

    def get_response(self):
        self.response = requests.get(url="https://opentdb.com/api.php?", params=parameter)
        self.response.raise_for_status()
        data = self.response.json()
        question_data = data["results"]
        return question_data
