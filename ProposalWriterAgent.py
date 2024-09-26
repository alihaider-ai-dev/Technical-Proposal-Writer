import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from langchain_anthropic import ChatAnthropic
from langchain.tools import BaseTool, StructuredTool, tool
from langchain import hub
from DataIngestion import read_text_from_pkl
from langchain.agents import create_tool_calling_agent
from langchain.agents import AgentExecutor
import time

from utils import generate_answer
from langchain import hub

load_dotenv()
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")
anthropicLLM = ChatAnthropic(model="claude-3-5-sonnet-20240620")
llm = ChatOpenAI(model="gpt-4o-2024-08-06", temperature=0)


@tool
def getCompanyPortfolio() -> str:
    """Return our Company Information, Experience, Project and our Specialitites."""
    return read_text_from_pkl("Arweqah_company_information.pkl")


@tool
def getInfoAboutSaudiVision2030() -> str:
    """Return Saudi Vision 2030 Information to help you find the alignment between the RFP and the Saudi Vision 2030 as well as Generated content"""
    return read_text_from_pkl("saudi_vision_2030_english.pkl")


@tool
def getRequestForProposalDocument() -> str:
    """Return the Request for Proposal Document that our company has to Submit the Proposal for."""
    return read_text_from_pkl("rfpInfo.pkl")


tools = [
    getCompanyPortfolio, getRequestForProposalDocument,
    getInfoAboutSaudiVision2030
]
scope_of_work = {
    "Our Understanding of the Scope of Work 1": {
        "part":
        "1",
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
            </most_important>
        """,
        "questions": [
            """ What are the client's main objectives and goals for the RFP project? """,
            """How do the project’s objectives align with the client’s strategic goals?
            Required Answer:
            (We need to mention the client’s strategic goals that related to the project objectives, show them as table. First column is client’s strategic goals, 2nd column is project objectives that related to client’s strategic goals, 3rd column explains how projects objectives align/contribute to client’s strategic goals)
            
            """,
        ]
    },
    "Our Understanding of the Scope of Work 2": {
        "part":
        "1",
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
            </most_important>
        """,
        "questions": [
            """How do the project’s objectives align with Saudi Vision 2030?
            Required Answer: ((We need to mention the Saudi Vision 2030 goals that related to the project objectives, show them as table. First column is Saudi vision goals, 2nd column is project objectives that related to 2030 goals, 3rd column explains how projects objectives align/contribute to 2030 goals))

            """,
            """How do the project’s objectives align with the programs of Saudi Vision 2030?
            Required Answer:
            (We need to mention the programs of Saudi Vision 2030 that related to the project objectives, show them as table. First column is programs of Saudi Vision 2030, 2nd column is project objectives that related to programs of Saudi Vision 2030, 3rd column explains how projects objectives align/contribute to programs of Saudi Vision 2030)

            """
        ]
    },
    "Our Understanding of the Scope of Work 3": {
        "part":
        "1",
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
            </most_important>
        """,
        "questions": [
            """How do the project’s objectives align with the United Nations Sustainable Development Goals (SDGs)?
            Required Answer:
            (We need to mention the United Nations Sustainable Development Goals that related to the project objectives, show them as table. First column is United Nations Sustainable Development Goals,2nd column is project objectives that related to United Nations Sustainable Development Goals, 3rd column explains how projects objectives align/contribute to United Nations Sustainable Development Goals)
            """,
        ]
    },
    "Our understanding in project field or industry 1": {
        "part":
        "2",
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
            </most_important>
        """,
        "questions": [
            """What's our understanding in RFP project field or industry?
           """,
            "What competitive advantages do we bring to this project based on our industry knowledge?",
            """What is the current state of the industry or field relevant to the project?
            Required Answer:
            (Give some state about the following: market size – targeted segments – any other relevant state - ...)

            """
        ]
    },
    "Our understanding in project field or industry 2": {
        "part":
        "2",
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
            </most_important>
        """,
        "questions": [
            """What global and local information and statistics are available concerning the scope of the project (target group, efforts made, etc.)? 
            Required Answer:
            (Must provide the updated and reliable reference urls/sources/citations and web links)"""
        ]
    },
    "Our understanding in project field or industry 3": {
        "part":
        "2",
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
            </most_important>
        """,
        "questions": [
            """What are the global and regional best practices (global and regional experiences) similar or relevant to the project? 
            Required Answer:
            (In the answer, mention the practice name, organization name, country, brief about the practice, goals, programs and services, achievements, and impact in numbers.) it could be shown as two tables (1 table for global , 1 table for regional).
            """,
            """What are the local best practices (local experiences) similar or relevant to the project? 
            Required Answer:
            ( Max 03: In the answer, mention the practice name, country, brief about the practice, goals, programs and services, achievements, and impact in numbers.)(Must provide the updated and reliable reference urls/sources/citations and web links)"""
        ]
    },
    "Operational Model": {
        "part":
        "3",
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
            </most_important>
        """,
        "questions": [
            """Write the following in a table about the project (project brief, project objectives, target group, geographic scope, project duration).""",
            """What is the appropriate operational business model for the project (in this you can mention the units or departments that needed to execute the project, and how will be the collaboration and the integration between them. Also describe how each unit will work and why it's important). You may show the operational model in a diagram. Provide coniseze and complete output.""",
        ]
    },
    "Methodology and Project Phases 1": {
        "part":
        "4",
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
            </most_important>
        """,
        "questions": [
            """What methodology will be used to execute the project? What are the suitable phases to execute the project? (You provide the answer in tables (for each phase) including the following: phase name, brief about the phase, associated activities / deliverables, and timeframe.)""",
            """How will the project be divided into phases and what are the key activities in each phase?""",
        ]
    },
    "Methodology and Project Phases 2": {
        "part":
        "4",
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.

            project phases Information:

            {phases}
            
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
                4. Only answer the given QUestions as specified without any other text.
            </most_important>
        """,
        "questions": [
            """What are the deliverables or outputs of each phase?""",
            """What technical tools are necessary for execution in each phase? (for example: if there is some phase related to innovation lab, we can use some tools / techniques or frameworks about innovation)
            """
        ]
    },
    "Tasks Division in Project Phases 1": {
        "part":
        "5",
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.

            project phases Information:

            {phases}

            Deliverables Information:
            {deliverables}
            
            Only Return the Answer to the Given Questions.
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
            </most_important>

        """,
        "questions": [
            """Divide each phase into several tasks that align with the deliverables.
            """,
            """Place each task in a table as follows: phase name, task name, associated deliverable, brief about the task, how we will execute it step by step, and the proposed consulting tools that may help to execute this phase.
            """
        ]
    },
    "Tasks Division in Project Phases 2": {
        "part":
        "5",
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.

            Tasks Division in Project Phases :

            {tasks}

            Only Return the Answer to the Given Questions.
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
            </most_important>

        """,
        "questions": [
            """from the task table, provide supporting and detailed information about each task and how to execute it (tools, techniques, frameworks, models, methodologies, matrices, tables, etc.). (for example: if there is a phase for getting feedback from the participants, we will use some of feedback tool like ethe survey) Provide a Single Complete Table.""",
        ]
    },
    "Project Implementation Timeline": {
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.

            project phases Information:
            {phases}

            Deliverables Information:
            {deliverables}
            
            Only Return the Answer to the Given Questions.
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
            </most_important>

        """,
        "questions": [
            "What are the key dates and milestones within the timeline?",
            "How will time be allocated across the different phases of the project?",
            "What dependencies or sequencing are critical to maintaining the timeline?",
            "Please generate a Gantt chart showing each phase of the project?",
            "What criteria will be used to declare a milestone as successfully completed?"
        ]
    },
    "Project Team": {
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.

            "Operational Model" Information:
            {operational_model}
            
            "Methodology and Project Phases" Information:
            {phases}
            
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
            </most_important>
        """,
        "questions": [
            """Who are the key members of the project team and what are their roles?
            Required Answer:
            
            Suggest a project team structure , and show How will the team structure support effective project execution?""",
            "How will the team's expertise contribute to the success of the project?",
            "How will the team’s collective experience help navigate project challenges?",
            "How will team collaboration be leveraged to maximize project outcomes?",
            "How does the team’s expertise align with the client’s expectations?"
        ]
    },
    "Why Arweqah": {
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
            </most_important>
        """,
        "questions": [
            """What are Arweqah's unique strengths and capabilities relevant to this project?"""
        ]
    },
    "Our Global and Local Partnerships": {
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
            </most_important>
        """,
        "questions": [
            """What global and local partnerships does Arweqah have that are relevant to this project? (just mention the name of partners)
            """,
            """Mention Arweqah other partners, who are not related to the project.
            """
        ]
    },
    "Arweqah Memberships": {
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
            </most_important>
        """,
        "questions": [
            """What professional memberships and affiliations does Arweqah hold? (just mention these memberships)
"""
        ]
    },
    "Our Relevant Experience and Previous Projects": {
        "prompt":
        """ 
            - Must Respond it Completely donot cut off the response.
            - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
            - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
            - if you claim anything then cite the sources using a weblink.
            <most_important>
                1. Must complete the response.
                2. dont cut off the response.
                3. complete each and every question/block.
            </most_important>
        """,
        "questions": [
            """What are some examples of similar projects that Arweqah has successfully completed? (just mention these project and give a brief of each one as follow : description, main deliverables, clients, geographical region)
            """
        ]
    }
}


def CreateAgentExecuter(prompt_content):
    prompt = hub.pull("hwchase17/openai-functions-agent")
    prompt.messages[0].prompt.template = prompt_content
    agent = create_tool_calling_agent(anthropicLLM, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor


def InvokeAgent(focus):
    f_ins = ''
    if len(focus):
        focus = f"""<focused_instructions>
            {f_ins}
        </focused_instructions>"""
    summary = generate_answer(
        read_text_from_pkl("rfpInfo.pkl"),
        f"""Your Task is to write the Detailed summary and Objective of the below Request for Proposal (Donot add any prefiex or post just retrun the summary) and Make sure to add the Project Maximum Timeline Mentioned in the RFP Neither less nor more from the RFP Below:

        {focus}

            """, "claude")

    initiator_prompt = f"""You are Expert Technical Proposal Writer for Arweqah Company (working in social awarness and leadership programs based in Saudi Arabia).
    Do not Include nay extra information only foucs on the one subsection that is provided.
    <most_important>
        1. Must complete the response.
        2. dont cut off the response.
        3. complete each and every question/block.
    </most_important>

   {focus}

    use the Tools getCompanyPortfolio, getRequestForProposalDocument, getInfoAboutSaudiVision2030 to get the Company Information, the Request For Proposal Inforamtion and Saudi Vision 2030 Information (when you need more info about the Saudio Vision 2030 and the RFP alignment) when required and also.

    OBJECTIVE AND SUMMARY OF THE REQUEST FOR PROPOSAL:
    {summary}
    """
    executor = CreateAgentExecuter(initiator_prompt)
    proposal = {}
    for key, value in scope_of_work.items():
        if key == "Methodology and Project Phases 2":
            s_prompt = value['prompt'].format(
                phases=proposal['Methodology and Project Phases 1'])
        elif key == "Tasks Division in Project Phases 1":
            s_prompt = value['prompt'].format(
                phases=proposal['Methodology and Project Phases 1'],
                deliverables=proposal['Methodology and Project Phases 2'])
        elif key == "Project Implementation Timeline 1":
            s_prompt = value['prompt'].format(
                phases=proposal['Methodology and Project Phases 1'],
                deliverables=proposal['Methodology and Project Phases 2'])
        elif key == "Project Team":
            s_prompt = value['prompt'].format(
                phases=proposal['Methodology and Project Phases 1'],
                operational_model=proposal['Operational Model'])
        elif key == "Tasks Division in Project Phases 2":
            s_prompt = value['prompt'].format(
                tasks=proposal['Tasks Division in Project Phases 1'])

        else:
            s_prompt = value['prompt']

        questions = ""
        for i, q in enumerate(value['questions']):
            questions += "\n\t\t" + f"{i+1}. {q}"
        prompt = f"""
      <Instructions>
        - Add Tables, charts, or artifacts for better clearification.
        - focus on the content specific instrcutions.
        - Do not provide the Explanation or conclusion only the Structure is Required.
        - Must use the Markdowns and make it detailed and specific.
        - Do not Include the Question just write the Content as you like with appropriate Headings but that content consiousl answer those questions.
        - D ont use the terms such as 'Based on the information provided, here is a' etc.
        - Use the Proper Markdowns.
        - Use the Tables, Artifacts, Visuals or Blocks where required for better quality and Explanation.
        - Prioritize the Tables and Diagramatic Representation then Text.
        - Utilize the Saudi Vision 2030 Information to make the Content more Qualitative and Quantitative and relevant to the RFP.
        - Use the Exact Maximum Project Timeline mentioned in the Request for Proposal Information and make the whole Content stick to it. Project timeline must be fixed and it must be Given Maximum Timeline not less not more in the RFP text donot add it from your own.
       </Instructions>

        <most_important>
            1. Must complete the response.
            2. dont cut off the response.
            3. complete each and every question/block.
        </most_important>
        
        <content_specific_instruction>
            {s_prompt}
        </content_specific_instruction>
        {focus}
        


        Section Title: {key}
        What need to be answered in the output Text.
        {questions}

        
      """
        for i in range(3):
            try:
                print(prompt)
                proposal[key] = executor.invoke({"input":
                                                 prompt})['output'][0]['text']
                break
            except Exception as e:
                print(e)
                import time
                time.sleep(30)
    result = []
    for key, item in proposal.items():
        result_eng = item
        result_arb = None

        for j in range(3):
            try:
                result_arb = generate_answer(
                    "", f"""
                    <TASK>
                    Your Task is to Translate the Given English to Arabic Langauge and must return the complete Arabic Text from the English Text provided.
                    </TASK>

                    <FORMATTING_INSTRUCTIONS>
                        1. Use the Markdown Exactly same as used in English version to make the Headings exactly same.
                        2. Use the Tables, Artifacts, Visuals or Blocks where required for better quality and Explanation as provided in the English Version.
                        4. Do not miss a single chunk of text to be translated.
                    </FORMATTING_INSTRUCTIONS>

                    <RESPONSE_INSTRUCTIONS>
                    1. Return the Arabic Version without any prefix or postfix or opening and closing Statement in english.
                    2. Replicate the Exact ENglish Content with Exact same strcture and Tables etc in Arabic.
                    3. write the Arabic from the Right to Left.
                    4. Numbering should be in Arabic and from right to left.
                    5. bullet point should be included in the right side as the Text is in arabic which is from right to left.
                    6. Must resemble to the English Content Exactly but in Arabic.
                    7. Do not miss or skip any part.
                    8. The bullet point must be on the right side that is the the bullet . is right oriented.
                    9. Donot Skip anything return the complete Text in arabic from the English.
                    10. respond the complete Arabic text from the English each and every section should be completed till the last section.
                    </RESPONSE_INSTRUCTIONS>
<most_important>
    1. Must complete the response.
    2. dont cut off the response.
    3. complete each and every question/block.
</most_important>
                    <Table_formatting_instructions>
                        if the Table is in the English Version then convert that Table to Arabic but make sure to as In English columns are from left to right and In Arabic you have to make the  columns from right to left.
                    </Table_formatting_instructions>

                <ENGLISH VERSION>
                    {result_eng}
                </ENGLISH VERSION>

                    """, "claude_for_translation")
                break
            except Exception as e:
                print(e)
                import time
                time.sleep(20)
        result.append({
            "english_subsection": result_eng,
            "arabic_subsection": result_arb
        })

    return result
