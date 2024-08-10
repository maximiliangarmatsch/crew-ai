import sys
from finance_crew.crew import FinnaceCrew


def run():
    final_response = FinnaceCrew().crew().kickoff()
    print(final_response)

def train():
    try:
        final_response = FinnaceCrew().crew().train(n_iterations=int(sys.argv[1]))
        print(final_response)
    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")
