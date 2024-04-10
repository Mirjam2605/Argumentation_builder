class ArgumentationFramework:
    def __init__(self):
        self.arguments = set()
        self.attacks = set()

    def add_argument(self, arg):
        self.arguments.add(arg)

    def add_attack(self, attacker, target):
        self.attacks.add((attacker, target))

    def is_conflict_free(self, argument_set):
        a = [(attacker, target) for attacker, target in self.attacks if (attacker in argument_set and target in argument_set)]
        print(a)
        return not bool(len(a))

    def is_admissible(self, argument_set):
        set_attacker = [attacker for attacker, target in self.attacks if target in argument_set]
        admissible = True
        if len(set_attacker):
            set_defence_targets = [target for attacker, target in self.attacks if attacker in argument_set]
            admissible = [True if attacker in set_defence_targets else False for attacker in set_attacker]           
        return self.is_conflict_free(argument_set) and all(admissible)

    # Implement other semantics as needed

# Example usage: This needs to be interpreted from an input file: YAML
af = ArgumentationFramework()
af.add_argument("A")
af.add_argument("B")
af.add_argument("C")
af.add_argument("D")
af.add_attack("A", "B")
af.add_attack("B", "C")
af.add_attack("C", "D")

# Check if a set of arguments is conflict-free
print(af.is_conflict_free({"A", "C"}))  # True

# Check if a set of arguments is admissible
print(af.is_admissible({"A", "C"}))  # True
