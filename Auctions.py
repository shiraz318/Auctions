from Products import DISK, BICYCLE, BAG, IMAGE, REFRIGERATOR, FAN, TABLE, HEADPHONES, SPORT_SHOES, ProductBid, \
    SHOW_TICKET, BOOK, CLOCK


NUM_OF_PRODUCTS = 3
YES = 'כן'
DROP = 'פורש\ת'


# Abstract class.
class Auction:
    def __init__(self, results):
        self.products = []
        self.results_per_product = {0: [], 1: [], 2: []}
        self.set_results(results)
        self.set_products()

    # Gets the auction's name.
    def get_auction_name(self):
        raise NotImplementedError

    # Map from index to product.
    def index_to_product(self, idx):
        raise NotImplementedError

    # Set results_per_product accordingly to the given results.
    def set_results(self, results):
        raise NotImplementedError

    # Set the current auction products.
    def set_products(self):
        for idx in range(NUM_OF_PRODUCTS):
            self.products.append(self.index_to_product(idx))


# Abstract class.
class SimpleAuction(Auction):
    def get_auction_name(self):
        raise NotImplementedError

    def index_to_product(self, idx):
        raise NotImplementedError

    def set_results(self, results):
        for result in results:
            for i in range(0, NUM_OF_PRODUCTS):
                p_b = ProductBid(self.index_to_product(i), result[(i * 2)], result[(i * 2) + 1])
                self.results_per_product[i].append(p_b)


# First Price Auction class.
class FirstPriceAuction(SimpleAuction):
    def index_to_product(self, idx):
        switcher = {
            0: DISK,
            1: BICYCLE,
            2: BAG,
        }
        return switcher.get(idx, DISK)

    def get_auction_name(self):
        return 'FIRST PRICE AUCTION'


# Second Price Auction class.
class SecondPriceAuction(SimpleAuction):

    def get_auction_name(self):
        return 'SECOND PRICE AUCTION'

    def index_to_product(self, idx):
        switcher = {
            0: IMAGE,
            1: REFRIGERATOR,
            2: FAN,
        }
        return switcher.get(idx, IMAGE)


# Dutch Auction class.
class DutchAuction(Auction):

    def get_auction_name(self):
        return "DUTCH AUCTION"

    def index_to_product(self, idx):
        switcher = {
            0: TABLE,
            1: HEADPHONES,
            2: SPORT_SHOES,
        }
        return switcher.get(idx, TABLE)

    # Map a given product to it's optional offers.
    def product_to_optional_offers(self, product):
        switcher = {
            TABLE: [300, 280, 260, 240, 220, 200, 180, 160, 140, 0],
            HEADPHONES: [150, 130, 110, 90, 70, 0],
            SPORT_SHOES: [350, 330, 310, 290, 270, 250, 230, 210, 190, 170, 150, 0],
        }
        return switcher.get(product, [])

    def set_results(self, results):
        for result in results:
            count = 0
            for i in range(0, NUM_OF_PRODUCTS):
                cur_product = self.index_to_product(i)
                num_of_options = len(self.product_to_optional_offers(cur_product)) - 1
                estimated_value = result[count]
                highest_offer = str(self.product_to_optional_offers(cur_product)[-1])

                count += num_of_options + 1
                for j in range(num_of_options):
                    # The player took the current offer.
                    if result[1 + j] == YES:
                        highest_offer = str(self.product_to_optional_offers(cur_product)[j])
                p_b = ProductBid(cur_product, estimated_value, highest_offer)
                self.results_per_product[i].append(p_b)


#  English Auction class.
class EnglishAuction(Auction):

    JUMPS = 10

    def get_auction_name(self):
        return "ENGLISH AUCTION"

    def index_to_product(self, idx):
        switcher = {
            0: SHOW_TICKET,
            1: BOOK,
            2: CLOCK,
        }
        return switcher.get(idx, SHOW_TICKET)

    # Map a product to it's start offer value.
    def product_to_start_offer(self, product):
        switcher = {
            SHOW_TICKET: 120,
            BOOK: 40,
            CLOCK: 20,
        }
        return switcher.get(product, 20)

    # Map a product to it's number of optional values -
    # also the number of columns in the csv file that belongs to the matching product.
    def product_to_num_of_options(self, product):
        switcher = {
            SHOW_TICKET: 1,
            BOOK: 4,
            CLOCK: 4,
        }
        return switcher.get(product, 1)

    def set_results(self, results):
        for result in results:
            count = NUM_OF_PRODUCTS
            for i in range(0, NUM_OF_PRODUCTS):
                cur_product = self.index_to_product(i)
                estimated_value = result[i]
                highest_offer = self.product_to_start_offer(cur_product) - self.JUMPS

                for j in range(self.product_to_num_of_options(cur_product)):
                    # As long as the player did not drop from the game,
                    # it means he rose the offer by the value of a JUMP.
                    # The opponent does the same and so the offer rises by 2 JUMPs.
                    if (result[count + j] != DROP) and (result[count + j] != ''):
                        highest_offer += (2 * self.JUMPS)

                count += self.product_to_num_of_options(cur_product)

                p_b = ProductBid(cur_product, estimated_value, str(highest_offer))
                self.results_per_product[i].append(p_b)
