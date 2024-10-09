# Arweqah Proposal Generation AI

## Project Overview

This project is a Streamlit-based web application for generating technical proposals for Arweqah, a company working in social awareness and leadership programs based in Saudi Arabia. The application allows users to upload Request for Proposal (RFP) documents, customize prompts, and generate detailed technical proposals in both English and Arabic.

## Features

1. Upload and process RFP documents
2. Customize proposal prompts
3. Generate technical proposals using AI
4. Produce proposals in both English and Arabic
5. Download generated proposals as Word documents

## Installation

1. Clone the repository
2. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set up environment variables in a `.env` file:
   ```
   LANGCHAIN_API_KEY=your_langchain_api_key
   OPENAI_API_KEY=your_openai_api_key
   ANTHROPIC_API_KEY=your_anthropic_api_key
   LLAMA_PARSE_KEY=your_llama_parse_key
   ```

## Usage

1. Run the Streamlit app:
   ```
   streamlit run app.py
   ```
2. Use the sidebar to navigate between "Proposal Writing" and "Prompt Customization" pages
3. Upload an RFP document and generate a proposal
4. Customize prompts as needed
5. Download the generated proposals in Word format

## Project Structure

- `main.py`: Main Streamlit application
- `ProposalWriterAgent.py`: Contains the `InvokeAgent` function for generating proposals
- `DataIngestion.py`: Handles file reading and processing
- `utils.py`: Utility functions for generating responses using various AI models
- `saving_utils.py`: Functions for saving and reading data
- `document_utils.py`: Functions for document processing

## Key Components

### Proposal Generation

The `InvokeAgent` function in `ProposalWriterAgent.py` is responsible for generating the proposal. It uses the Anthropic API to generate responses for each section of the proposal.

### Language Models

The project uses multiple language models:
- Claude 3.5 Sonnet (Anthropic) for generating proposal content
- GPT-4 (OpenAI) for translations (optional)

### Data Processing

- `LlamaParse` is used for parsing PDF documents
- Pickle is used for saving and loading processed data

### User Interface

The Streamlit app provides two main pages:
1. Proposal Writing: For uploading RFPs and generating proposals
2. Prompt Customization: For customizing the prompts used in proposal generation

## Customization

Users can customize the proposal structure and prompts by modifying the `scope_of_work` dictionary in the `main.py` file.

## Output

The application generates:
1. An English proposal
2. An Arabic translation of the proposal
3. Downloadable Word documents for both versions

## Notes

- Ensure all API keys are properly set in the `.env` file
- The application uses a predefined company information file (`Arweqah_company_information.pkl`)
- The generated proposals are formatted using Markdown

## Dependencies

- Streamlit
- Anthropic
- OpenAI
- python-dotenv
- llama_parse
- langchain
- (other dependencies as listed in `requirements.txt`)

## Future Improvements

- Implement error handling and retry mechanisms for API calls
- Add more customization options for proposal structure
- Improve the Arabic translation process
- Implement user authentication and proposal saving features
