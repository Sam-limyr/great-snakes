"""
    A short Python script to determine steak ratings.

    Main evaluation function: Restaurant.get_rating()

    Other constants to maintain:
        REQUIRED_CRITERIA: Used for maintaining criteria. All criteria names must be added.
        RESTAURANTS: All restaurant entries, in a suitable tuple form.
        PRINT_TOP_K: Number of top-rated restaurants to print.
    
"""


class Restaurant:

    def __init__(self, name, **kwargs):
        self.name = name
        self.__dict__.update(kwargs)
        self.assert_criteria()

    def get_name(self):
        return self.name

    def get_rating(self):
        return (2 * self.price) + (self.taste ** 2)

    def assert_criteria(self):
        for criteria in REQUIRED_CRITERIA:
            assert hasattr(self, criteria), "Missing required criteria: {}".format(criteria)


def populate_restaurants(restaurants):
    
    def unpack_criteria_values(values):
        return dict(zip(REQUIRED_CRITERIA, values))

    restaurant_list = [Restaurant(name, **unpack_criteria_values(args)) for name, *args in restaurants]
    return restaurant_list


def obtain_scores(restaurant_list):
    restaurant_scores = [(restaurant.get_name(), restaurant.get_rating()) for restaurant in restaurant_list]
    sorted_scores = sorted(restaurant_scores, key=lambda x: x[1], reverse=True)
    return sorted_scores


RESTAURANTS = [
    ('Sarnies', 6, 8),
    ('iSteaks', 6, 6),
    ('Siam Kitchen', 8, 6),
    ('Bizen', 3, 5),
    ('Collins', 4, 4),
    ('Astons', 8, 2),
    ('Hot Tomato', 10, 2),
    ('Opus Bar and Grill', 1, 9),
    ('Black Marble', 2, 5),
    ('Assembly Ground', 4, 2),
    ('Armoury', 9, 3),
    ('Waa Cow', 4, 5),
    ('Aburi En', 3, 7),
    ('Fish and Chicks', 8, 2),
    ('Feather Blade', 5, 4),
    ('Flamed Diced Beef Cubes', 6, 6)

    # ('Meating Place', unable to remember)
    # ('Triple Three', unfair to judge price, 8)

]

REQUIRED_CRITERIA = ['price', 'taste']

restaurant_list = populate_restaurants(RESTAURANTS)
restaurant_scores = obtain_scores(restaurant_list)

PRINT_TOP_K = 100

for i in range(min(PRINT_TOP_K, len(restaurant_scores))):
    print(restaurant_scores[i])
