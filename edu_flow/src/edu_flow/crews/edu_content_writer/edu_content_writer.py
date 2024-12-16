from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task, before_kickoff, after_kickoff

# Uncomment the following line to use an example of a custom tool
# from edu_content_writer.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool
import os
from dotenv import load_dotenv
load_dotenv()

agent_llm = LLM(
	base_url=os.getenv("OLLAMA_BASE_URL"), 
	model=os.getenv("OLLAMA_MODEL"),
	api_key = os.getenv("FAKE_KEY")
)
@CrewBase
class EduContentWriter():
	"""EduContentWriter crew"""

	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@before_kickoff # Optional hook to be executed before the crew starts
	def pull_data_example(self, inputs):
		# Example of pulling data from an external API, dynamically changing the inputs
		inputs['extra_data'] = "This is extra data"
		return inputs

	@after_kickoff # Optional hook to be executed after the crew has finished
	def log_results(self, output):
		# Example of logging results, dynamically changing the output
		print(f"Results: {output}")
		return output

	@agent
	def writer(self) -> Agent:
		return Agent(
			config=self.agents_config['writer'],
			# tools=[MyCustomTool()], # Example of custom tool, loaded on the beginning of file
			verbose=True,
   			llm=agent_llm
		)

	@agent
	def editor(self) -> Agent:
		return Agent(
			config=self.agents_config['editor'],
			verbose=True,
   			llm=agent_llm
		)

	@agent
	def quality_control(self) -> Agent:
		return Agent(
			config=self.agents_config['quality_control'],
			verbose=True,
   			llm=agent_llm
		)
  
	@agent
	def producer(self) -> Agent:
		return Agent(
			config=self.agents_config['producer'],
			verbose=True,
   			llm=agent_llm
		)

	@task
	def writer_task(self) -> Task:
		return Task(
			config=self.tasks_config['writer_task'],
		)

	@task
	def editor_task(self) -> Task:
		return Task(
			config=self.tasks_config['editor_task']
		)
  
	@task
	def quality_control_task(self) -> Task:
		return Task(
			config=self.tasks_config['quality_task']
		)
  
	@task
	def producer_task(self) -> Task:
		return Task(
			config=self.tasks_config['producer_task']
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the EduContentWriter crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=True,
			# process=Process.hierarchical, # In case you wanna use that instead https://docs.crewai.com/how-to/Hierarchical/
		)
