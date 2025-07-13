from openai import OpenAI

from gitify.__init__ import defaultModel


def generate_commit_message(diff_text, api_key, model=defaultModel):
  client = OpenAI(api_key=api_key)
  systemPrompt = """
  You are a helpful assistant that writes Git commit messages.

  Write a **concise and descriptive** Git commit message (in imperative mood, like "Fix bug", "Add feature") based on the following Git diff. Focus on summarizing the **purpose and effect** of the changes, not implementation details.

  - Limit to **a single sentence** per significant change made.
  - Output **only** the commit message.

  """

  userPrompt = f"Git diff:\n\n{diff_text}"

  response = client.chat.completions.create(model=model,
                                            messages=[{
                                                "role": "system",
                                                "content": systemPrompt
                                            }, {
                                                "role": "user",
                                                "content": userPrompt
                                            }],
                                            temperature=0.4,
                                            max_tokens=300)

  return response.choices[0].message.content.strip()
