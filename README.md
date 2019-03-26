To run the program, just run `python voting_problem.py` from within this folder.

To manually change the voter weights, change the values in the `voter_weights.csv` file.  Feel free to add voters or
just change the existing values of the voters.

To use the voters in the CSV file, open up the `voting_problem.py` file and, in the `if __name__ == "__main__":`
section, make sure the line that says `voters = create_voters()` is uncommented and that the line
`voters = create_random_voters(num_voters=9, max_weight=10)` is commented out.  To use the randomly generated voters, do
the opposite, and feel free to change the parameters in the call to `create_random_voters()`.