import yaml
import networkx as nx
import matplotlib.pyplot as plt

class ArgumentationFramework:
    def __init__(self):
        self.arguments = set()
        self.attacks = set()

    def add_argument(self, arg):
        self.arguments.add(arg)

    def add_attack(self, attacker, target):
        assert attacker in self.arguments and target in self.arguments, "Argument not in Argumentation Framework"
        self.attacks.add((attacker, target))

    def is_conflict_free(self, argument_set):
        # check if there are any attacks between set members
        conflicts = [(attacker, target) for attacker, target in self.attacks if (attacker in argument_set and target in argument_set)]
        return not bool(len(conflicts))

    def is_admissible(self, argument_set):
        # check conflict-free
        if not self.is_conflict_free(argument_set):
            return False
        # Find arguments that attack arguments in argument set
        set_attacker = [attacker for attacker, target in self.attacks if target in argument_set]
        admissible = True
        # Proof if attackers of argument set are attacked by elements of argument set
        if len(set_attacker):
            set_defence_targets = [target for attacker, target in self.attacks if attacker in argument_set]
            admissible = [True if attacker in set_defence_targets else False for attacker in set_attacker]           
        return all(admissible)

# Load your YAML data (replace 'your_yaml_file.yaml' with your actual file)
def load_yaml(file_path):
    with open(file_path, 'r') as file:
        return yaml.safe_load(file)
    
# define Argument dictionary
def create_arguments(data):
    arguments_dict = {}
    for key, value in data.items():
        if ">" in key:
            # Split the string using the arrow symbol
            supp, conc = key.split("->")
            # Remove leading/trailing spaces
            supp = supp.strip()
            conc = conc.strip()
            # Create the dictionary
            arguments_dict[supp] = conc
        else:
            arguments_dict [key] = key
    return arguments_dict

# Construct the argumentation graph
def create_argumentation_graph(data):
    G = nx.MultiDiGraph()
    for key, value in data.items():
        G.add_node(key)
        if key.startswith('not_'):
            # Remove the 'not_' prefix to get the attacked node
            attacked_node = key[4:]
            attacker = key
            G.add_edge(attacked_node, key)
            for key, value in data.items():
                if attacker[4:] in key:
                     #Add the attack edge
                    G.add_edge(attacker, key)
    G.remove_edges_from(nx.selfloop_edges(G))
    # Erstelle ein neues Mapping, das die Knoten als "A1", "A2", "A3", ... benennt
    new_mapping = {node: f"A{idx}" for idx, node in enumerate(G.nodes(), start=1)}
    G = nx.relabel_nodes(G, new_mapping)
    return G


# Load your YAML data (replace 'your_yaml_file.yaml' with your actual file)
yaml_data = load_yaml('statement.yml')

#create arguments
arguments = create_arguments(yaml_data)

# Enumerate through the original dictionary and assign names
arguments_dict = {}
for i, (key, value) in enumerate(arguments.items(), start=1):
    new_key = f"A{i}"
    arguments_dict[new_key] = {'support': key, 'conclusion': value}

print("Arguments: ", arguments_dict)

# Create the argumentation graph
argumentation_graph = create_argumentation_graph(arguments)

# create Argumentation Framework out of graph
af = ArgumentationFramework()
for node in argumentation_graph.nodes:
    af.add_argument(node)

for edge in argumentation_graph.edges:
    af.add_attack(edge[0], edge[1])
  
# Check if a set of arguments is conflict-free
set_arg = {"A1", "A4"}
if af.is_conflict_free(set_arg):
    print(f"{set_arg} is conflict free")

# Check if a set of arguments is admissible
if af.is_admissible(set_arg):
    print(f"{set_arg} is admissible")

fig = plt.figure()
fig.set_figheight(10)
fig.set_figwidth(12)
pos = nx.spring_layout(argumentation_graph, seed=42)
nx.draw(argumentation_graph, pos, with_labels=True, node_size=800, node_color='skyblue', font_size=10)
plt.title("Argumentation Graph")
plt.savefig('Argumentation_Graph.png')
plt.show()
plt.close()





