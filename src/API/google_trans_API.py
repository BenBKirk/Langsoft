
import requests
class GoogleTranslate:
    def __init__(self):
        # this url gives all the extra information "https://translate.googleapis.com/translate_a/single?client=gtx&sl=id&tl=en&hl=en-GB&dt=t&dt=bd&dj=1&source=bubble&tk=702420.702420&q=bahasa"
        # you can find this url by inspecting a web page and watching network requests to see what is being sent by gooogle tranlsate browser extension.
        self.url = "https://translate.googleapis.com/translate_a/single?client=gtx&ie=UTF-8&oe=UTF-8&sl=id&tl=en&dt=t&q="

    def translate(self, text):
        if text:
            try:
                response = requests.get(self.url + text)
                jsonResponse = response.json()
                print(jsonResponse)
                return jsonResponse[0][0][0]
            except:
                return None