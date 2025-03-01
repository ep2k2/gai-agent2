#

Given a common Japanese phrase (saying, proverb, tongue twister) parse and return a json structured list of japanese vocabulary in dictionary-from along with grammar information (parts of speech etc.), along with a JLPT Nx level 

# Target Technical spec
- Python: write simple pythonic code
- LLM: use GPT4o (we may try Gemini 2.0 Flash as well)
- Japanese: use yomi for tokenization (web service or local code as needed)
- ~use uv as package manager and for virtual environments~ 1st attempt
- use conda as virtual environment


# Technical uncertainty
- how strong the 'reasoning' of the target LLM model needs to be in order to make effective function-calling tool use
- how easy to extend to new tools ('tool card' in Octotools-speak)
-- octotools with a new custom tool 'card' is in practice (in this case a non-LLM tool)
-- as Japanese tokeniser (including morphological analysis) web API using yomi https://github.com/ookii-tsuki/yomi https://ookii-tsuki.github.io/yomi/
--- a possible alternative might be local code using e.g. https://github.com/mocobeta/janome;
- whether an additional tool to check and enforce a JSON schema is necessary to consistently return valid and consistent JSON

# Approach
- clone https://github.com/octotools/octotools
- create a new virtual environment using Conda
- test install using build in items
-- cd octotools/tools/python_code_generator
-- python tool.py
- connect to OpenAI GPT and Google Gemini APIs
-- double check .gitignore
-- test connectivity
- create a new tool card
-- implement new tool following the structure of existing tools as stored in the octotools/tools directory
-- enable tool by configuring subset of tools for tasks by setting the enabled_tools argument in tasks/solve.py
-- consider JsonSchema

# Plan tracking

## Install and connectivity
- [x] Install Conda
- [x] Clone octotools repository
- [X] install repo requirements (including parallels if want to run full comparitive tests)
- [x] Create and activate virtual environment using Conda
- [x] Create new engine definition for Gemini based on the OpenAI engine def
- [x] Create .env file and include API_KEY(s)
- [x] Verify .gitignore includes .env
- [x] Test ChatGPT API connectivity manually
- [x] Test Gemini API connectivity manually
- [x] Create new python_code_generator_gemini entry in based on OpenAI version 
- [x] Test basic octotools installation using python_code_generator_gemini/tool.py

## Development Phase 1 - Core Implementation
- [x] Create new 'card' tool in octotools/tools directory
- [x] Define tool structure and interface
- [x] Make sure Gemini API is configured to be constrained to return JSON output
      https://ai.google.dev/gemini-api/docs/structured-output?lang=python
- [x] Implement basic function calling
- [x] Configure tool in tasks/solve.py
- [x] Test basic tool functionality / check JSON output structure

## Development Phase 2 - Japanese Processing
- [x] Integrate yomi API for Japanese tokenization
- [x] Test API connectivity
- [x] Implement tokenization logic

## Development Phase 3 - Agent task
- [x] create task structure prompt
- [x] test running - important: framework is setup to need the call from the solve.py folder i.e. from octotools/octotools/tasks run ./random_japanese_saying/quick_demo.sh

## Development Phase 4 - Agent actually use the task
- [x] iterate task definition (and prompt) so that agent recognises that the new tool is worth using for task(!)

## Optional Extensions
- [ ] consider implementing local tokenization using janome
- [ ] consider exploring structured/constrained output e.g. https://ai.google.dev/gemini-api/docs/structured-output?lang=python
- [ ] consider adding a JSON schema tool explicitly (but I'm not confident the model would choose to use it)