import requests as rq

from bs4 import BeautifulSoup as bs


class Base:

    Base_Url = 'https://www.yelp.com'
    Denied_Class_Name = 'u-space-b6'

    def get_content(self, url):
        soup = None
        while True:
            try:
                html_source = rq.get(url)
                plain_text = html_source.text
                if len(plain_text) > 0:
                    soup = bs(plain_text)
                    denied_element = soup.find('div', {'class': self.Denied_Class_Name})
                    if denied_element:
                        print(f'{denied_element.find("h2").string} You have to refake ip.')
                    else:
                        break
            except ValueError:
                print(ValueError)
            finally:
                if soup:
                    break
                else:
                    continue
        return soup

# print(Base().get_content('https://www.yelp.com/search?cflt=restaurants&find_loc=Hong+Kong%2C+%E9%A6%99%E6%B8%AF%2C+HK'))
# print(rq.get('https://www.yelp.com/search?cflt=restaurants&find_loc=Hong+Kong%2C+%E9%A6%99%E6%B8%AF%2C+HK').text)