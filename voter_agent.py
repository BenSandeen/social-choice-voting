class Voter:
    def __init__(self, name, weight, votes):
        self.name = name
        self.weight = weight
        self.Alex, self.Brad, self.Cindy, self.David, self.Erik, self.Frank, self.Greg = votes

    def __repr__(self):
        return f"Name: {self.name},\tweight: {self.weight},\tAlex: {self.Alex},\tBrad: {self.Brad}," \
            f"\tCindy: {self.Cindy},\tDavid: {self.David},\tErik: {self.Erik},\tFrank: {self.Frank}," \
            f"\tGreg: {self.Greg}\n"
