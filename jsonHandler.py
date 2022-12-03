import json


class JsonReader:
    def __init__(self, path):
        self.path = path

    def getJson(self):
        with open(self.path, encoding='utf-8') as fp:
            json_data = json.load(fp)
            return json_data

    def writejson(self, params):
        with open(self.path, 'w', encoding='utf-8') as r:
            json.dump(params, r, indent=4, ensure_ascii=False)

            
