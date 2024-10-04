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


st.sidebar.image("شعار_أروقة_page-0001-removebg-preview.png",
                 caption="Arweqah Proposal Generation AI")

st.subheader("Upload Request for Proposal")
scope_of_work = {
    "# Our Understanding of the Scope of Work": {
        "questions": [
            {
                """
            What are the client's main objectives and goals for the RFP project? (provide the Detailed Answer)
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
            Required Answer: (Give some state about the following in a Table: market size – targeted segments (which also explains the percentage of the population/seekers being considered/Instrested or tragetted ) – any other relevant state - ...)
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
            Also Add the Heading 'local best practices'
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
                """What is the appropriate operational business model for the project 
                (
                In this you can mention the units or departments that needed to execute the project.
                How will be the collaboration and the integration happen between Different Roles and Departments.
                Also describe how each unit will work and why it's important).
                Show the operational model in a diagram.
                Explain and Provide the Answer in a Detailed Table (columns: Units/Departments, Descriptions, Roles , COlloborations and Integrations) for Better understanding. 
                """:
                ""
            },
        ]
    },
    "# Methodology and Project Phases": {
        "questions": [
            {
                """
              What methodology will be used to execute the project? What are the suitable phases to execute the project? (You provide the answer in tables (for each phase) including the following: phase name, brief about the phase, associated activities, deliverables, and timeframe.)
              What tools (these tools are not software Tools but more like Analysis Tools and Technique, Benchmarking Models, frameworks,Templates, Approaches, Methadologies, Consultation/Coaching Tools etc) are necessary for execution in each phase? 
              Some of the Examples are Given Below:
                              {
                  "Planning and Strategy Phase": [
                    "SWOT Analysis",
                    "PESTEL Analysis",
                    "Balanced Scorecard",
                    "Gap Analysis",
                    "Scenario Planning",
                    "Stakeholder Analysis",
                    "Risk Assessment Matrix",
                    "Strategic Roadmapping"
                  ],
                  "Operational Implementation Phase": [
                    "Lean Six Sigma",
                    "Process Mapping",
                    "5S Methodology",
                    "Standard Operating Procedures (SOPs)",
                    "Key Performance Indicators (KPIs)",
                    "Gemba Walk",
                    "Kanban Boards",
                    "PDCA (Plan-Do-Check-Act) Cycle"
                  ],
                  "Quality Management Phase": [
                    "Total Quality Management (TQM)",
                    "Quality Function Deployment (QFD)",
                    "Failure Mode and Effects Analysis (FMEA)",
                    "Root Cause Analysis",
                    "Pareto Analysis",
                    "Control Charts",
                    "Ishikawa (Fishbone) Diagram",
                    "Benchmarking"
                  ],
                  "Human Resources and Training Phase": [
                    "Competency Frameworks",
                    "360-Degree Feedback",
                    "Learning Management Systems (LMS)",
                    "Succession Planning Models",
                    "Employee Engagement Surveys",
                    "Performance Improvement Plans (PIPs)",
                    "Mentoring and Coaching Programs",
                    "Skills Gap Analysis"
                  ],
                  "Financial Management Phase": [
                    "Cost-Benefit Analysis",
                    "Break-Even Analysis",
                    "Budgeting Models",
                    "Financial Ratio Analysis",
                    "Activity-Based Costing (ABC)",
                    "Cash Flow Forecasting",
                    "Return on Investment (ROI) Calculation",
                    "Variance Analysis"
                  ],
                  "Compliance and Risk Management Phase": [
                    "Compliance Checklists",
                    "Risk Registers",
                    "Internal Audit Frameworks",
                    "Incident Reporting Systems",
                    "Policy and Procedure Management Systems",
                    "Compliance Training Programs",
                    "Ethics Hotlines",
                    "Regulatory Change Management Tools"
                  ],
                  "Continuous Improvement Phase": [
                    "Kaizen Events",
                    "Plan-Do-Study-Act (PDSA) Cycle",
                    "5 Whys Technique",
                    "Suggestion Systems",
                    "Lean Waste Analysis",
                    "Benchmarking Databases",
                    "Continuous Improvement Maturity Models",
                    "Visual Management Boards"
                  ]
                }
              (Provide Detailed answer)
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
            Who are the key members of the project team and what are their roles (enlist as Much Members as Possible and also their rleveant experiences so to give Value to the Project) ?
            Required Answer:
              Suggest a project team structure , and show How will the team structure support effective project execution?
              "How will the team's expertise contribute to the success of the project?"
              "How will the team’s collective experience help navigate project challenges?"
              "How will team collaboration be leveraged to maximize project outcomes?"
              "How does the team’s expertise align with the client’s expectations?"
              Provide concrete info based on company info and project info rather then abstract or general info.
             
              (use the team members from the Arewqeah company information and provide the concrete names and project Team)
              Provide the Team Structure in a Diagramatical Representation and allocate the Team Members to the Given Operational Models Units who could work in that Unit in a Table.
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
                """
                What are some examples of similar projects that Arweqah has successfully completed? (focus more the Relevant Projects we did and Discssed in the Competive Advantage Section) (just mention these project and give a brief of each one as follow : description, main deliverables, clients, geographical region)""":
                ""
            },
        ]
    }
}
if "scope_of_work" not in st.session_state:
    st.session_state.scope_of_work = scope_of_work
    

if st.button("Edit Prompts"):
    st.subheader("RFP Project Questions Editor")
    def display_questions():
        for section, content in st.session_state.scope_of_work.items():
            with st.expander(section, expanded=True):
                for question_dict in content["questions"]:
                    for question, required_answer in question_dict.items():
                        edited_answer = st.text_area(label=question,value=required_answer, height=100)
                        question_dict[question] = edited_answer
    display_questions()
    
    if st.button("Save"):
        # Print the updated structure in JSON format
        formatted_data = {}
        for key, value in st.session_state.scope_of_work.items():
            formatted_questions = []
            for question_dict in value["questions"]:
                for question, answer in question_dict.items():
                    if answer.strip():
                        formatted_questions.append({f"{question}\nRequired Answer: \n{answer}":""})
                    else:
                        formatted_questions.append({f"{question}":""})
            formatted_data[f"# {key}"] = {"questions": formatted_questions}
        st.session_state.scope_of_work = formatted_data
        st.success("Changes saved!")
      
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
        st.session_state['full_response'] = InvokeAgent(focus, st.session_state.scope_of_work)

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
