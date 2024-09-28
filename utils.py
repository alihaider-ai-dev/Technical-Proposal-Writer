from anthropic import Anthropic
from openai import OpenAI
import os

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")
claude_apikey = os.getenv("ANTHROPIC_API_KEY")
client_claude = Anthropic(api_key=claude_apikey, )
client_openai = OpenAI()


def generate_answer(content, task, model):
    prompt = f"""
    {task}

    {content}
    """
    if model == "claude":
        message = client_claude.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=8192,
            extra_headers={
                "anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"
            },
            temperature=0.0,
            system=
            "You think a Social Innovtaion and leadership program Agency and your main goal is to Develop a Proposal for the Request for Proposal. Do not cut off the Content Must Complete it till the Last heading in the Given Table.",
            messages=[{
                "role": "user",
                "content": prompt
            }])
        content = message.content[0]
        response_text = content.text
    elif model == "openai":
        completion = client_openai.chat.completions.create(
            model="gpt-4o",
            messages=[{
                "role":
                "system",
                "content":
                "Your main Task is Exaclty replicate the content from English to Arabic Do not miss a single word to be Translated from english to arabic."
            }, {
                "role": "user",
                "content": prompt
            }])
        response_text = completion.choices[0].message.content
    elif model == "claude_for_translation":
        message = client_claude.messages.create(
            model="claude-3-5-sonnet-20240620",
            max_tokens=8192,
            extra_headers={
                "anthropic-beta": "max-tokens-3-5-sonnet-2024-07-15"
            },
            temperature=0.0,
            system=
            "Your main Task is Exaclty replicate the content from English to Arabic Do not miss a single Block or section to be Translated from english to arabic.",
            messages=[{
                "role": "user",
                "content": prompt
            }])
        content = message.content[0]
        response_text = content.text
    return response_text
