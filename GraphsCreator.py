import matplotlib.pyplot as plt
import numpy as np

from Auctions import NUM_OF_PRODUCTS

HIGHEST_OFFER = 1
ESTIMATED_VALUE = 0

ESTIMATED_VALUE_LABEL = 'ESTIMATED VALUES'
AVERAGE_ESTIMATED_VALUE_LABEL = 'AVERAGE ESTIMATED VALUE'
AVERAGE_OFFER_LABEL = 'AVERAGE OFFER'
PRODUCTS_LABEL = 'PRODUCTS'
AUCTIONS_LABEL = 'AUCTIONS'
PRICE_LABEL = 'PRICE'
RELATION_LABEL = 'RELATION'


# Create graphs for each product in the given auction.
def create_graphs_per_product(auction):
    for product in auction.products:
        create_product_graph(auction, product)


# Calculate the averages of the estimated value and the highest offer of the given auction.
def calc_averages_of_auction(auction):
    average_est_value = calc_average_of(auction.results_per_product, ESTIMATED_VALUE)
    average_offer = calc_average_of(auction.results_per_product, HIGHEST_OFFER)
    return average_est_value, average_offer


# Create a multiple bars graph accordingly to the given params.
def create_multiple_bars_graph(n_groups, x_values, y_values, auctions):
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.35
    opacity = 0.8

    rects1 = plt.bar(index, x_values, bar_width,
                     alpha=opacity,
                     color='b',
                     label=AVERAGE_ESTIMATED_VALUE_LABEL)

    rects2 = plt.bar(index + bar_width, y_values, bar_width,
                     alpha=opacity,
                     color='r',
                     label=AVERAGE_OFFER_LABEL)

    # This is a graph for a single auction.
    if len(auctions) == 1:
        plt.xlabel(PRODUCTS_LABEL)
        plt.title(auctions[0].get_auction_name())
        plt.xticks(index + bar_width - 0.2, (i.name for i in auctions[0].products))
    # This is a graph for all the auctions.
    else:
        plt.xlabel(AUCTIONS_LABEL)
        plt.xticks(index + bar_width - 0.2, (i.get_auction_name() for i in auctions))

    plt.ylabel(PRICE_LABEL)
    plt.legend()
    plt.tight_layout()
    plt.show()


# Create a graph for the given auction.
def create_auction_graph(auction):
    average_est_value, average_offer = calc_averages_of_auction(auction)

    print('\n', auction.get_auction_name())
    print("ESTIMATED VALUES: ", average_est_value)
    print("OFFERS: ", average_offer)

    create_multiple_bars_graph(NUM_OF_PRODUCTS, average_est_value, average_offer, [auction])


# Calculate the average of the given values.
def calc_average(values):
    sum = 0
    for value in values:
        sum += value

    return sum / len(values)


# Create graphs for all the auctions together.
def create_all_auctions_graphs(auctions):
    total_actions_average_est_value = []
    total_actions_average_offers = []

    # Iterate the given auctions and create a graph for each auction.
    for auction in auctions:
        average_est_values, average_offers = calc_averages_of_auction(auction)
        auction_average_est_value = calc_average(average_est_values)
        auction_average_offer = calc_average(average_offers)

        print('\n', auction.get_auction_name())
        print("ESTIMATED VALUES: ", auction_average_est_value)
        print("OFFERS: ", auction_average_offer)

        total_actions_average_est_value.append(auction_average_est_value)
        total_actions_average_offers.append(auction_average_offer)

    create_multiple_bars_graph(len(auctions), total_actions_average_est_value, total_actions_average_offers, auctions)
    create_partial_graph(auctions, total_actions_average_est_value, total_actions_average_offers)


# Create a graph of the partial values of the auctions.
def create_partial_graph(auctions, total_actions_average_est_value, total_actions_average_offers):
    partial = []
    for i in range(len(total_actions_average_est_value)):
        partial.append(total_actions_average_offers[i] / total_actions_average_est_value[i])

    print('\n', "PARTIAL: ", partial)

    plt = create_bar_graph([i.get_auction_name() for i in auctions], partial)
    plt.xlabel(AUCTIONS_LABEL)
    plt.ylabel(RELATION_LABEL)

    plt.show()


# Create a bar graph accordingly to the given columns names and value.
def create_bar_graph(columns_names, columns_values):
    columns = columns_names
    pos = np.arange(len(columns_names))
    var_one = np.array(columns_values)

    plt.bar(pos, var_one, color='green', edgecolor='black', width=0.5)
    plt.xticks(pos, columns)

    return plt


# Calculate the average offer for each estimated value of the given product.
def calc_average_highest_offer_per_est_value(results_per_product, product):
    sum_per_est_value = {}
    average_per_est_value = {}
    num_of_results_per_est_value = {}

    # Iterate the optional estimated values of the given product and reset to zero.
    for v in product.optional_values:
        sum_per_est_value[v] = 0
        num_of_results_per_est_value[v] = 0

    # Iterate the product bids of the given product and sum the offers of each estimated value.
    for p_b in results_per_product[product.index]:
        sum_per_est_value[int(p_b.estimated_value)] += int(p_b.highest_offer)
        num_of_results_per_est_value[int(p_b.estimated_value)] += 1

    # Iterate the sums of each estimated value and calculate the average.
    for v in sum_per_est_value:
        if num_of_results_per_est_value[v] == 0:
            average_per_est_value[v] = 0
        else:
            average_per_est_value[v] = sum_per_est_value[v] / num_of_results_per_est_value[v]

    return average_per_est_value


# Create a product graph accordingly to the given product and auction.
def create_product_graph(auction, product):
    plt = create_bar_graph(product.optional_values,
                           list(calc_average_highest_offer_per_est_value
                                (auction.results_per_product, product).values()))
    plt.xlabel(ESTIMATED_VALUE_LABEL)
    plt.ylabel(AVERAGE_OFFER_LABEL)
    plt.title(product.name)
    plt.show()


# Calculate the average of the highest offer or the estimated value accordingly to the given average_of param.
def calc_average_of(results_per_product, average_of):
    avgs = {0: [], 1: [], 2: []}

    # Iterate products.
    for product in results_per_product:
        sum = 0
        count = 0
        # Iterate product bids of the current product.
        for p_b in results_per_product[product]:
            count += 1
            if average_of == HIGHEST_OFFER:
                sum += p_b.highest_offer
            elif average_of == ESTIMATED_VALUE:
                sum += p_b.estimated_value

        avgs[product] = sum / count
    return list(avgs.values())
