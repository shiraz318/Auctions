class Product:
    def __init__(self, name, value, index, optional_values):
        self.name = name
        self.value = value
        self.index = index
        self.optional_values = optional_values


class ProductBid:
    def __init__(self, product, estimated_value, highest_offer):
        self.product = product
        self.estimated_value = int(estimated_value.split(" ")[0])
        self.highest_offer = int(highest_offer.split(" ")[0])


# FIRST PRICE AUCTION PRODUCTS
DISK = Product("Disk", 100, 0, [60, 80, 100, 120, 140])
BICYCLE = Product("Bicycle", 4000, 1, [1000, 2000, 3000, 4000])
BAG = Product("Bag", 180, 2, [120, 140, 160, 180])

# SECOND PRICE AUCTION PRODUCTS
IMAGE = Product("Image", 80, 0, [60, 70, 80, 90])
REFRIGERATOR = Product("Refrigerator", 1000, 1, [1000, 1500, 2000, 2500])
FAN = Product("Fan", 120, 2, [60, 80, 100, 120])

# DUTCH AUCTION PRODUCTS
TABLE = Product("Table", 280, 0, [180, 200, 240, 280])
HEADPHONES = Product("Headphones", 140, 1, [40, 70, 100, 140])
SPORT_SHOES = Product("Sport Shoes", 300, 2, [150, 200, 250, 300])

# ENGLISH AUCTION PRODUCTS
SHOW_TICKET = Product("Show Ticket", 120, 0, [120, 140, 160, 180])
BOOK = Product("Book", 100, 1, [70, 80, 90, 100])
CLOCK = Product("Clock", 80, 2, [40, 60, 80, 100])
