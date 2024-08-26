import streamlit as st
from DataIngestion import SaveTextFromPDF, read_text_from_pkl
from ProposalWriterAgent import InvokeAgent
import os

st.set_page_config(page_icon="💬", layout="wide", page_title="Proposal AI")


def icon(emoji: str):
    """Shows an emoji as a Notion-style page icon."""
    st.write(
        f'<span style="font-size: 78px; line-height: 1">{emoji}</span>',
        unsafe_allow_html=True,
    )


st.header("Proposal Writer", divider="rainbow", anchor=False)

st.subheader("Upload Request for Proposal")
rfp_file = st.file_uploader("Choose a file for Request for Proposal",
                            type=['csv', 'xlsx', 'txt', 'pdf'])

btn = st.button("Generate Proposal", use_container_width=True)
save_path = None
if rfp_file is not None and btn:
    # Save the uploaded file temporarily
    save_path = os.path.join("tempDir", rfp_file.name)

    # Create the directory if it doesn't exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)

    with open(save_path, "wb") as f:
        f.write(rfp_file.getbuffer())

if rfp_file and btn:
    with st.spinner('Processing files and Generating Proposal...'):
        SaveTextFromPDF(save_path, "rfpInfo.pkl")
        full_response = InvokeAgent()
        st.markdown("---")
        st.write("\n\n")

        with st.expander("Open English Proposal"):
            english_text = ""
            for item in full_response:
                english_text += item['english_subsection']
                st.markdown(item['english_subsection'])
                st.write("\n\n")

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

else:
    st.error("Please upload RFP File.")
