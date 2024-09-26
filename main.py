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
        st.session_state['full_response'] = InvokeAgent(focus)

if st.session_state['full_response'] is not None:
    full_response = st.session_state['full_response']

    st.markdown("---")
    st.write("\n\n")

    with st.expander("Open English Proposal"):
        english_text = ""
        for item in full_response:
            english_text += item['english_subsection']
            st.markdown(item['english_subsection'])
            st.write("\n\n")

        convert(english_text, "english.html")
        with open('english.html', 'r', encoding='utf-8') as file:
            html_content = file.read()
        html_to_word(html_content, "english.docx", "English Proposal")
        process_document('english.docx',
                         'Technical_proposal_english.docx',
                         apply_rtl=False)

    with st.expander("Open Arabic Variant"):
        arabic_text = ""
        for item in full_response:
            arabic_text += item['arabic_subsection']
            st.markdown(f"""
<div style="text-align: right; direction: rtl;">
                    {item['arabic_subsection']}
                </div>
                """,
                        unsafe_allow_html=True)
            st.write("\n\n")
        convert(arabic_text, "arabic.html")
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
