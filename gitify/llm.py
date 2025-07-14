import tiktoken
from openai import OpenAI

from gitify.__init__ import (DEFAULT_MODEL, MODEL_INPUT_COST, SYSTEM_PROMPT,
                             SYSTEM_PROMPT_LENGTH)


def get_tokens_cost(diff_text, model):
  tokens = get_tokens_length(diff_text, model)
  model_cost = MODEL_INPUT_COST[model] / 1e6
  total_cost = round(model_cost * tokens, 2)

  return total_cost


def get_tokens_length(diff_text, model):
  encoding = tiktoken.encoding_for_model(
      'gpt-4'
  )  # TODO: fix this here from gpt-4 to search for model if family gpt then gpt-4 else just chars()/4 for token estimation
  user_prompt = f"Git diff:\n\n{diff_text}"
  tokens = encoding.encode(user_prompt)
  total_tokens = len(tokens) + SYSTEM_PROMPT_LENGTH

  return total_tokens


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
