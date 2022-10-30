import itertools

class Party:
    def __init__(self, name):
        self.name = name
        self.state = []
        self.column_size = 6

    def add_state(self, name):
        self.state.append(name)

    def serialise(self):
        strings = []
        strings.append(self.name)
        strings.append("-" * self.column_size)
        for state in self.state:
            assert len(state) < self.column_size
            padding_len = self.column_size - len(state)
            padded_str = " " * (padding_len // 2) + state + " " * (self.column_size - (len(state) + padding_len // 2))
            strings.append(padded_str)
        return strings

class Protocol:
    def __init__(self, parties, max_width=50):
        self.parties = parties
        self.max_width = max_width
        self.interval = int(max_width / len(self.parties))
        self.events = []

    def compute(self, parties_computations):
        parties_computations = list(map(lambda x: (self.parties.index(x[0]), x[1]), parties_computations))
        string = ""
        for party_idx in range(len(self.parties)):
            string += " " * self.interval
            computation = ([x for x in parties_computations if x[0] == party_idx] + [(None, "")])[0][1]
            string += computation

        self.events.append(string)

    def interaction(self, sender, receiver, name):
        sender_idx = self.parties.index(sender)
        receiver_idx = self.parties.index(receiver)
        start_idx = min(sender_idx, receiver_idx)
        end_idx = max(sender_idx, receiver_idx)

        string = " " * self.interval * (start_idx + 1)
        string += " " * int(self.interval / 2) * (start_idx + 1)
        string += name
        string += "\n"
        string += " " * len(self.parties[min(sender_idx, receiver_idx)].name)
        string += " " * self.interval * (start_idx + 1)
        if receiver_idx < sender_idx:
            string += "<"            
        string += "-" * (self.interval * (end_idx - start_idx) - 1)
        if sender_idx < receiver_idx:
            string += ">"

        self.events.append(string)

    def print_parties(self):
        parties = list(map(lambda x: x.serialise(), self.parties))
        parties = list(zip(*itertools.zip_longest(*parties, fillvalue="")))
        length = max(len(party) for party in parties)
        strings = []
        for i in range(length):
            string = ""
            for party in parties:
                string += " " * self.interval
                string += party[i]
            strings.append(string)
        for string in strings:
            print(string)

    def render(self):
        print()
        self.print_parties()
        for event in self.events:
            print(event)
        print()

alice = Party('Alice')
alice.add_state('  M  ')
alice.add_state('  a  ')

bob = Party('Bob')
bob.add_state('')
bob.add_state(' b ')

diffie_hellman = Protocol([alice, bob])
diffie_hellman.interaction(alice, bob, 'A = g^a')
diffie_hellman.interaction(bob, alice, 'B = g^b')

diffie_hellman.compute([(alice, 'k = B^a'), (bob, 'k = A^b')])
diffie_hellman.interaction(alice, bob, 'e = Enc(k, M)')
diffie_hellman.compute([(bob, '       M = Dec(k, e)')])

diffie_hellman.render()
