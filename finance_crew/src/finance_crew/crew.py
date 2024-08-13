from typing import List
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, PDFSearchTool

folder_path = "./assets"
files = os.listdir(folder_path)
for file in files:
	file_path = os.path.join(folder_path, file)
pdf_search_tool = PDFSearchTool(
	pdf = file_path,
)

@CrewBase
class FinnaceCrew():
	"""Finance crew"""
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'

	@agent
	def admin_assistant_managr(self) -> Agent:
		return Agent(
			config=self.agents_config['admin_research_assistant'],
			tools=[SerperDevTool(), ScrapeWebsiteTool(), pdf_search_tool],
			verbose=True,
			memory=False,
		)

	@agent
	def chief_finance_officer(self) -> Agent:
		return Agent(
			config=self.agents_config['chief_finance_officer'],
			tools=[SerperDevTool(), ScrapeWebsiteTool()],
			verbose=True,
			memory=False,
		)

	@agent
	def chief_excutive_officer(self) -> Agent:
		return Agent(
			config=self.agents_config['chief_excutive_officer'],
			verbose=True,
			memory=False,
		)

	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['admin_research_assistant_task'],
			agent=self.admin_assistant_managr()
		)

	@task
	def project_understanding_task(self) -> Task:
		return Task(
			config=self.tasks_config['chief_finance_officer_task'],
			agent=self.chief_finance_officer()
		)

	@task
	def marketing_strategy_task(self) -> Task:
		return Task(
			config=self.tasks_config['chief_excutive_officer_task'],
			agent=self.chief_excutive_officer()
		)
	@crew
	def crew(self) -> Crew:
		"""Creates the Finance crew"""
		return Crew(
			agents=self.agents, # Automatically created by the @agent decorator
			tasks=self.tasks, # Automatically created by the @task decorator
			process=Process.sequential,
			verbose=2,
			# process=Process.hierarchical,
		)
