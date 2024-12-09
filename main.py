 import csv
 from itertools import combinations
 import networkx as nx
 import matplotlib.pyplot as plt
 import pandas as pd

 data = {
 'Antecedent': [('Previous Attempts',), ('Previous Attempts',), ('Abuse
 History',), ('Social Isolation',),
 ('Childhood Trauma',), ('Financial Problem',), ('Abuse
 History',), ('Childhood Trauma',),
 ('Social Isolation',), ('Self-Harm History',), ('Abuse
 History', 'Social Isolation')],
 'Consequent': [('Abuse History',), ('Childhood Trauma',), ('Childhood
 Trauma',), ('Childhood Trauma',),
 ('Social Isolation',), ('Childhood Trauma',), ('Childhood
 Trauma',), ('Social Isolation',),
 ('Childhood Trauma',), ('Financial Problem',), ('Childhood
 Trauma',)],
 'Support': [0.2, 0.3, 0.25, 0.18, 0.15, 0.22, 0.28, 0.21, 0.27, 0.19,
 0.23],
 'Confidence': [0.6, 0.7, 0.65, 0.5, 0.55, 0.6, 0.72, 0.67, 0.75, 0.58,
 0.68]
 }

 df = pd.DataFrame(data)

 def apriori_analysis(transactions, min_support):
 C1 = {}
 for transaction in transactions:
 for item in transaction:
 			if item in C1:
 				C1[item] += 1
 			else:
 C1[item] = 1
 L1 = {key: value for key, value in C1.items() if value/len(transactions) >= min_support}
 L = [L1]
 k = 2
 while len(L[k-2]) > 0:
 Ck = {}
 for transaction in transactions:
 	combos = combinations(transaction, k)
 for combo in combos:
 if combo in Ck:
 	Ck[combo] += 1
 else:
 Ck[combo] = 1
 	Lk = {key: value for key, value in Ck.items() if value/len(transactions) >=min_support}
 	 	L.append(Lk)
  	k += 1
       return [item for sublist in L for item in sublist.keys()]

 def generate_association_rules(frequent_itemsets, transactions,min_confidence):
 rules = []
 for itemset in frequent_itemsets:
 for i in range(1, len(itemset)):
 antecedents = [x for x in combinations(itemset, i)]
 for antecedent in antecedents:
 consequent = tuple([item for item in itemset if item not in
 antecedent])
 antecedent_support = sum([1 for transaction in transactions if
 set(antecedent).issubset(set(transaction))])
 both_support = sum([1 for transaction in transactions if
 set(antecedent + consequent).issubset(set(transaction))])
 try:
 confidence = both_support / antecedent_support
 if confidence >= min_confidence:
 rules.append((antecedent, consequent))
 except ZeroDivisionError:
 Pass
 return rules

 def plot_network_graph(association_rules):
 	G = nx.DiGraph()
 	for rule in association_rules:
 antecedent, consequent = rule
 G.add_node(antecedent)
 		 G.add_node(consequent)
 		 G.add_edge(antecedent, consequent)
 pos = nx.spring_layout(G)
 nx.draw(G, pos, with_labels=True, font_size=10, font_color="black",
 	node_size=2000, node_color="skyblue", font_weight="bold", arrowsize=20)
 plt.show()

 def plot_bar_graph(file_path):
 df = pd.read_csv(file_path)
 elements = [element for column in df.columns for element in df[column]]
 	element_counts = pd.Series(elements).value_counts()
 plt.figure(figsize=(10, 6))
 element_counts.plot(kind='bar', color='skyblue')
 plt.title('Frequency of Elements')
 plt.xlabel('Elements')
 	plt.ylabel('Frequency')
 plt.show()

 def scatterplot(rules):
 import matplotlib.pyplot as plt
 import seaborn as sns
 	plt.figure(figsize=(8, 6))
 sns.scatterplot(x='Support', y='Confidence', data=df)
 	plt.title('Scatter Plot of Support vs Confidence')
 plt.show()

 def heatmap(rules):
 	plt.figure(figsize=(10, 8))
 	pivot_table = df.pivot_table(index='Antecedent', columns='Consequent',
 values='Support', fill_value=0)
 sns.heatmap(pivot_table, annot=True, cmap='YlGnBu')
 	plt.title('Heatmap of Association Rules')
 	plt.show()

 def choose_and_input_attributes(file_path, attributes):
 try:
 # Get the number of transactions from the user
 num_transactions = int(input("Enter the number of transactions: "))
 # Get chosen attributes from the user
 		chosen_attributes = input("Enter the attributes to choose
 (comma-separated): ").split(',')
 # Validate chosen attributes
 for attr in chosen_attributes:
 			if attr not in attributes:
 print(f"Error: '{attr}' is not a valid attribute. Please
 		choose from {', '.join(attributes)}.")
 return
 # Get transactions from the user
 transactions = []
 for i in range(num_transactions):
 transaction = []
 for attr in chosen_attributes:
 value = input(f"Enter value for {attr} in transaction {i+1}:
 ")
 transaction.append(value)
 transactions.append(transaction)
 # Write transactions to the CSV file
 with open(file_path, 'w', newline='') as file:
 writer = csv.writer(file)
 writer.writerows(transactions)
 print(f"Values successfully written to {file_path}")
     except Exception as e:
 	print(f"Error: {e}")

 def menu_driven_program():
 	file_path = "short2.csv"
 	transactions = []
 	with open(file_path, 'r') as file:
reader = csv.reader(file)
 transactions = [list(row) for row in reader]
 attributes = ["Abuse History", "Social Isolation", "Previous Attempts",
 	"Media Bullying", "Self-Harm History", "Financial Problem", "Childhood
 Trauma"]
 while True:
 print("\nMenu:")
 print("1. Apriori Analysis")
 print("2. Association Rules")
 print("3. Plot Network Graph")
 print("4. Plot Scatter Plot")
 print("5. Plot Heat Map")
 print("6. Input Attributes to CSV")
 print("6. Exit")
 choice = input("Enter your choice (1-6): ")
 		if choice == '1':
 min_support = 2/len(transactions)
 frequent_itemsets = apriori_analysis(transactions, min_support)
 			 print("Apriori Analysis Result:")
 			 print(frequent_itemsets)
 		elif choice == '2':
 min_confidence = 0.65
 			 rules = generate_association_rules(frequent_itemsets,
 			 transactions, min_confidence)
 			 print("Association Rules:")
 for rule in rules:
 		print(f"{rule[0]} => {rule[1]}")
 elif choice == '3':
 plot_network_graph(rules)
 elif choice == '4':
 			scatterplot(rules)
 elif choice == '5':
 			heatmap(rules)
 		elif choice == '6':
 plot_bar_graph(file_path)
elif choice == '7':
 			choose_and_input_attributes(file_path, attributes)
 elif choice == '8':
 print("Exiting the program.")
 Break
 else:
 print("Invalid choice. Please enter a number between 1 and 6.")
 if _name_ == "_main_":
 		menu_driven_program()

