"""
    Market Basket Analysis

    Prediction of next item which user can purchase based on previous purcahse history
    and current purchased items.
"""
from typing import Dict, Union, Tuple

import pandas as pd
from collections import Counter
from itertools import permutations


n_transactions = 0
n_items = 0


def read_data() -> pd.DataFrame:

    global n_transactions, n_items

    df = pd.read_csv("data/basket.csv", index_col='ID')

    n_transactions, n_items = df.shape
    print(n_transactions, n_items)
    # print(df)

    return df


def get_items_freq(df: pd.DataFrame) -> Counter:

    freq = Counter()

    for _, row in df.iterrows():
        row_no_nan = filter(pd.notna, row)
        row_no_nan_no_dups = set(row_no_nan)
        freq.update(row_no_nan_no_dups)

    # print(freq)

    return freq


def generate_support_filtered(frequency: Union[Counter, Dict[Tuple[str, str], int]], min_thres: float = 0.0) -> Dict[Union[str, Tuple[str, str]], float]:
    support = {}
    for item, freq in frequency.items():
        supp = freq / n_transactions

        if supp >= min_thres:
            support[item] = supp

    # print(len(support), support)

    return support


def get_combi_items_freq(df: pd.DataFrame, single_items_freq: Counter):

    permuts = list(permutations(single_items_freq.keys(), 2))

    print(len(permuts))

    freq = {}
    for _, row in df.iterrows():
        row = set(filter(pd.notna, row))
        for permut in permuts:
            if set(permut).issubset(row):
                if permut in freq:
                    freq[permut] += 1
                else:
                    freq[permut] = 1

    # print(freq)

    return freq


def generate_assoc_rule(single_support: dict[str, float], combi_support: Dict[Tuple[str, str], float], min_thres: float = 0.0):

    df = pd.DataFrame(None,
                      columns=["antecedents", "consequents", "antecedant support", "consequent support", "support",
                               "confidence", "lift"]
                      )

    for (ante, conseq), support in combi_support.items():
        supp_a = single_support[ante]
        supp_c = single_support[conseq]
        confidence = support / supp_a
        lift = confidence / supp_c

        if confidence >= min_thres:
            df.loc[len(df.index)] = [
                ante,
                conseq,
                supp_a,
                supp_c,
                support,
                confidence,
                lift
            ]

    print(df.to_string())

    return df


if __name__ == '__main__':
    df = read_data()

    freq = get_items_freq(df)

    combi_freq = get_combi_items_freq(df, freq)

    single_support = generate_support_filtered(freq)
    combi_support = generate_support_filtered(combi_freq, 0.005)

    rules_df = generate_assoc_rule(single_support, combi_support, 0.1)

    print(rules_df.sort_values(by=['lift'], ascending=False).head(10))

