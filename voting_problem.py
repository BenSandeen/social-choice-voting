import voter_agent
import csv
import itertools
import random
import math


# Read this in from file if there's time
candidates = ["Alex", "Bart", "Cindy", "David", "Erik", "Frank", "Greg"]


def create_voters(filename="voter_weights.csv"):
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


def kemeny_ranking(voters):
    """Yes, I know this is hideous code, but it should get the job done.  The implementation is based on Wikipedia's
    explanation of Kemeny voting: https://en.wikipedia.org/wiki/Kemeny%E2%80%93Young_method#Description
    """
    results = {}

    # For each possible pair (head-to-head matchup), determine which is preferred by each voter and tally up the results
    for pair in itertools.permutations(candidates, 2):
        if pair[0] not in results.keys():
            results[pair] = 0
        # print(pair)

        for voter in voters:
            # Voter ranks first candidate in `pair` is ranked above second candidate
            if voter.votes[pair[0]] < voter.votes[pair[1]]:
                results[pair] += 1 * voter.weight
            # Voter ranks candidates as equal
            elif voter.votes[pair[0]] == voter.votes[pair[1]]:
                results[pair] += 0.5 * voter.weight
            # Voter ranks first candidate in `pair` is ranked below second candidate
            else:
                results[pair] += 0 * voter.weight

    order_scores = {}

    # Check to see which ranking is least disagreed with
    for order in itertools.permutations(candidates, 7):
        order_scores[order] = 0
        for pair, votes in results.items():
            # If the first item in `pair` is ranked higher than the second in the order being tested...
            if order.index(pair[0]) < order.index(pair[1]):
                order_scores[order] += votes

    # Settle ties by just returning the first result
    return list(sorted(order_scores.items(), key=lambda x: x[1], reverse=True))[0]


def bucklin_ranking(voters):
    results = []
    while len(results) < 7:
        found_candidate_this_iteration = False
        for k in range(1, 7):
            for candidate in candidates:
                if candidate in results:
                    continue
                count = 0
                for voter in voters:
                    if candidate in [cand for cand, ranking in voter.get_ranking_order()[:k]]:
                        count += 1 * voter.weight

                if count >= math.ceil((len(voters) + 1) / 2):  # This gets the majority of voters
                    results.append(candidate)
                    found_candidate_this_iteration = True
                    break
            if found_candidate_this_iteration:
                break

    return results


def second_order_copeland_ranking(voters):
    """Figures out which candidates defeat which other candidates and then gets Copeland scores for the defeated
    candidates to determine the second order Copeland score
    """
    copeland_order = copeland_ranking(voters)
    results = {}

    for pair in itertools.permutations(candidates, 2):
        if pair[0] not in results.keys():
            results[pair[0]] = 0
        for voter in voters:
            if voter.votes[pair[0]] < voter.votes[pair[1]]:
                # Second order Copeland takes the Copeland score of defeated candidates
                results[pair[0]] += copeland_order[pair[1]] * voter.weight

    return list(sorted(results, key=lambda x: x[1], reverse=True))


def copeland_ranking(voters):
    """Helper method for getting the Copeland scores"""
    # Candidates are the keys and the values are 2-element lists with wins first and losses second
    victories_and_defeats = {}
    for pair in itertools.permutations(candidates, 2):
        # Yes, this is inefficient, but it's easier to do it the lazy way, so that's what I'm doing :P
        victories_and_defeats[pair[0]] = [0, 0]
        for voter in voters:
            # Remember, lower ranking number means more preferred candidate
            if voter.votes[pair[0]] < voter.votes[pair[1]]:
                victories_and_defeats[pair[0]][0] += 1 * voter.weight
            elif voter.votes[pair[0]] > voter.votes[pair[1]]:
                victories_and_defeats[pair[0]][1] += 1 * voter.weight

    # Wikipedia says that the Copeland score (https://en.wikipedia.org/wiki/Copeland%27s_method) should subtract the
    # candidate's defeats from its victories, but this disagrees with lecture, which does NOT have us subtract the
    # number of defeats from the number of victories.  I implemented the version from lecture
    copeland_order = {cand: score[0] for cand, score in
                      sorted(victories_and_defeats.items(), key=lambda x: x[1][0], reverse=True)}

    return copeland_order


def create_random_voters(num_voters=4, max_weight=10):
    voters = []

    # Used for picking a voter name.  If user wants more than 26 voters, names are repeated.  Oh well.
    letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    for voter_idx in range(num_voters):
        name = letters[voter_idx]
        weight = random.uniform(0, max_weight)
        votes = random.sample(range(1, 8), 7)  # Gets random order of preference for candidates

        voter = voter_agent.Voter(name, weight, votes)
        voters.append(voter)

    return voters


def print_votes(voters):
    print("VOTES ARE AS FOLLOWS")
    for voter in sorted(voters):  # Sort them so they appear alphabetically
        print(voter, end='')

    print()


if __name__ == "__main__":
    # To use the voters in the `voter_weights.csv` file, use this line
    voters = create_voters()

    # To use the randomly generated voters, comment out the previous line and use this line instead
    # voters = create_random_voters(num_voters=9, max_weight=10)

    print_votes(voters)
    kem = kemeny_ranking(voters)

    print("Results:\t\t\t\t 1 \t\t 2 \t\t 3 \t\t 4 \t\t 5 \t\t 6 \t\t 7")
    print(f"Kemeny: \t\t\t{kem[0]}")

    buck = bucklin_ranking(voters)
    print(f"Bucklin: \t\t\t{buck}")

    sec_cope = second_order_copeland_ranking(voters)
    print(f"2nd order Copeland: {sec_cope}")
