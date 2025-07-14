import tiktoken
from openai import OpenAI

from gitify.__init__ import DEFAULT_MODEL, SYSTEM_PROMPT, SYSTEM_PROMPT_LENGTH

#TODO: create a get_tokens_cost method here so


def get_tokens_length(diff_text, model):
  encoding = tiktoken.encode_for_model(model)

  user_prompt = f"Git diff:\n\n{diff_text}"
  tokens = encoding.encode(user_prompt)

  return len(tokens) + SYSTEM_PROMPT_LENGTH


def generate_commit_message(diff_text, api_key, model=DEFAULT_MODEL):
  client = OpenAI(api_key=api_key)

  user_prompt = f"Git diff:\n\n{diff_text}"

  response = client.chat.completions.create(model=model,
                                            messages=[{
                                                "role": "system",
                                                "content": SYSTEM_PROMPT
                                            }, {
                                                "role": "user",
                                                "content": user_prompt
                                            }],
                                            temperature=0.4,
                                            max_tokens=300)

  return response.choices[0].message.content.strip()
