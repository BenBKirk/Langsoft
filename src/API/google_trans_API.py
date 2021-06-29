
import requests
# https://translate.googleapis.com/translate_a/single?client=gtx&ie=UTF-8&oe=UTF-8&sl=de&tl=en&dt=t&q=kaiser


class GoogleTranslate:
    def __init__(self):
        self.url = "https://translate.googleapis.com/translate_a/single?client=gtx&ie=UTF-8&oe=UTF-8&sl=id&tl=en&dt=t&q="

    def translate(self, text):
        response = requests.get(self.url + text)
        jsonResponse = response.json()
        # plainText = json.loads(jsonResponse)
        return jsonResponse[0][0][0]