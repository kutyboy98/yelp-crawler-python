from operator import itemgetter

from models.country_model import Country
from models.category_model import Category
from models.restaurant_model import Restaurant
from models.review_model import Review
from workscope.workscope import WorkScope as ws
from workscope.dbcontext import YelpContext as yelpcontext

def Insert_Category(category_lst, unit_of_work):
    try:
        for item in category_lst:
            unit_of_work.category.post([item['id'], item['name'], item['label']])
    except ValueError:
        print(ValueError)

def Insert_Restaurant(country_lst, category_lst, unit_of_work, restaurant, restaurant_id):
    try:
        for item in country_lst:
            for genes in category_lst:
                start = 0
                while True:
                    restaurant_list = restaurant.search_restaurants(genes[0], genes[2], item, str(start))
                    print(f'We got {len(restaurant_list)} restaurants.')
                    if restaurant_list:
                        for res in restaurant_list:
                            if not unit_of_work.restaurant.check_exist(res['code']):
                                restaurant_record = [
                                    restaurant_id, res['name'], res['code'],
                                    res['region'], res['category_id'], res['url'],
                                    res['star'], res['review'], res['address'],
                                    res['imgs'], res['services']
                                ]
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
        print(ValueError)

def Insert_Review(restaurant_lst, unit_of_work, review):
    for res in restaurant_lst:
        start = 0
        while True:
            reviews = review.get_reviews(res[5], str(start))
            print(f'We got {len(reviews)} reviews')
            if reviews:
                for rv in reviews:
                    if not unit_of_work.review.check_exist(rv['id']):
                        review_record = (
                            rv['id'], res[0], rv['content'],
                            rv['imgs'], rv['review'], rv['useful'],
                            rv['funny'], rv['cool'], rv['review_time']
                        )
                        unit_of_work.review.post(review_record)
                start += len(reviews)
            else:
                break

def Main():
    country = Country()
    category = Category()
    restaurant = Restaurant()
    review = Review()

    country_lst = country.get_coutries()
    category_lst = category.get_categories()

    yc = yelpcontext()
    unit_of_work = ws(yc)

    #Insert_Category(category_lst, unit_of_work)

    category_lst = unit_of_work.category.get()
    restaurant_lst = unit_of_work.restaurant.get()
    restaurant_id = sorted(restaurant_lst, key=itemgetter(0), reverse= True)[0][0] + 1 if restaurant_lst else 0

    # Insert_Restaurant(country_lst, category_lst, unit_of_work, restaurant, restaurant_id)
    restaurant_lst = unit_of_work.restaurant.get()

    Insert_Review(restaurant_lst, unit_of_work, review)

Main()