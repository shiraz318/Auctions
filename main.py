import Auctions
import csv
import GraphsCreator


# Read the results from the given path to the result csv file and return it's rows.
def read_results(path_to_result):
    rows = []
    with open(path_to_result, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)

        # First row for the fields name.
        next(csv_reader)

        for row in csv_reader:
            rows.append(row)

    return rows


def main():

    # Create the auctions.
    auctions = [Auctions.FirstPriceAuction(read_results("Results_Files/FirstPrice.csv")),
                Auctions.SecondPriceAuction(read_results("Results_Files/SecondPrice.csv")),
                Auctions.DutchAuction(read_results("Results_Files/Dutch.csv")),
                Auctions.EnglishAuction(read_results("Results_Files/English.csv"))]

    # Create graphs for each auction.
    for auction in auctions:
        GraphsCreator.create_auction_graph(auction)

    # Create graphs for all the auctions.
    GraphsCreator.create_all_auctions_graphs(auctions)


if __name__ == '__main__':
    main()
