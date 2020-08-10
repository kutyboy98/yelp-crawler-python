from models import base_model

from log import yelp_log

class Restaurant(base_model.Base):

    # You will see the rule of each restaurant list like that with first param is category label,
    # second param is region and last param is item position
    Search_Url = 'https://www.yelp.com/search?cflt={0}&find_loc={1}&start={2}'
    # Class name of div tag where it save each restaurant information
    Container_Class_Name = 'lemon--li__373c0__1r9wz border-color--default__373c0__3-ifU'
    # Some class name relate with the restaurant information
    Element_Detail = {
        'link': 'link__373c0__1G70M',
        'img': 'photoHeader__373c0__YdvQE',
        'title': 'alternate__373c0__2Mge5',
        'star': 'i-stars__373c0__1T6rz',
        'review': 'reviewCount__373c0__2r4xT',
        'address': 'lemon--address__373c0__2sPac',
        'detail-block': 'arrange-unit-grid-column--8__373c0__2dUx_',
        'services': 'lemon--a__373c0__IEZFH link__373c0__2-XHa link-color--inherit__373c0__2f-vZ link-size--inherit__373c0__nQcnG'
    }

    def search_restaurants(self,category_id, category, region, start):
        '''
        This method result the list of restaurant
        :param category_id:
        :param category:
        :param region:
        :param start:
        :return:
        '''
        result = []
        url = self.Search_Url.replace('{0}', category) \
            .replace('{1}', region) \
            .replace('{2}', start)
        print(url)
        soup = self.get_content(url)
        for elm in soup.find_all('li', {'class', self.Container_Class_Name}):
            star = elm.find('div', {'class': self.Element_Detail['star']})
            review = elm.find('span', {'class': self.Element_Detail['review']})
            title = elm.find('h4', {'class': self.Element_Detail['title']})
            atag = title.find('a', {'class': self.Element_Detail['link']}) if title else None
            if atag:
                href = atag.get('href')
                if href.find('/biz/') != -1:
                    restaurant = {}
                    split_data = href.split('/')
                    restaurant['name'] = atag.string
                    restaurant['region'] = region
                    restaurant['category_id'] = category_id
                    restaurant['url'] = self.Base_Url + href
                    restaurant['code'] = split_data[2]
                    restaurant['star'] = float(star.get('aria-label').replace(' star rating', '')) if star else 0.0
                    restaurant['review'] = int(review.string) if review else 0
                    restaurant_detail = self.get_restaurant_detail(restaurant['url'])
                    restaurant['address'] = restaurant_detail['address']
                    restaurant['imgs'] = restaurant_detail['imgs']
                    restaurant['services'] = restaurant_detail['services']
                    result.append(restaurant)
        return result

    def get_restaurant_detail(self, url):
        '''
        This method come to the restaurant detail page and result some restaurant information
        :param url:
        :return:
        '''
        result = {'address': '', 'imgs': '', 'services': ''}
        soup = self.get_content(url)
        if soup:
            address = soup.find('address', {'class': self.Element_Detail['address']})
            imgs = soup.find('div', {'class': self.Element_Detail['img']})
            detail_block = soup.find('div', {'class': self.Element_Detail['detail-block']})
            services = detail_block.find_all('a', {'class': self.Element_Detail['services']}) if detail_block else None
            result['address'] = ','.join([add.string for add in address.find_all('span')]) if address else ''
            result['imgs'] = ','.join([img.get('src') for img in imgs.find_all('img')]) if imgs else ''
            result['services'] = ','.join([span.string for span in services]) if services else ''
        return result

