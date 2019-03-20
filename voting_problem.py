import voter_agent
import csv


def create_voters(filename="voters.csv"):
    voters = []

    with open(filename, 'r') as infile:
        csv_file = csv.reader(infile)
        for row in csv_file:
            if "Name" in row:  # Skip header row
                continue

            name = row[0]
            weight = row[1]
            votes = row[2:]
            voters.append(voter_agent.Voter(name, weight, votes))

    return voters


if __name__ == "__main__":
    print(create_voters())
