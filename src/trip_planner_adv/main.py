#!/usr/bin/env python
import sys
import warnings

from datetime import datetime
from textwrap import dedent

from trip_planner_adv.crew import TripPlannerAdv

warnings.filterwarnings("ignore", category=SyntaxWarning, module="pysbd")

# This main file is intended to be a way for you to run your
# crew locally, so refrain from adding unnecessary logic into this file.
# Replace with inputs you want to test with, it will automatically
# interpolate any tasks and agents information

def gather_inputs():
    print("## Welcome to Trip Planner Crew")
    print('-------------------------------')
    origin = input(
        dedent("""
        From where will you be traveling from?
        """))
    cities = input(
        dedent("""
        Which City you are interested in visiting?
        """))
    date_range = input(
        dedent("""
        What is the date range you are interested in traveling?
        """))
    interests = input(
        dedent("""
        What are some of your high level interests and hobbies?
        """))
    return {
        'origin': origin,
        'cities': cities,
        'date_range': date_range,
        'interests': interests
    }
def run():
    """
    Run the crew.
    """

    # Test Data
    inputs = {
        'origin': "Mumbai",
        'cities': "London",
        'date_range': "1-Jun-2025 to 3-Jun-2025",
        'interests': "Museum, Music, Food"
    }
    inputs = gather_inputs()
    
    try:
        TripPlannerAdv().crew().kickoff(inputs=inputs)
    except Exception as e:
        raise Exception(f"An error occurred while running the crew: {e}")


def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        TripPlannerAdv().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        TripPlannerAdv().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        'origin': "Mumbai",
        'cities': "London",
        'date_range': "1-Jun-2025 to 3-Jun-2025",
        'interests': "Museum, Music, Food"
    }
    try:
        TripPlannerAdv().crew().test(n_iterations=int(sys.argv[1]), eval_llm=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while testing the crew: {e}")
