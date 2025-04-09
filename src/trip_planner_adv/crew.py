from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task

from trip_planner_adv.tools.amadeus import AmadeusSearchTool

# If you want to run a snippet of code before or after the crew starts,
# you can use the @before_kickoff and @after_kickoff decorators
# https://docs.crewai.com/concepts/crews#example-crew-class-with-decorators

@CrewBase
class TripPlannerAdv():
    """TripPlannerAdv crew"""

    # Learn more about YAML configuration files here:
    # Agents: https://docs.crewai.com/concepts/agents#yaml-configuration-recommended
    # Tasks: https://docs.crewai.com/concepts/tasks#yaml-configuration-recommended
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    # If you would like to add tools to your agents, you can learn more about it here:
    # https://docs.crewai.com/concepts/agents#agent-tools
    @agent
    def city_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['city_expert'],
            verbose=True
        )

    @agent
    def local_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['local_expert'],
            verbose=True
        )

    @agent
    def flights_expert(self) -> Agent:
        tool = AmadeusSearchTool()
        amadeus_tools = [tool]
        
        return Agent(
            config=self.agents_config['flights_expert'],
            tools=amadeus_tools,
            verbose=True
        )

    @agent
    def travel_concierge(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_concierge'],
            verbose=True
        )

    # To learn more about structured task outputs,
    # task dependencies, and task callbacks, check out the documentation:
    # https://docs.crewai.com/concepts/tasks#overview-of-a-task
    @task
    def identify_best_city(self) -> Task:
        return Task(
            config=self.tasks_config['identify_best_city'],
        )

    @task
    def build_city_guide(self) -> Task:
        return Task(
            config=self.tasks_config['build_city_guide'],
            output_file='report1.md'
        )

    @task
    def recommend_flights(self) -> Task:
        return Task(
            config=self.tasks_config['recommend_flights'],
            output_file='report2.md'
        )

    @task
    def build_travel_plan(self) -> Task:
        return Task(
            config=self.tasks_config['build_travel_plan'],
            output_file='report.md'
        )
    
    @crew
    def crew(self) -> Crew:
        """Creates the TripPlannerAdv crew"""
        # To learn how to add knowledge sources to your crew, check out the documentation:
        # https://docs.crewai.com/concepts/knowledge#what-is-knowledge

        return Crew(
            agents=self.agents, # Automatically created by the @agent decorator
            tasks=self.tasks, # Automatically created by the @task decorator
            process=Process.sequential,
            verbose=True,
            # process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
        )
