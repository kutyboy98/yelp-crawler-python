import requests as rq
import json
import pandas as pd


class Country:

    Base_Api = 'https://api.first.org/data/v1/countries'

    def get_coutries(self):
        response = rq.get(self.Base_Api)
        if response.status_code == 200:
            datas = json.loads(response.content)['data']
            data_frame = pd.DataFrame(datas)
            return data_frame.head(1).values[0]
        return []

