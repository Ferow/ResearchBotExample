from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff
from typing import List

from pydantic import BaseModel
# Check our tools documentations for more information on how to use them
from crewai_tools import SerperDevTool

import os
from dotenv import load_dotenv
load_dotenv()

agent_llm = LLM(
	base_url=os.getenv("OLLAMA_BASE_URL"), 
	model=os.getenv("OLLAMA_MODEL"),
	api_key = os.getenv("FAKE_KEY")
)

class Section(BaseModel):
    title: str
    high_level_goal: str
    why_important: str
    sources: List[str]
    content_outline: List[str]
    
class EducationalPlan(BaseModel):
    sections: List[Section]

@CrewBase
class Edu_Research_Crew():
	"""Edu_Research_Crew crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def planner(self) -> Agent:
		return Agent(
			config=self.agents_config['planner'],
			tools=[SerperDevTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
			llm=agent_llm
		)

	@agent
	def developer(self) -> Agent:
		return Agent(
			config=self.agents_config['developer'],
			verbose=True,
			llm=agent_llm
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
		)

	@task
	def reporting_task(self) -> Task:
		return Task(
			config=self.tasks_config['planning_task'],
			output_pydantic=EducationalPlan
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the EduResearch crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
