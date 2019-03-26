class Voter:
    def __init__(self, name, weight, votes):
        self.name = name
        self.weight = int(weight)
        self.Alex, self.Bart, self.Cindy, self.David, self.Erik, self.Frank, self.Greg = votes
        self.votes = {
            "Alex":  self.Alex,
            "Bart":  self.Bart,
            "Cindy": self.Cindy,
            "David": self.David,
            "Erik":  self.Erik,
            "Frank": self.Frank,
            "Greg":  self.Greg
        }

    def get_ranking_order(self):
        return list(sorted(self.votes.items(), key=lambda x: x[1]))

    def __repr__(self):
        return f"Name: {self.name},\tweight: {self.weight},\tAlex: {self.Alex},\tBart: {self.Bart}," \
            f"\tCindy: {self.Cindy},\tDavid: {self.David},\tErik: {self.Erik},\tFrank: {self.Frank}," \
            f"\tGreg: {self.Greg}\n"

    def __lt__(self, other):
        return self.name < other.name
