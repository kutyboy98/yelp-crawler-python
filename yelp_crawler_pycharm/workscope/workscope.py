from workscope import dbcontext


class WorkScope:

    category = None
    restaurant = None
    review = None

    def __init__(self, _dbcontext):
        self.category = dbcontext.CategoryDbSet(_dbcontext)
        self.restaurant = dbcontext.RestaurantDbSet(_dbcontext)
        self.review = dbcontext.ReviewDbSet(_dbcontext)

