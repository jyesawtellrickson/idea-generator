# Research Idea Generator 
# 研究想法產生器

Generate research ideas using LLMs.
使用法學碩士產生研究想法。

## Setup

You should install the requirements with conda
```sh
conda install --yes --file requirements.txt
```

Make sure to get ollama running before, e.g. on Windows:
```sh
ollama serve
```



You can run the app by using:
```sh
python main.py
```

This will begin the conversation with the LLM.


# LLM setup
There are lots of ways to set LLMs up.
1. Using Ollama on different operating system(e.g. Windows, MacOS, Linux), more details in https://github.com/ollama/ollama.
2. Using VLLM by one command in conda environment.
   ```sh
   (env) pip install vllm
   ```
   Requirements: Linux OS, Python3.9-3.12(perfer 3.12) 
                 GPU: compute capability 7.0 or higher (e.g., V100, T4, RTX20xx, A100, L4, H100, etc.)
   More details in https://github.com/vllm-project/vllm.

# How to start LLMs after installation?
1. In Windows, open your terminal and key in:
   ```sh
   ollama run [LLM name]
   ```
   LLMs information on https://ollama.com/library.
2. The command line will enter dialog box after running, as picture showing.
   ![image](https://github.com/user-attachments/assets/41126d11-5d85-4da3-84c4-613d11bf69fa)

# Next Steps

Leverage Concept Net
Show thinking / downloaded research papers on the right.


Model user intent, then use validation, i.e. predict if you should return a list of ideas, if so, validate they are numbered and only 5. ValidationNode


[P2] 1. Diversity of Input Sources
Semantic Scholar?

[P2] 2. Idea Scoring and Categorization
Current Limitation: The generated ideas are not explicitly scored or categorized for impact, novelty, and feasibility.
Improvement:
Implement a scoring system based on these metrics. Use external tools or APIs (e.g., GPT-based models) to assess and rank ideas.
Group ideas into categories (e.g., applied, theoretical, high-risk/high-reward).

3. Enhanced Review Process
Current Limitation: Idea review appears limited to a single pass with user feedback.
Improvement:
Introduce iterative review cycles where suggestions are refined through multiple rounds.
Allow the system to provide structured feedback (e.g., SWOT analysis).

4. Multi-Agent Collaboration
Current Limitation: The agent is single-threaded and focuses on linear interactions.
Improvement: Use a multi-agent architecture where specialized agents (e.g., one for feasibility, one for literature depth) collaborate and debate to refine ideas.

5. Interactive Visualizations
Current Limitation: Text-only interaction limits the user experience.
Improvement:
Generate concept maps or flowcharts for ideas.
Use tools like Plotly or D3.js to visually represent relationships between research areas or potential impacts.

6. Personalization
Current Limitation: System prompts and tools are static.
Improvement:
Add user profiling to tailor idea generation based on expertise, preferences, and history.
Include adaptive prompts to guide idea generation dynamically based on user input.

7. Continuous Learning
Current Limitation: The agent doesn't learn from user interactions.
Improvement:
Implement a memory system (e.g., LangChain MemorySaver) to retain and evolve based on past sessions.
Use reinforcement learning to optimize idea quality based on user feedback.

8. Transparency in Idea Origin
Current Limitation: Users may not always know how ideas are grounded in research.
Improvement:
Provide citations or summaries from the ArXiv papers that inspired each idea.
Show a traceable lineage of the thought process for generated ideas.

9. Scenario Testing
Current Limitation: Ideas might not account for practical implementation scenarios.
Improvement:
Add a scenario simulator where users can test how ideas would work under certain constraints.
Use reasoning models to predict potential challenges or successes in specific applications.

10. Interface Improvements
Current Limitation: Interaction is command-line based, which can be limiting.
Improvement:
Develop a GUI or integrate it into platforms like Slack or Microsoft Teams for more accessible interactions.