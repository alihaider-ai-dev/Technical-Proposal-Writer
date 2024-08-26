import nest_asyncio
from dotenv import load_dotenv
import os

load_dotenv()
nest_asyncio.apply()
from llama_parse import LlamaParse
import pickle

parser = LlamaParse(
    api_key=os.getenv("LLAMA_PARSE_KEY"),
    result_type="markdown",  # "markdown" and "text" are available
    num_workers=4,  # if multiple files passed, split in `num_workers` API calls
    verbose=True,
    language="en",  # Optionally you can define a language, default=en
)


def save_text_to_pkl(text, filename):
    with open(filename, 'wb') as file:
        pickle.dump(text, file)


def read_text_from_pkl(filename):
    with open(filename, 'rb') as file:
        text = pickle.load(file)
    return text


def SaveTextFromPDF(path, name):
    documents = parser.load_data(path)
    print(documents)
    text = ""
    for doc in documents:
        text += doc.text + "\n"
    print(text)
    save_text_to_pkl(text, name)
