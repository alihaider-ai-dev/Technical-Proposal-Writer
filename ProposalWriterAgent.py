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
llm = ChatOpenAI(model="gpt-4o", temperature=0)


@tool
def getCompanyPortfolio() -> str:
    """Return our Company Information, Experience, Project and our Specialitites."""
    return read_text_from_pkl("Arweqah_company_information.pkl")


@tool
def getInfoAboutSaudiVision2030() -> str:
    """Return  Saudi Vision 2030 Information to help you find the alignment between the RFP and the Saudi Vision 2030 as well as Generated content"""
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
    "Our Understanding of the Scope of Work": {
        "prompt":
        "Only Return the Table of Content: Make sure to Add all the essential Question discussed below and provide the complete Response. Think in a Innovation and Leadership Program Manager. Add th Artifacts, Tables or Representation where Reqruired for better Clearification.",
        "questions": [
            "What are the client's main objectives and goals for the RFP project?",
            "What specific deliverables and outcomes are expected by the client in the Request for Proposal?",
            "What are the key challenges or pain points the client is facing that this Request for Proposal aims to address?",
            "What's our understanding in project field or industry based on company profile?",
            "Are there any specific requirements or constraints mentioned in the RFP?"
            "Create a Project Card that includes the General Objective, Target Group, Greographial Regeion, Duration, Objectives and Outputs and other projects if required based on the Request for Proposal."
        ]
    },
    "Methodology and Project Phases": {
        "prompt":
        "Only Return the Table of Content: Make sure to Add all the essential Question discussed below and provide the complete Response.\n Think in a Innovation and Leadership Program Manager Pick a Single Phases and Provide Complete Detailed Information about each and Every Step that needs to be done in each of the phase.\n Do not Depend on the Given STructure its only for the Idea Pick the Most Optimal strcture accoridng to the RFP GIven.\n Add th Artifacts, Tables or Representation where Reqruired for better Clearification.",
        "questions": [
            "What methodology will be used to execute the Proposed Project in Request for Proposal , how the project will flow and what will be the funnel or pipelines ?",
            "How will the project be divided into phases and what are the key activities in each phase, what is program defination, solution design, Risks, Expected Outputs, Expected Team Structure and Comittes, Phase Indicators and Insights, KPIS , Knowledge Trasnfer Plan, Communication Plan, Feedback Mehanism , and how does each phase contibute to the Project Objective etc? ",
            "What specific tools and techniques will be employed at each phase of the project?",
        ]
    },
    "Project Implementation Timeline": {
        "prompt":
        "Only Return the Table of Content: Make sure to Add all the essential Question discussed below and provide the complete Response.\n Think in a Innovation and Leadership Program Manager Pick a Single Phases from below and GIve Appropriate Topics \n Do not Depend on the Given STructure its only for the Idea Pick the Most Optimal strcture accoridng to the RFP GIven.\n Add th Artifacts, Tables or Representation where Reqruired for better Clearification.",
        "questions": [
            "What is the proposed timeline for the RFP project from initiation to completion?",
            "What are the key milestones and deliverables within this timeline for RFP project??",
            "How will the timeline ensure the project meets the client's deadlines?",
            "What are the potential risks to the timeline and how will they be mitigated?"
        ]
    },
    "RFP Project Management and Implementation Methodologies": {
        "prompt":
        "Only Return the Table of Content: Make sure to Add all the essential Question discussed below and provide the complete Response.\n Think in a Innovation and Leadership Program Manager\n Do not Depend on the Given STructure its only for the Idea Pick the Most Optimal strcture accoridng to the RFP GIven.\n Add th Artifacts, Tables or Representation where Reqruired for better Clearification.",
        "questions": [
            "What project management methodologies will be used to ensure the project that is in Request for Proposal stays on track?",
            "How will project progress be tracked and reported to the client?",
            "What are the processes for managing changes and issues during the Execution of the project proposed in RFP?",
            "How will quality control and assurance be maintained throughout the project proposed in RFP?"
        ]
    },
    "Project Team": {
        "prompt":
        "Only Return the Table of Content: Make sure to Add all the essential Question discussed below and provide the complete Response.\n Think in a Innovation and Leadership Program Manager Pick most appropriate persons accoridng to the RFP requirements and ROle Expertise\n Do not Depend on the Given STructure its only for the Idea Pick the Most Optimal strcture accoridng to the RFP GIven.\n Add th Artifacts, Tables or Representation where Reqruired for better Clearification.",
        "questions": [
            "Who are the key members of the project team and what are their roles as per provided RFP and Arweqah Team?",
            "What are the qualifications and relevant experiences of each team member which is essential for the REF Management and Execution?",
            "How will the team's expertise contribute to the success of the project?"
        ]
    },
    "Why Arweqah": {
        "prompt":
        "Only Return the Table of Content: Make sure to Add all the essential Question discussed below and provide the complete Response.\n Think in a Innovation and Leadership Program Manager Pick most releveant Experineces according to the RFP \n Do not Depend on the Given STructure its only for the Idea Pick the Most Optimal strcture accoridng to the RFP GIven.\n Add th Artifacts, Tables or Representation where Reqruired for better Clearification.",
        "questions": [
            "What are Arweqah's unique strengths and capabilities relevant to this project?",
            "How has Arweqah successfully handled similar projects in the past?",
            "What differentiates Arweqah from other consulting firms?",
            "Why should the client choose Arweqah for this project?"
        ]
    },
    "Our Global and Local Partnerships": {
        "prompt":
        "Only Return the Table of Content: Make sure to Add all the essential Question discussed below and provide the complete Response.\n Think in a Innovation and Leadership Program Manager Pick most releveant Experineces according to the RFP \n Do not Depend on the Given STructure its only for the Idea Pick the Most Optimal strcture accoridng to the RFP GIven.\n Add th Artifacts, Tables or Representation where Reqruired for better Clearification.",
        "questions": [
            "What global and local partnerships does Arweqah have that are relevant to this project?",
            "How do these partnerships enhance Arweqah's ability to deliver on the project?"
        ]
    },
    "Arweqah Memberships": {
        "prompt":
        "Only Return the Table of Content: Make sure to Add all the essential Question discussed below and provide the complete Response.\n Think in a Innovation and Leadership Program Manager Pick most releveant Experineces according to the RFP\n Do not Depend on the Given STructure its only for the Idea Pick the Most Optimal strcture accoridng to the RFP GIven.\n Add th Artifacts, Tables or Representation where Reqruired for better Clearification.",
        "questions": [
            "What professional memberships and affiliations does Arweqah hold?",
            "How do these memberships benefit the project and the client?"
        ]
    },
    "Our Relevant Experience and Previous Projects": {
        "prompt":
        "Only Return the Table of Content: Make sure to Add all the essential Question discussed below and provide the complete Response.\n Think in a Innovation and Leadership Program Manager Pick most releveant Experineces according to the RFP\n Do not Depend on the Given STructure its only for the Idea Pick the Most Optimal strcture accoridng to the RFP GIven.\n Add th Artifacts, Tables or Representation where Reqruired for better Clearification.",
        "questions": [
            "What are some examples of similar projects that Arweqah has successfully completed?",
            "What were the key challenges and outcomes of these projects?"
        ]
    }
}


def CreateAgentExecuter(prompt_content):
    prompt = hub.pull("hwchase17/openai-functions-agent")
    prompt.messages[0].prompt.template = prompt_content
    agent = create_tool_calling_agent(anthropicLLM, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    return agent_executor


def InvokeAgent():
    summary = generate_answer(
        read_text_from_pkl("rfpInfo.pkl"),
        """Your Task is to write the Detailed summary and Objective of the below Request for Proposal (Donot add any prefiex or post just retrun the summary) and Make sure to add the Project Maximum Timeline Mentioned in the RFP Neither less nor more from the RFP Below:
        
        """, "claude")

    print(summary)
    vision_extra_content = generate_answer(
        read_text_from_pkl("saudi_vision_2030_english.pkl"), f"""
        Your are Given the Objective of the Request for Proposal and the Summary of the Request for Proposal.

        {summary}

     Your Task is to Return the Supporting Information from the Below Text that is Saudi 2030 Vision you should enlist all the parts in detail from the Given text which are relevant to the Request for Proposal and could make a valueable impact on Proposal writing if the RFP get a Supporting information from the Below Text.
     if the RFP does not get any Supporting information from the Below Text then return the Empty text.
     Return Comprehensive information from the Provided Text.
     
Saudi Vision 2023 Text:
        
        """, "claude")
    print(f"\n\n\n{vision_extra_content}\n\n\n")
    initiator_prompt = f"""You are Expert Technical Proposal Table of Content or Structure Writer for Arweqah Company (working in social awarness and leadership programs based in Saudi Arabia).
    
    use the Tools getCompanyPortfolio, getRequestForProposalDocument, getInfoAboutSaudiVision2030 to get the Company Information, the Request For Proposal Inforamtion and Saudi Vision 2030 Information (when you need more info about the Saudio Vision 2030 and the RFP alignment) when required and also.
    
    OBJECTIVE AND SUMMARY OF THE REQUEST FOR PROPOSAL:
    {summary}
    """
    executor = CreateAgentExecuter(initiator_prompt)
    proposal = []
    for key, value in scope_of_work.items():
        questions = "\n\t".join([q for q in value['questions']])
        prompt = f"""
      <Instructions>
        - Do not provide the Explanation or conclusion only the Structure is Required.
        - Provide the Comprehensive Structure, Chapters/Headings Questions, Pipelines sub headings etc that justifies the Given QUestions and Return a Complete Table of Content.
        - Must use the Markdowns and make it detailed and specific.
        - Do not Include the Question just write the Content as you like with appropriate Headings but that content consiousl answer those questions.
        - Return Complete Table of content and do not add the closing heading as it is a Only a subsection.
        - Do not attach any prefix or postfix or explanation just return the Table of Content Directly. dont use the terms such as 'Based on the information provided, here is a' etc.
        - Use the Exact Maximum Project Timeline mentioned in the Request for Proposal Information and make the whole Content stick to it. Project timeline must be fixed and it must be Given Maximum Timeline not less not more in the RFP text donot add it from your own.
       </Instructions>

            
        <content_specific_instruction>
            {value['prompt']}
        </content_specific_instruction>


        Section Title: {key}
        
        what need to be answered in the output Text.
        \t{questions}
      """
        for i in range(3):
            try:
                proposal.append(
                    executor.invoke({"input": prompt})['output'][0]['text'])
                break
            except Exception as e:
                print(e)
                import time
                time.sleep(20)

    result = []
    for item in proposal:
        result_eng = None
        result_arb = None
        for i in range(3):
            try:
                result_eng = generate_answer(
                    "", f"""
                    Request for Proposal Information:\n
                    \t\t{read_text_from_pkl("rfpInfo.pkl")} 

                    \n\nSupporting Text from the Saudi Vision 2030 Information:\n
                    {vision_extra_content}
                    
                    \n\n Company Information: 
                    \t\t{read_text_from_pkl("Arweqah_company_information.pkl")}\n\n\n 
                    
                    TABLE OF CONTENT: 
                    \t\t{item}\n\n

                    <Instructions>
                    - Your Task is to write the Detailed Content using the Table of Content provided by the Information from the RFP and company and Explain each and Every Heading in Detail and Tune the Structure of Content with the Best of Quality Think , analyze and then write accordingly. 
                    - Be specific and Return complete Response without. 
                    - Use the Exact Maximum Project Timeline mentioned in the Request for Proposal Information and make the whole Content stick to it. Project timeline must be fixed and it must be Given Maximum Timeline not less not more in the RFP text donot add it from your own.
                    - Directly Write the Content without any opening or closing statements such as "here is content" and likewise phrases.
                    - Write Complete Content so the Text is complete according to the Table of Content wihtout cutting of it at some random Point.
                    - Use the Proper Markdowns.
                    - Use the Tables, Artifacts, Visuals or Blocks where required for better quality and Explanation.
                    - Prioritize the Tables and Diagramatic Representation then Text.
                    - Utilize the Saudi Vision 2030 Information to make the Content more Qualitative and Quantitative and relevant to the RFP.
                    </Instructions>

                    <Most important>
                    - Use the Exact Maximum Project Timeline mentioned in the Request for Proposal Information neither less nor more from the RFP text donot add it from your own.
                    </ Mostimportant>
                    """, "claude")
                break
            except Exception as e:
                print(e)
                import time
                time.sleep(20)

        for j in range(3):
            try:
                result_arb = generate_answer(
                    "", f"""
                    <TASK>
                    Your Task is to Translate the Given English to Arabic Langauge.
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
                    </RESPONSE_INSTRUCTIONS>

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
