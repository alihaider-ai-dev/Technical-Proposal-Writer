import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
import os
from langchain import hub
from DataIngestion import read_text_from_pkl
import time
from utils import generate_answer
from langchain import hub
import streamlit as st
load_dotenv()
os.environ['LANGCHAIN_API_KEY'] = os.getenv("LANGCHAIN_API_KEY")
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
os.environ["ANTHROPIC_API_KEY"] = os.getenv("ANTHROPIC_API_KEY")

import anthropic

client = anthropic.Anthropic()
 

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


def InvokeAgent(focus,scope_of_work):
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
                    context = f"<Project_methodology_and_phases>{list(scope_of_work['# Methodology and Project Phases']['questions'][0].values())[0]}</Project_methodology_and_phases>"
                elif question == list(
                        scope_of_work['# Methodology and Project Phases']
                    ['questions'][2].keys())[0]:
                    context = f"<Project_phases_and_tasks>{list(scope_of_work['# Methodology and Project Phases']['questions'][1].values())[0]}</Project_phases_and_tasks>"
                elif question == list(
                        scope_of_work['# Project Implementation Timeline']
                    ['questions'][0].keys())[0]:
                    context = f"<Project_methodlogy_phases_and_tasks>{list(scope_of_work['# Methodology and Project Phases']['questions'][0].values())[0]}\n{list(scope_of_work['# Methodology and Project Phases']['questions'][1].values())[0]}\n{list(scope_of_work['# Methodology and Project Phases']['questions'][2].values())[0]}</Project_methodlogy_phases_and_tasks>"
                elif question == list(
                        scope_of_work['# Project Team']
                    ['questions'][0].keys())[0]:
                    context =f"<Operational_model>{ list(scope_of_work['# Operational Model']['questions'][1].values())[0]}</Operational_model>"
                elif question == list(scope_of_work['# Our Relevant Experience and Previous Projects']['questions'][0].keys())[0]:
                    context = f"\n<Our Competetive Advantage> {list(scope_of_work['# Our understanding in project field or industry']['questions'][1].values())[0]}</Our Competetive Advantage>"

                
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
