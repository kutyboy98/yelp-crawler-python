import requests as rq
import json
import pandas as pd
from datetime import datetime

from models import base_model

class Review(base_model.Base):

    Base_Api = '{0}/review_feed?rl=en&sort_by=relevance_desc&q=&start={1}'

    def get_reviews(self, restaurant_url, start):
        result = []
        api = self.Base_Api\
                        .replace('{0}', restaurant_url)\
                        .replace('{1}', start)
        print(api)
        response = rq.get(api)
        if response.status_code == 200:
            reviews = json.loads(response.content)['reviews']
            if reviews:
                for review in pd.DataFrame(reviews).iterrows():
                    record = {}
                    review = review[1]
                    comment = review['comment']['text']
                    record['content'] = comment if len(comment) < 2000 else comment[0:2000]
                    record['id'] = review['id']
                    record['review_time'] = datetime.strptime(review['localizedDate'], '%m/%d/%Y')
                    record['review_time'] = datetime.strftime(record['review_time'], '%Y/%m/%d')
                    record['imgs'] = ','.join([photo['src'] for photo in review['photos']]) if review['photos'] else ''
                    feedback = review['feedback']['counts']
                    record['funny'] = int(feedback['funny'])
                    record['useful'] = int(feedback['useful'])
                    record['cool'] = int(feedback['cool'])
                    record['review'] = record['funny'] + record['useful'] + record['cool']
                    result.append(record)
        return result




# Review().get_reviews('https://www.yelp.com/biz/%E6%B7%BB%E5%A5%BD%E9%81%8B-%E9%A6%99%E6%B8%AF-6','1000')