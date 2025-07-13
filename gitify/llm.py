import openai


def generate_commit_message(diff_text, api_key, model='gpt-4'):
  openai.api_key = api_key

  prompt = f"Write a concise Git commit message for the following diff:\n\n{diff_text}"
  response = openai.ChatCompletion.create(model=model,
                                          messages=[{
                                              "role": "user",
                                              "content": prompt
                                          }],
                                          temperature=0.7)

  return response['choices'][0]['message']['content'].strip()
