# :cherry_blossom: free-genai-bootcamp-2025 :cherry_blossom:

:white_flower: https://genai.cloudprojectbootcamp.com/ :white_flower:

# This is an experiment as part of Bootcamp activity (see above) and uses Octotools - see below
- https://octotools.github.io/
- https://github.com/octotools/octotools

# @Andrew see 

new model defn
- octotools/octotools/engine/gemini.py

LLM connectivity checks (add API_KEYS in env)
- octotools/test_gpt.py
- octotools/test_gemini.py

new tool 'cards'
- octotools/octotools/tools/python_code_generator_gemini/tool.py
- octotools/octotools/tools/japanese_tokenizer/tool.py
- test tools in isolation with 'python tool.py' from *within* a tool's directory 

new task defn in 
- octotools/tasks/random_japanese_saying
- test tasks in isolation with './random_japanese_saying/quick_demo.sh' from folder *above* the task i.e. /octotools/tasks

sample outputs and wk3 journal in
- wk3 agent notes/
- AGENTEXP.MD