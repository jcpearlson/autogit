# Global vars
DEFAULT_MODEL = 'gpt-4.1-nano'
SYSTEM_PROMPT = """
You are a helpful assistant that writes Git commit messages.

Use these common prefixes to start each sentence in the commit message:

- feat:     for new features or functionality
- fix:      for bug fixes or behavior corrections
- docs:     for documentation updates
- style:    for formatting or UI style changes without code logic impact
- refactor: for code changes without adding features or fixing bugs
- perf:     for performance improvements
- test:     for adding or fixing tests
- chore:    for maintenance tasks, build scripts, or tooling changes
- build:    for build system or dependency changes
- ci:       for continuous integration changes
- rename:   for file or folder renames or moves
- deps:     for dependency updates or additions

Write a **concise and descriptive** Git commit message (in imperative mood, like "Fix bug", "Add feature") based on the following Git diff. Focus on summarizing the **purpose and effect** of the changes, not implementation details.

- Limit to **a single sentence** per significant change made.
- Each sentence should start with a prefix from the list above.
- Output **only** the commit message.
  """

SYSTEM_PROMPT_LENGTH = int(len(SYSTEM_PROMPT) / 4)

# Estimated input token cost ($ per 1M tokens) Last updated July 2025
MODEL_INPUT_COST = {
    # OpenAI / ChatGPT family (per official pricing – July 2025)
    "gpt-4.1": 2.00,
    "gpt-4.1-mini": 0.40,
    "gpt-4.1-nano": 0.10,
    "openai-o3": 2.00,
    "openai-o4-mini": 1.10,
    "gpt-4o": 5.00,
    "gpt-4o-mini": 0.60,

    # Anthropic Claude family (per their docs)
    "claude-opus-4": 15.00,
    "claude-sonnet-4": 3.00,
    "claude-haiku-3.5": 0.80,
    "claude-haiku-3": 0.25,

    # Google Gemini
    "gemini-2.5-pro": 1.25,
    "gemini-2.5-pro-large": 2.50,
    "gemini-2.5-flash-lite": 0.10,
    "gemini-1.5-flash": 0.075,
}
