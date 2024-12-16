#!/usr/bin/env python
import os
from langtrace_python_sdk import langtrace
from pydantic import BaseModel

from crewai.flow.flow import Flow, listen, start
from .crews.edu_research.edu_research_crew import Edu_Research_Crew
from .crews.edu_content_writer.edu_content_writer import EduContentWriter

from dotenv import load_dotenv

load_dotenv()
langtrace.init(api_key = os.getenv("LANGTRACE_API_KEY"),
                api_host = os.getenv("LANGTRACE_API_HOST"))
input_variables = {
            "audience_level": "beginners",
            "topic": "Fine-tuning LLMs"
        }

class EduFlow(Flow):
    @start()
    def generate_research_topic(self):
       
        return Edu_Research_Crew().crew().kickoff(inputs=input_variables).pydantic

    @listen(generate_research_topic)
    def generate_educational_content(self, plan):
        final_content = []
        for section in plan.sections:
            print("Generating content for section:", section.title)
            writer_inputs = input_variables.copy()
            writer_inputs["section"] = section.model_dump_json()
            final_content.append(EduContentWriter().crew().kickoff(writer_inputs).raw)
            return final_content
    @listen(generate_educational_content)
    def save_final(self, content):
        print("printing final thoughts")
        output_dir = "output"
        os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
        
        # Use topic and audience_level from input_variables to create the file name
        topic = input_variables.get("topic")
        audience_level = input_variables.get("audience_level")
        file_name = f"{topic}_{audience_level}_final.md".replace(" ", "_")  # Replace spaces with underscores
        
        output_path = os.path.join(output_dir, file_name)
        print(f"Here's the output path: {output_path}")
        print(f"Length of content array: {len(content)}")
        with open(output_path, "w") as f:
            for section_content in content:
                f.write(section_content)
                f.write("\n\n")  # Add space between sections
    #@listen(generate_educational_content)
    #def save_to_text(self, content):
    #    output_dir = "output"
    #    os.makedirs(output_dir, exist_ok=True)  # Ensure the directory exists
    #    
    #    # Use topic and audience_level from input_variables to create the file name
    #    topic = input_variables.get("topic")
    #    audience_level = input_variables.get("audience_level")
    #    file_name = f"{topic}_{audience_level}_outline.md".replace(" ", "_")  # Replace spaces with underscores
    #    
    #    output_path = os.path.join(output_dir, file_name)
    #    
    #    with open(file_name, 'w') as f:
    #        f.write("# Educational Plan\n\n")
    #        for i, section in enumerate(content.sections, start=1):
    #            f.write(f"## Section {i}: {section.title}\n\n")
    #            f.write(f"**High-Level Goal:** {section.high_level_goal}\n\n")
    #            f.write(f"**Why It's Important:** {section.why_important}\n\n")
    #            f.write("### Sources\n")
    #            if section.sources:
    #                for source in section.sources:
    #                    f.write(f"- {source}\n")
    #            else:
    #                f.write("- None\n")
    #            f.write("\n### Content Outline\n")
    #            if section.content_outline:
    #                for item in section.content_outline:
    #                    f.write(f"- {item}\n")
    #            else:
    #                f.write("- None\n")
    #            f.write("\n")
    #            
    #        
    #    file_name = f"{topic}_{audience_level}_final.md".replace(" ", "_") 
    #    output_path = os.path.join(output_dir, file_name)
    #    with open(output_path)
    #        for section in content:
    #            f.write(section)
    #            f.write("\n\n")  # Add space between sections
def kickoff():
    edu_flow = EduFlow()
    edu_flow.kickoff()


def plot():
    edu_flow = EduFlow()
    edu_flow.plot()


if __name__ == "__main__":
    kickoff()
