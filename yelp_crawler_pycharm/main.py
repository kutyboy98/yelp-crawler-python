from operator import itemgetter

from models.country_model import Country
from models.category_model import Category
from models.restaurant_model import Restaurant
from models.review_model import Review
from workscope.workscope import WorkScope as ws
from workscope.dbcontext import YelpContext as yelpcontext
from log import yelp_log

def Insert_Category(category_lst, unit_of_work):
    '''
    Using to insert category in your database
    :param category_lst: list of category
    :param unit_of_work: work scope
    :return:
    '''
    try:
        for item in category_lst:
            unit_of_work.category.post([item['id'], item['name'], item['label']])
    except ValueError:
        yelp_log.logger.error(ValueError)

def Insert_Restaurant(country_lst, category_lst, unit_of_work, restaurant, restaurant_id):
    '''
    Using to insert restaurant in your database
    :param country_lst: list of country
    :param category_lst: list of category
    :param unit_of_work: work scope
    :param restaurant: scrawler object
    :param restaurant_id: last restaurant id
    :return:
    '''
    try:
        for item in country_lst:
            for genes in category_lst:
                start = 0
                while True:
                    # Crawl restaurants
                    restaurant_list = restaurant.search_restaurants(genes[0], genes[2], item, str(start))
                    print(f'We got {len(restaurant_list)} restaurants.')
                    if restaurant_list:
                        for res in restaurant_list:
                            if not unit_of_work.restaurant.check_exist(res['code']):
                                # Create restaurant record
                                restaurant_record = [
                                    restaurant_id, res['name'], res['code'],
                                    res['region'], res['category_id'], res['url'],
                                    res['star'], res['review'], res['address'],
                                    res['imgs'], res['services']
                                ]
                                # Insert restaurant record in your database
                                if unit_of_work.restaurant.post(restaurant_record):
                                    restaurant_id += 1
                        print(f'Inserted {restaurant_id} restaurants')
                        print('-------------------------------------')
                        start += len(restaurant_list)
                    else:
                        print(f'Inserted {restaurant_id} restaurants')
                        print('-------------------------------------')
                        break
    except ValueError:
        yelp_log.logger.error(ValueError)

def Insert_Review(restaurant_lst, unit_of_work, review):
    '''
    Using to insert review in your database
    :param restaurant_lst: the list of restaurants
    :param unit_of_work: work scope
    :param review: crawler object
    :return:
    '''
    for res in restaurant_lst:
        start = 0
        while True:
            # Crawl reviews
            reviews = review.get_reviews(res[5], str(start))
            print(f'We got {len(reviews)} reviews')
            if reviews:
                for rv in reviews:
                    if not unit_of_work.review.check_exist(rv['id']):
                        # Create review record
                        review_record = (
                            rv['id'], res[0], rv['content'],
                            rv['imgs'], rv['review'], rv['useful'],
                            rv['funny'], rv['cool'], rv['review_time']
                        )
                        # Insert review record in your database
                        unit_of_work.review.post(review_record)
                start += len(reviews)
            else:
                break

def Main():
    # Create country crawler object
    country = Country()
    # Create category crawler object
    category = Category()
    # Create restaurant crawler object
    restaurant = Restaurant()
    # Create review crawler object
    review = Review()

    # Crawl list of country
    country_lst = country.get_coutries()
    # Crawl list of category
    category_lst = category.get_categories()

    yc = yelpcontext()
    # Create work scope object
    unit_of_work = ws(yc)

    # Handle insert category to the database
    Insert_Category(category_lst, unit_of_work)

    # Get list category in your database
    category_lst = unit_of_work.category.get()
    # Get list restaurant in your database
    restaurant_lst = unit_of_work.restaurant.get()
    # Take last restaurant id in your database
    restaurant_id = sorted(restaurant_lst, key=itemgetter(0), reverse= True)[0][0] + 1 if restaurant_lst else 0

    # Handle insert restaurant to your database
    Insert_Restaurant(country_lst, category_lst, unit_of_work, restaurant, restaurant_id)
    # Take restaurant list in your database
    restaurant_lst = unit_of_work.restaurant.get()

    # Handle insert review to your database
    Insert_Review(restaurant_lst, unit_of_work, review)

    yelpcontext.disconnect()

Main()