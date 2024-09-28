import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from langchain import hub
from DataIngestion import read_text_from_pkl
import time
from utils import generate_answer
from langchain import hub

load_dotenv()
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

import anthropic

client = anthropic.Anthropic()

scope_of_work = {
    "# Our Understanding of the Scope of Work": {
        "questions": [
            {
                """
            What are the client's main objectives and goals for the RFP project?
            """:
                ""
            },
            {
                """
            How do the project’s objectives align with the client’s strategic goals?
            Required Answer: (We need to mention the client’s strategic goals that related to the project objectives, show them as table. First column is client’s strategic goals, 2nd column is project objectives that related to client’s strategic goals, 3rd column explains how projects objectives align/contribute to client’s strategic goals)
            """:
                ""
            },
            {
                """
            How do the project’s objectives align with Saudi Vision 2030?
            Required Answer: ((We need to mention the Saudi Vision 2030 goals that related to the project objectives, show them as table. First column is Saudi vision goals, 2nd column is project objectives that related to 2030 goals, 3rd column explains how projects objectives align/contribute to 2030 goals))

            How do the project’s objectives align with the programs of Saudi Vision 2030?
            Required Answer: (We need to mention the programs of Saudi Vision 2030 that related to the project objectives, show them as table. First column is programs of Saudi Vision 2030, 2nd column is project objectives that related to programs of Saudi Vision 2030, 3rd column explains how projects objectives align/contribute to programs of Saudi Vision 2030)
            """:
                ""
            },
            {
                """
            How do the project’s objectives align with the United Nations Sustainable Development Goals (SDGs)?
            Required Answer: (We need to mention the United Nations Sustainable Development Goals that related to the project objectives, show them as table. First column is United Nations Sustainable Development Goals,2nd column is project objectives that related to United Nations Sustainable Development Goals, 3rd column explains how projects objectives align/contribute to United Nations Sustainable Development Goals)
            """:
                ""
            },
        ]
    },
    "# Our understanding in project field or industry": {
        "questions": [
            {
                """
            What's our understanding in RFP project field or industry?
            """:
                ""
            },
            {
                "What competitive advantages do we bring to this project based on our industry knowledge?":
                ""
            },
            {
                """
            What is the current state of the industry or field relevant to the project?
            Required Answer: (Give some state about the following in a Table: market size – targeted segments – any other relevant state - ...)
            """:
                ""
            },
            {
                """
            What global and local information and statistics are available concerning the scope of the project (target group, efforts made, etc.)? 
            Required Answer: (Must provide the updated and reliable reference urls/sources/citations and web links)
            """:
                ""
            },
            {
                """
            What are the global and regional best practices (global and regional experiences) similar or relevant to the project? 
            Required Answer:
            (In the answer, mention the practice name, organization name, country, brief about the practice, goals, programs and services, achievements, and impact in numbers.) it could be shown as two tables (1 table for global , 1 table for regional).
            """:
                ""
            },
            {
                """
            What are the local best practices (local experiences) similar or relevant to the project? 
            Required Answer:
            ( Max 03: In the answer, mention the practice name, country, brief about the practice, goals, programs and services, achievements, and impact in numbers.)(Must provide the updated and reliable reference urls/sources/citations and web links)
            """:
                ""
            },
        ]
    },
    "# Operational Model": {
        "questions": [
            {
                """Write the following in a table about the project (project brief, project objectives, target group, geographic scope, project duration).""":
                ""
            },
            {
                """What is the appropriate operational business model for the project (in this you can mention the units or departments that needed to execute the project, and how will be the collaboration and the integration between them. Also describe how each unit will work and why it's important). You may show the operational model in a diagram. Provide coniseze and complete output. (Make it consize)""":
                ""
            },
        ]
    },
    "# Methodology and Project Phases": {
        "questions": [
            {
                """
              What methodology will be used to execute the project? What are the suitable phases to execute the project? (You provide the answer in tables (for each phase) including the following: phase name, brief about the phase, associated activities, deliverables, and timeframe.)
              What technical tools are necessary for execution in each phase? (for example: if there is some phase related to innovation lab, we can use some tools / techniques or frameworks about innovation) (Provide Detailed answer)
            """:
                ""
            },
            {
                """
              Divide each phase into several tasks that align with the deliverables. (Must ensure all Phases are enlisted)
              Place each task in a table as follows: phase name, task name, associated deliverable, brief about the task, how we will execute it step by step, and the proposed consulting tools that may help to execute this phase.
            """:
                ""
            },
            {
                """from the tasks table, provide supporting and detailed information about each task and how to execute it (tools, techniques, frameworks, models, methodologies, matrices, tables, etc.). (for example: if there is a phase for getting feedback from the participants, we will use some of feedback tool like ethe survey) Provide a Tabular Response for each Table.""":
                ""
            },
        ]
    },
    "# Project Implementation Timeline": {
        "questions": [
            {
                """
              "What are the key dates and milestones within the timeline?"
              "How will time be allocated across the different phases of the project?"
              "What dependencies or sequencing are critical to maintaining the timeline?"
              "Please generate a Gantt chart showing each phase of the project?"
              "What criteria will be used to declare a milestone as successfully completed?"
            """:
                ""
            },
        ]
    },
    "# Project Team": {
        "questions": [
            {
                """
            Who are the key members of the project team and what are their roles?
            Required Answer:
              Suggest a project team structure , and show How will the team structure support effective project execution?
              "How will the team's expertise contribute to the success of the project?"
              "How will the team’s collective experience help navigate project challenges?"
              "How will team collaboration be leveraged to maximize project outcomes?"
              "How does the team’s expertise align with the client’s expectations?"
              Provide concrete info based on company info and project info rather then abstract or general info.
              (use the team members from the Arewqeah company information and provide the concrete names and project Team)
              """:
                ""
            },
        ]
    },
    "# Why Arweqah": {
        "questions": [
            {
                """What are Arweqah's unique strengths and capabilities relevant to this project )RFP)?""":
                ""
            },
        ]
    },
    "# Our Global and Local Partnerships": {
        "questions": [
            {
                """
              "What global and local partnerships does Arweqah have that are relevant to this project? (just mention the name of partners)"
              "Mention Arweqah other partners, who are not related to the project."
            """:
                ""
            },
        ]
    },
    "# Arweqah Memberships": {
        "questions": [
            {
                """What professional memberships and affiliations does Arweqah hold? (just mention these memberships)""":
                ""
            },
        ]
    },
    "# Our Relevant Experience and Previous Projects": {
        "questions": [
            {
                """What are some examples of similar projects that Arweqah has successfully completed? (just mention these project and give a brief of each one as follow : description, main deliverables, clients, geographical region)""":
                ""
            },
        ]
    }
}


def getResponse(question, context, f_ins):
    rfp = read_text_from_pkl("rfpInfo.pkl")
    compnay_info = read_text_from_pkl("Arweqah_company_information.pkl")

    systems_info = [{
        "type":
        "text",
        "text":
        f"""
          You are Expert Technical Proposal Writer for Arweqah Company (working in social awarness and leadership programs based in Saudi Arabia).
          Do not Include any extra information only foucs on the one subsection that is provided.
          - Must Respond it Completely donot cut off the response.
          - Return the Detailed Answers to the Given Questions (with Headings) Think in a Innovation and Leadership Program Manager.
          - Add th Artifacts, Tables or Representation where Reqruired for better Clearification.
          - if you claim anything then cite the sources using a weblink.
          - use markdowns format for response.
          must use the Heading markdowns , Tables and Bullets.

          <most_important>
              1. Must complete the response.
              2. dont cut off the response.
              3. complete each and every question/block.
              4. Provide Extensive Information about each question being asked.
          </most_important>

          {f_ins}

        for Every Question MUst stick the Given Information for the RFP and Compnay Profile.
        use the Company Information, Request for Proposal to get the Company Information, the Request For Proposal Inforamtion and use your knowledge Saudi Vision 2030 Information.

          """,
    }, {
        "type":
        "text",
        "text":
        f"\n<Request_for_proposal_Information>\n{rfp}\n\n</Request_for_proposal_Information>\n",
    }, {
        "type":
        "text",
        "text":
        f"\n<Arweqah_compnay_Information>\n{compnay_info}\n\n</Arweqah_compnay_Information>\n",
    }]

    if context:
        systems_info.append({{
            "type": "text",
            "text": f"\n{context}\n",
        }})

    response = client.messages.create(
        model="claude-3-5-sonnet-20240620",
        max_tokens=8192,
        extra_headers={"anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"},
        system=systems_info,
        messages=[{
            "role":
            "user",
            "content":
            f"{question} \n (Must use the Heading markdowns, Tables and Bullets in response)"
        }],
    )
    print(response)
    return response.content[0].text


def InvokeAgent(focus):
    f_ins = ''
    if len(focus):
        focus = f"""<focused_instructions>
            {f_ins}
        </focused_instructions>"""

    for main_heading, questions in scope_of_work.items():
        for i, item in enumerate(questions['questions']):
            for question, answer in item.items():
                context = None
                if question == list(
                        scope_of_work['# Methodology and Project Phases']
                    ['questions'][1].keys())[0]:
                    context == list(
                        scope_of_work['# Methodology and Project Phases']
                        ['questions'][0].values())[0]
                elif question == list(
                        scope_of_work['# Methodology and Project Phases']
                    ['questions'][2].keys())[0]:
                    context == list(
                        scope_of_work['# Methodology and Project Phases']
                        ['questions'][1].values())[0]
                elif question == list(
                        scope_of_work['# Project Implementation Timeline']
                    ['questions'][0].keys())[0]:
                    context == f"{list(scope_of_work['# Methodology and Project Phases']['questions'][0].values())[0]}\n{list(scope_of_work['# Methodology and Project Phases']['questions'][1].values())[0]}\n{list(scope_of_work['# Methodology and Project Phases']['questions'][2].values())[0]}"

                for i in range(3):
                    try:
                        scope_of_work[main_heading]["questions"][i][
                            question] = getResponse(question, context, focus)
                        break
                    except Exception as e:
                        print(e)
                        import time
                        time.sleep(30)

                break
    English_proposal = """"""
    arabic_proposal = """"""

    for main_heading, questions in scope_of_work.items():
        English_proposal += main_heading + "\n"
        arabic_proposal += translate(main_heading)

        for i, item in enumerate(questions['questions']):
            for question, answer in item.items():
                English_proposal += f"{answer}\n\n"
                arabic_proposal += translate(answer)

    result = {
        "English_proposal": English_proposal,
        "arabic_proposal": arabic_proposal
    }

    return result


def translate(result_eng):
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
    return result_arb
