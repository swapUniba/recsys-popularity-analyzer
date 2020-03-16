from lenskit.datasets import ML1M


def run(recs, algorithm_name, ratings):
    items = set(ML1M('../datasets/ml-1m').movies.index.values.flatten())

    covered_items = set(recs[['item']].values.flatten())
    coverage_percentage = len(covered_items) / len(items) * 100 

    print('Covered items: ', len(covered_items), ' ({}%)'.format(coverage_percentage))
    ########################### Serializing results ###########################
    with open('results/catalog-coverage.csv', 'a', newline='') as f:
        f.write("%s,%d,%f\n"%(algorithm_name, len(covered_items), coverage_percentage))