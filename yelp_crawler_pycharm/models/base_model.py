import requests as rq

from bs4 import BeautifulSoup as bs

from log import yelp_log


class Base:

    Base_Url = 'https://www.yelp.com'
    Denied_Class_Name = 'u-space-b6'

    def get_content(self, url):
        soup = None
        while True:
            try:
                # Get page source
                html_source = rq.get(url)
                # Exchange html source to text
                plain_text = html_source.text
                if len(plain_text) > 0:
                    soup = bs(plain_text)
                    # Get denied page
                    denied_element = soup.find('div', {'class': self.Denied_Class_Name})
                    # Check denied
                    if denied_element:
                        print(f'{denied_element.find("h2").string} You have to refake your ip.')
                        yelp_log.logger.warning(f'{denied_element.find("h2").string} You have to refake your ip.')
                    else:
                        break
            except ValueError:
                yelp_log.logger.error(ValueError)
            finally:
                if soup:
                    break
                else:
                    continue
        return soup

# print(Base().get_content('https://www.yelp.com/search?cflt=restaurants&find_loc=Hong+Kong%2C+%E9%A6%99%E6%B8%AF%2C+HK'))
# print(rq.get('https://www.yelp.com/search?cflt=restaurants&find_loc=Hong+Kong%2C+%E9%A6%99%E6%B8%AF%2C+HK').text)