import streamlit as st
from DataIngestion import SaveTextFromPDF, read_text_from_pkl
from ProposalWriterAgent import InvokeAgent
import os
from saving_utils import convert, html_to_word
from document_utils import process_document

st.set_page_config(page_icon="💬",
                   layout="wide",
                   page_title="Arweqah Proposal AI")


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


if "scope_of_work" not in st.session_state:
    st.session_state.scope_of_work = {
        "Our Understanding of the Scope of Work": {
            "questions": [
                {
                    "1. What are the client's main objectives and goals for the RFP project? (provide the Detailed Answer)":
                    ""
                },
                {
                    "2. How do the project's objectives align with the client's strategic goals?":
                    "We need to mention the client's strategic goals that related to the project objectives, show them as table. First column is client's strategic goals, 2nd column is project objectives that related to client's strategic goals, 3rd column explains how projects objectives align/contribute to client's strategic goals"
                },
                {
                    "3. How do the project's objectives align with Saudi Vision 2030?\n4. How do the project's objectives align with the programs of Saudi Vision 2030?":
                    "- We need to mention the Saudi Vision 2030 goals that related to the project objectives, show them as table. First column is Saudi vision goals, 2nd column is project objectives that related to 2030 goals, 3rd column explains how projects objectives align/contribute to 2030 goals\n- We need to mention the programs of Saudi Vision 2030 that related to the project objectives, show them as table. First column is programs of Saudi Vision 2030, 2nd column is project objectives that related to programs of Saudi Vision 2030, 3rd column explains how projects objectives align/contribute to programs of Saudi Vision 2030"
                },
                {
                    "5. How do the project's objectives align with the United Nations Sustainable Development Goals (SDGs)?":
                    "- We need to mention the United Nations Sustainable Development Goals that related to the project objectives, show them as table. First column is United Nations Sustainable Development Goals,2nd column is project objectives that related to United Nations Sustainable Development Goals, 3rd column explains how projects objectives align/contribute to United Nations Sustainable Development Goals"
                },
            ]
        },
        "Our understanding in project field or industry": {
            "questions": [
                {
                    "1. What's our understanding in RFP project field or industry?":
                    ""
                },
                {
                    "2. What competitive advantages do we bring to this project based on our industry knowledge?":
                    ""
                },
                {
                    "3. What is the current state of the industry or field relevant to the project?":
                    "- Give some state about the following in a Table: market size – targeted segments (which also explains the percentage of the population/seekers being considered/Instrested or tragetted ) - any other relevant state - ..."
                },
                {
                    "4. What global and local information and statistics are available concerning the scope of the project (target group, efforts made, etc.)?":
                    "- Must provide the updated and reliable reference urls/sources/citations and web links"
                },
                {
                    "5. What are the global and regional best practices (global and regional experiences) similar or relevant to the project?":
                    "In the answer, mention the practice name, organization name, country, brief about the practice, goals, programs and services, achievements, and impact in numbers.) it could be shown as two tables (1 table for global , 1 table for regional."
                },
                {
                    "6. What are the local best practices (local experiences) similar or relevant to the project?":
                    "- Max 03: In the answer, mention the practice name, country, brief about the practice, goals, programs and services, achievements, and impact in numbers.)(Must provide the updated and reliable reference urls/sources/citations and web links)"
                },
            ]
        },
        "Operational Model": {
            "questions": [
                {
                    "1. Write the following in a table about the project (project brief, project objectives, target group, geographic scope, project duration).":
                    ""
                },
                {
                    "2. What is the appropriate operational business model for the project":
                    "- In this you can mention the units or departments that needed to execute the project.\n- How will be the collaboration and the integration happen between Different Roles and Departments.\n- Also describe how each unit will work and why it's important).\n- Show the operational model in a diagram.\n- Explain and Provide the Answer in a Detailed Table (columns: Units/Departments, Descriptions, Roles , COlloborations and Integrations) for Better understanding."
                },
            ]
        },
        "Methodology and Project Phases": {
            "questions": [
                {
                    """1. What methodology will be used to execute the project? What are the suitable phases to execute the project? (You provide the answer in tables (for each phase) including the following: phase name, brief about the phase, associated activities, deliverables, and timeframe.)\n2. What tools (these tools are not software Tools but more like Analysis Tools and Technique, Benchmarking Models, frameworks,Templates, Approaches, Methadologies, Consultation/Coaching Tools etc) are necessary for execution in each phase?""":
                    """(Provide Detailed answer)\nSome of the Examples for the Tools are Given Below:\n              {{\n  \"Planning and Strategy Phase\": [\n    \"SWOT Analysis\",\n    \"PESTEL Analysis\",\n    \"Balanced Scorecard\",\n    \"Gap Analysis\",\n    \"Scenario Planning\",\n    \"Stakeholder Analysis\",\n    \"Risk Assessment Matrix\",\n    \"Strategic Roadmapping\"\n  ],\n  \"Operational Implementation Phase\": [\n    \"Lean Six Sigma\",\n    \"Process Mapping\",\n    \"5S Methodology\",\n    \"Standard Operating Procedures (SOPs)\",\n    \"Key Performance Indicators (KPIs)\",\n    \"Gemba Walk\",\n    \"Kanban Boards\",\n    \"PDCA (Plan-Do-Check-Act) Cycle\"\n  ],\n  \"Quality Management Phase\": [\n    \"Total Quality Management (TQM)\",\n    \"Quality Function Deployment (QFD)\",\n    \"Failure Mode and Effects Analysis (FMEA)\",\n    \"Root Cause Analysis\",\n    \"Pareto Analysis\",\n    \"Control Charts\",\n    \"Ishikawa (Fishbone) Diagram\",\n    \"Benchmarking\"\n  ],\n  \"Human Resources and Training Phase\": [\n    \"Competency Frameworks\",\n    \"360-Degree Feedback\",\n    \"Learning Management Systems (LMS)\",\n    \"Succession Planning Models\",\n    \"Employee Engagement Surveys\",\n    \"Performance Improvement Plans (PIPs)\",\n    \"Mentoring and Coaching Programs\",\n    \"Skills Gap Analysis\"\n  ],\n  \"Financial Management Phase\": [\n    \"Cost-Benefit Analysis\",\n    \"Break-Even Analysis\",\n    \"Budgeting Models\",\n    \"Financial Ratio Analysis\",\n    \"Activity-Based Costing (ABC)\",\n    \"Cash Flow Forecasting\",\n    \"Return on Investment (ROI) Calculation\",\n    \"Variance Analysis\"\n  ],\n  \"Compliance and Risk Management Phase\": [\n    \"Compliance Checklists\",\n    \"Risk Registers\",\n    \"Internal Audit Frameworks\",\n    \"Incident Reporting Systems\",\n    \"Policy and Procedure Management Systems\",\n    \"Compliance Training Programs\",\n    \"Ethics Hotlines\",\n    \"Regulatory Change Management Tools\"\n  ],\n  \"Continuous Improvement Phase\": [\n    \"Kaizen Events\",\n    \"Plan-Do-Study-Act (PDSA) Cycle\",\n    \"5 Whys Technique\",\n    \"Suggestion Systems\",\n    \"Lean Waste Analysis\",\n    \"Benchmarking Databases\",\n    \"Continuous Improvement Maturity Models\",\n    \"Visual Management Boards\"\n  ]\n}}"""
                },
                {
                    "3. Divide each phase into several tasks that align with the deliverables. (Must ensure all Phases are enlisted)\n4. Place each task in a table as follows: phase name, task name, associated deliverable, brief about the task, how we will execute it step by step, and the proposed consulting tools that may help to execute this phase.":
                    ""
                },
                {
                    "5. from the tasks table, provide supporting and detailed information about each task and how to execute it (tools, techniques, frameworks, models, methodologies, matrices, tables, etc.). (for example: if there is a phase for getting feedback from the participants, we will use some of feedback tool like ethe survey) Provide a Tabular Response for each Task. Must ensure all the Phases are covered":
                    ""
                },
            ]
        },
        "Project Implementation Timeline": {
            "questions": [
                {
                    "1. What are the key dates and milestones within the timeline?\n2. How will time be allocated across the different phases of the project?\n3. What dependencies or sequencing are critical to maintaining the timeline?\n4. Please generate a Gantt chart showing each phase of the project?\n5. What criteria will be used to declare a milestone as successfully completed?":
                    ""
                },
            ]
        },
        "Project Team": {
            "questions": [
                {
                    "1. Who are the key members of the project team and what are their roles (enlist as Much Members as Possible and also their rleveant experiences so to give Value to the Project) ?\n2. Suggest a project team structure , and show How will the team structure support effective project execution?\n3. How will the team's expertise contribute to the success of the project?\n4. How will the team's collective experience help navigate project challenges?\n5. How will team collaboration be leveraged to maximize project outcomes?\n6. How does the team's expertise align with the client's expectations?":
                    "Provide concrete info based on company info and project info rather then abstract or general info.\n(use the team members from the Arewqeah company information and provide the concrete names and project Team)\nProvide the Team Structure in a Diagramatical Representation and allocate the Team Members to the Given Operational Models Units who could work in that Unit in a Table."
                },
            ]
        },
        "Why Arweqah": {
            "questions": [
                {
                    "1. What are Arweqah's unique strengths and capabilities relevant to this project RFP?":
                    ""
                },
            ]
        },
        "Our Global and Local Partnerships": {
            "questions": [
                {
                    "1. What global and local partnerships does Arweqah have that are relevant to this project? (just mention the name of partners)\n2. Mention Arweqah other partners, who are not related to the project.":
                    ""
                },
            ]
        },
        "Arweqah Memberships": {
            "questions": [
                {
                    "1. What professional memberships and affiliations does Arweqah hold? (just mention these memberships)":
                    ""
                },
            ]
        },
        "Our Relevant Experience and Previous Projects": {
            "questions": [
                {
                    "1. What are some examples of similar projects that Arweqah has successfully completed? (focus more the Relevant Projects we did and Discssed in the Competive Advantage Section) (just mention these project and give a brief of each one as follow : description, main deliverables, clients, geographical region)":
                    ""
                },
            ]
        }
    }


def update_structure(scope_of_work):
    formatted_data = {}
    for key, value in scope_of_work.items():
        formatted_questions = []
        for question_dict in value["questions"]:
            for question, answer in question_dict.items():
                if answer.strip():
                    formatted_questions.append(
                        {f"{question}\nRequired Answer: \n{answer}": ""})
                else:
                    formatted_questions.append({f"{question}": ""})
        formatted_data[f"# {key}"] = {"questions": formatted_questions}
    return formatted_data


def Pormpt_customization():
    st.subheader("Prompts Customization")

    def display_questions():
        for section, content in st.session_state.scope_of_work.items():
            with st.expander(section):
                for question_dict in content["questions"]:
                    for question, required_answer in question_dict.items():
                        edited_answer = st.text_area(label=question,
                                                     value=required_answer,
                                                     height=100)
                        question_dict[question] = edited_answer

    display_questions()
    if st.button("Save", use_container_width=True):
        st.success("Changes saved!")
        st.session_state.scope_of_work = st.session_state.scope_of_work
    with st.expander("View Structure"):
        st.json(st.session_state.scope_of_work)


def proposal_writer():
    st.subheader("Upload Request for Proposal")
    formatted_data = update_structure(st.session_state.scope_of_work)
    with st.expander("View Structure"):
        st.json(formatted_data)
    rfp_file = st.file_uploader("Choose a file for Request for Proposal",
                                type=['csv', 'xlsx', 'txt', 'pdf'])

    focus = st.text_input("focused Instructions")
    btn = st.button("Generate Proposal", use_container_width=True)
    save_path = None

    if 'full_response' not in st.session_state:
        st.session_state['full_response'] = None

    if rfp_file is not None and btn:
        # Save the uploaded file temporarily
        save_path = os.path.join("tempDir", rfp_file.name)
        os.makedirs(os.path.dirname(save_path), exist_ok=True)

        with open(save_path, "wb") as f:
            f.write(rfp_file.getbuffer())

        # Process the file and store the results in session state
        with st.spinner('Processing files and Generating Proposal...'):
            SaveTextFromPDF(save_path, "rfpInfo.pkl")
            st.session_state['full_response'] = InvokeAgent(
                focus, formatted_data)

    if st.session_state['full_response'] is not None:
        full_response = st.session_state['full_response']

        st.markdown("---")
        st.write("\n\n")

        with st.expander("Open English Proposal"):

            st.markdown(full_response['English_proposal'])
            st.write("\n\n")
            convert(full_response['English_proposal'], "english.html")

            with open('english.html', 'r', encoding='utf-8') as file:
                html_content = file.read()
            html_to_word(html_content, "english.docx", "English Proposal")
            process_document('english.docx',
                             'Technical_proposal_english.docx',
                             apply_rtl=False)

        with st.expander("Open Arabic Variant"):
            st.markdown(f"""
    <div style="text-align: right; direction: rtl;">
                        {full_response['arabic_proposal']}
                    </div>
                    """,
                        unsafe_allow_html=True)
            st.write("\n\n")
            convert(full_response['arabic_proposal'], "arabic.html")
            with open('arabic.html', 'r', encoding='utf-8') as file:
                html_content = file.read()
            html_to_word(html_content, "arabic.docx", "Arabic Proposal")
            process_document('arabic.docx',
                             'Technical_proposal_arabic.docx',
                             apply_rtl=True)

        with open('Technical_proposal_english.docx', 'rb') as file:
            st.download_button(
                label="Download English Proposal",
                data=file,
                file_name="Technical_proposal_english.docx",
                mime=
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

        with open('Technical_proposal_arabic.docx', 'rb') as file:
            st.download_button(
                label="Download Arabic Proposal",
                data=file,
                file_name="Technical_proposal_arabic.docx",
                mime=
                "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
            )

    else:
        st.error("Please upload RFP File.")


st.sidebar.image("شعار_أروقة_page-0001-removebg-preview.png",
                 caption="Arweqah Proposal Generation AI")
st.sidebar.subheader("Page Selection")
page = st.sidebar.selectbox("Choose a page",
                            ["Proposal Writing", "Prompt Customization"])

# Display content based on selected page
if page == "Proposal Writing":
    proposal_writer()
elif page == "Prompt Customization":
    Pormpt_customization()
