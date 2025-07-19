import tiktoken
from openai import OpenAI

from gitify.__init__ import (DEFAULT_MODEL, MODEL_INPUT_COST, SYSTEM_PROMPT,
                             SYSTEM_PROMPT_LENGTH)


def get_tokens_cost(diff_text, model):
  tokens = get_tokens_length(diff_text, model)
  model_cost_per_token = MODEL_INPUT_COST[model] / 1e6
  total_cost = round(model_cost_per_token * tokens, 2)

  return total_cost


def get_tokens_length(diff_text, model):
  if 'gpt' in model:
    encoding = tiktoken.encoding_for_model('gpt-4')
    diff_prompt = f"Git diff:\n\n{diff_text}"
    diff_tokens = len(encoding.encode(diff_prompt))
  else:
    diff_tokens = len(diff_text) / 4

  total_tokens = diff_tokens + SYSTEM_PROMPT_LENGTH

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
