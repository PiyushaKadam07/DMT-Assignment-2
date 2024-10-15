import itertools
from collections import defaultdict

# Function to read transactions from file
def load_transactions(filename):
    transactions = []
    with open(filename, 'r') as file:
        for line in file:
            transaction = set(line.strip().split())
            transactions.append(transaction)
    return transactions

# Function to calculate the support count for itemsets
def calculate_support(transactions, itemsets):
    support_count = defaultdict(int)
    for transaction in transactions:
        for itemset in itemsets:
            if itemset.issubset(transaction):
                support_count[itemset] += 1
    return support_count

# Function to generate candidate itemsets of size k
def generate_candidates(frequent_itemsets, k):
    candidates = set()
    frequent_items = list(frequent_itemsets)
    for i in range(len(frequent_items)):
        for j in range(i + 1, len(frequent_items)):
            union_set = frequent_items[i] | frequent_items[j]
            if len(union_set) == k:
                candidates.add(union_set)
    return candidates

# Apriori algorithm
def apriori(filename, min_support_percent):
    transactions = load_transactions(filename)
    total_transactions = len(transactions)
    min_support_count = (min_support_percent / 100) * total_transactions
    
    # Step 1: Generate frequent 1-itemsets
    itemsets_1 = set(itertools.chain(*transactions))
    candidates_1 = [{item} for item in itemsets_1]
    support_1 = calculate_support(transactions, candidates_1)
    
    # Filter by min support count
    frequent_itemsets = {itemset: count for itemset, count in support_1.items() if count >= min_support_count}
    
    all_frequent_itemsets = dict(frequent_itemsets)
    k = 2
    
    # Step 2: Generate frequent itemsets of size k
    while frequent_itemsets:
        candidates_k = generate_candidates(frequent_itemsets, k)
        support_k = calculate_support(transactions, candidates_k)
        
        frequent_itemsets = {itemset: count for itemset, count in support_k.items() if count >= min_support_count}
        all_frequent_itemsets.update(frequent_itemsets)
        
        k += 1
    
    # Output frequent itemsets
    print("Frequent itemsets:")
    for itemset, count in all_frequent_itemsets.items():
        print(f"{set(itemset)}: {count}")

# Main function to execute apriori
if __name__ == '__main__':
    import sys
    if len(sys.argv) != 3:
        print("Usage: myapriori <filename> <min_support_percent>")
        sys.exit(1)
    
    filename = sys.argv[1]
    min_support_percent = float(sys.argv[2])
    
    apriori(filename, min_support_percent)
