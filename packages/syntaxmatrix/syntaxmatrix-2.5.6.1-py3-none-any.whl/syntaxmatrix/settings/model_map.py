import json
import os


PROVIDERS_MODELS = {
    #1
    "openai": [  
        "gpt-5.1",
        "gpt-5.1-chat-latest",
        "gpt-5.1-codex-mini",
        "gpt-5.1-codex",
        "gpt-5",
        "gpt-5-nano",
        "gpt-5-mini", 
        "gpt-4.1", 
        "gpt-4.1-nano",
        "gpt-4.1-mini",                 
        "gpt-4o-mini",
        "gpt-4o",
    ],
    #2
    "google": [    
        "gemini-3-pro-preview",                
        "gemini-2.5-flash-lite",
        "gemini-2.5-flash",
        "gemini-2.5-pro",
        "gemini-2.0-flash-lite",
        "gemini-2.0-flash",
    ],
    #3
    "xai": [    
        "grok-4",                    
        "grok-3-mini-fast",
        "grok-3-mini",
        "grok-3",
        
    ],
    #4
    "deepseek": [                    
        "deepseek-chat",
    ],
    #5
    "moonshot": [
        "kimi-k2-0905-preview",
    ],
    #6
    "alibaba": [   
        "qwen-flash",  
        "qwen-plus",                
        "qwen3-coder-plus",
        "qwen-max",
    ],
    #7
    "anthropic": [
        "claude-opus-4-5",
        "claude-opus-4-1",
        "claude-sonnet-4-5",
        "claude-sonnet-4-0",
        "claude-3-5-haiku-latest",
        "claude-3-haiku-20240307",
    ]
}


# Read-only model descriptions for LLM-profile builder
# -----------------------------------------------------------------------------
MODEL_DESCRIPTIONS = {
    #1. OpenAI                       
    "gpt-4o-mini":"Cost-efficient multimodal; $0.15/1M input, $0.60/1M output. Ideal for prototyping vision+text apps on a budget.",

    "gpt-4o":"Multimodal powerhouse; $5.00/1M input, $15.00/1M output. Best for high-fidelity chat, complex reasoning & image tasks.",
    
    "gpt-4.1-nano":"Ultra-fast low-cost (1M-token); $0.10/1M in, $0.40/1M out. Perfect for high-throughput, low-latency tasks.",

    "gpt-4.1-mini":"Balanced speed/intel (1M-token context); $0.40/1M in, $1.60/1M out. Great for apps needing wide context at moderate cost.",

    "gpt-4.1":"Top general-purpose (1M-token context); $2.00/1M in, $8.00/1M out. Excels at large-doc comprehension, coding, reasoning.",

    "gpt-5-chat-latest":"""gpt-5-main. """,

    "gpt-5-nano":"""gpt-5-thinking-nano. In/Out €0.043/€0.344 (cached in €0.004).  
    Fastest/lowest cost; ideal for short prompts, tagging, and rewrite flows; tools supported. 
    Best for:
    1.  High-volume classification/moderation
    2.  Copy clean-up and templated rewrites
    3.  Lightweight summarisation and routing

    Use cases:
    a.  Real-time content moderation and policy tagging.
    b.  Bulk product description normalisation with style rules.
    c.  News/article triage to decide which items warrant a deeper pass.
    """,

    "gpt-5-mini":"""gpt-5-thinking-mini. In/Out $0.25/$2 (cached in $0.025). 
    Cheaper, faster variant with broad task coverage; still supports tools and long context. 
    Best for:
    1.  Production chatbots at scale
    2.  Mid-complexity RAG/extraction pipelines
    3.  Batch summarisation with occasional tool calls
    Use cases:
    a.  Customer support copilot that classifies intent, drafts replies, and calls ticketing APIs.
    b.  Meeting-notes pipeline: diarised summary, actions, CRM updates.
    c.  ETL enrichment: pull facts from documents into structured JSON.
    """,
    
    "gpt-5":"""gpt-5-thinking. In/Out $1.25/$10.00 (cached in $0.125). 
    Advanced reasoning and tool use; strong code generation/repair; robust long-context handling (400k). 
    Best for:
    1. Complex agentic workflows and planning
    2. Long-context RAG and analytics
    3. High-stakes coding assistance (multi-file changes & tests) 
    Use cases:
    a.  An autonomous “data room” analyst reading hundreds of PDFs and producing audit-ready briefs.
    b.  A coding copilot that opens tickets, edits PRs, and runs tests via tools.</li>
    c.  An enterprise chat assistant that reasons over policies and produces compliant outputs.
    """,

    # "gpt-o3":"High-accuracy reasoning (200K-token); $2.00/1M in, $8.00/1M out. Best for math, code gen, structured data outputs.",
    # "gpt-o4-mini":"Fast lean reasoning (200K-token); $1.10/1M in, $4.40/1M out. Ideal for vision+code when o3 is overkill.",
    # "gpt-o4-mini-high":"Enhanced mini-engine; $2.50/1M in (est.), $10.00/1M out (est.). Suited for interactive assistants with visual reasoning.",

    # Google
    "gemma-3n-e4b-it":"""Gemma is free.
      Best for:         Use case:  
      - Low latency   | - Visual and text processing 
      - Multilingual  | - Text translation
      - Summarization | - Summarizing text research content
    """,

    #2 Google
    "gemma-3n-e4b-it": """
        Open source for local hosting
    """,  

    "gemini-2.0-flash-lite":"""$0.075 In, $0.30 Out. CoD: Aug 2024"
      Best for:              Use case: 
      - Long Context       | - rocess 10,000 lines of code
      - Realtime streaming | - Call tools natively
      - Native tool use    | - Stream images and video in realtime
    """,

    "gemini-2.0-flash": """$0.10 In, $0.40 Out. CoD: Aug 2024
      Best for:                    Use case:
      - Multimodal understanding | - Process 10,000 lines of code
      - Realtime streaming       | - Call tools natively, like Search
      - Native tool use          | - Stream images & vids in R time  
    """,

    "gemini-2.5-flash-lite": "($0.10 In, $0.40 Out)/1M (est.) CoD: Jan 2025."
    "  Best for:                        Use case:"
    "  - Large scale processing         - Data transformation"
    "  - Low latency, high volume       - Translation"
    "      tasks with thinking          - Summarizationt",

    "gemini-2.5-flash": """$0.30. $2.50 Out CoD: Jan 2024.
      Best for:                           Use case:
      - Large scale processing            - Reason over complex problems
      - Low latency, high volume tasks    - Show thinking process
      - Agentic use cases                 - Call tools natively
    """,

    "gemini-2.5-pro": """$3.00 In /1M (est.). Advanced analytics, detailed reports & multi-step reasoning.
        Best for:
        - Coding
        - Reasoning
        - Multimodal understanding

        Use case:
        - Reason over complex problems
        - Tackle difficult code, math and STEM problems
        - Use the long context for analyzing large datasets, codebases or documents
    """,

    #3 XAI
    "grok-3-mini-fast": "$0.20/1M (est.). "
    "Ultra-low latency chat, real-time monitoring & streaming apps.",

    "grok-3-mini": "$0.40/1M (est.). Budget-friendly chat & assistant tasks with good accuracy.",

    "grok-3": "$1.00/1M (est.). General-purpose chat & content gen with balanced speed/quality.",

    #4 DeepSeek
    "deepseek-chat": "DeepSeek Chat; $1.20/1M (est.). Optimized for private-data Q&A, enterprise search & document ingestion.",

    #5 MoonShot
    "kimi-k2-0905-preview": """Mixture-of-Experts (MoE). Context length of 256k.
    Enhanced Agentic Coding abilities, improved frontend code aesthetics and practicality, and better context understanding.
    
    Pricing (per 1M tokens):
        Input: $0.15 
        Cache: $0.60
        Output: $2.50
    """,

    #6 Alibaba
    #i
    "qwen-flash": """ Qwen-Flash is a lightweight, high-speed large language model from Alibaba Cloud, optimized for efficiency and cost-effectiveness.

    Pricing (per 1M tokens):
        Input: $0.05 
        Output: $0.40

    Best for:
    > Simple, high-speed tasks requiring low latency.
    > Cost-sensitive applications where budget is a priority.
    > Scenarios demanding large context windows (supports up to 1M tokens).

    Use cases:
    > Real-time chat and dialogue systems needing quick responses.
    > Large-scale text processing (e.g., summarization, polishing).
    > Prototyping and development where rapid iteration is key.

    Note: Lacks advanced reasoning features like "deep thinking" mode found in higher-tier Qwen models (e.g., Qwen-Plus).
    """,

    #ii
    "qwen-plus": """LLM offering a balance of performance, speed, and cost. It features a 131,072 token context window and supports both thinking and non-thinking modes for enhanced reasoning.

    Pricing (per 1M tokens):
        Input: $0.40 
        Output: $1.20 

    Best for:
    > Moderately complex reasoning tasks due to its enhanced reasoning capabilities and thinking mode support 16.
    > Multilingual applications, with support for over 100 languages, including strong Chinese and English performance 12.
    > Cost-sensitive deployments requiring a balance of capability and affordability 13.

    Use cases:
    > Customer service automation (e.g., chatbots, virtual assistants) 26.
    > Content generation and summarization (e.g., marketing copy, document summarization) 236.
    > Code generation and tool-assisted tasks due to its agent capabilities and tool-calling support
    """,

    #iii
    "qwen3-Coder-Plus": """A commercial, high-performance coding model optimized for agentic tasks like tool use, browser interaction, and long-context code generation. 
       
        Pricing (per 1M tokens):
            Input $1 (0-32K tokens), $1.8 (32K-128K), $3 (128K-256K), $6 (256K-1M). 
            Output $5 (0-32K), $9 (32K-128K), $15 (128K-256K), $60 (256K-1M) 

        Best for:
        > Repository-scale coding (handles large codebases with long context).
        > Agentic workflows (tool calling, multi-step environment interactions).
        > Real-world software engineering (debugging, refactoring, SWE-bench tasks).

        Use cases:
        > Automating complex coding tasks (e.g., full-stack app generation, data storytelling).
        > Debugging and refactoring (identifying bugs, improving code quality).
        > Multi-turn coding with feedback (iterative problem-solving with execution).
        > Consider this model if you need long-context, agentic coding capabilities comparable to Claude Sonnet 17. Avoid if budget constraints outweigh performance needs.
    """,

    #iv
    "qwen-max": """Alibaba Cloud's flagship large-scale Mixture-of-Experts (MoE) model, pretrained on 20+ trillion tokens and refined with SFT/RLHF. Competes with top models like GPT-4o and Claude-3.5-Sonnet in benchmarks.
    
    Pricing (per 1M tokens): 
        Input: $1.60 - Output: $6.40

    Best for:
    > Complex, multi-step reasoning tasks 113
    > Multilingual applications (supports 100+ languages)
    > Coding and tool-calling precision 111

    Use cases:
    > Advanced coding assistance and debugging 310
    > High-quality content creation (e.g., documents, scripts)
    > Large-context analysis (32K token window) for documents or data

    """,

    "claude-opus-4-1":""" $15 / MTok	$18.75 / MTok	$30 / MTok	$1.50 / MTok	$75 / MTok
    """,

    "claude-sonnet-4-0":""" $3 / MTok	$3.75 / MTok	$6 / MTok	$0.30 / MTok	$15 / MTok
    """,

    "claude-haiku-3-5-latest":""" $0.80 / MTok	$1 / MTok	$1.6 / MTok	$0.08 / MTok	$4 / MTok   
    """,

    "claude-3-haiku-20240307":""" $0.25 / MTok	$0.30 / MTok	$0.50 / MTok	$0.03 / MTok	$1.25 / MTok
    """,

}


# -----------------------------------------------------------------------------
PURPOSE_TAGS = [
    "admin",
    "chat",
    "coding",
    "vision2text",
    "classification",
    "summarization",  
]

# -----------------------------------------------------------------------------
EMBEDDING_MODELS = {
    "openai": [
    "text-embedding-3-small",
    "text-embedding-3-large",
    ],
}


GPT_MODELS_LATEST = [
    "gpt-5.1",
    "gpt-5.1-chat-latest",
    "gpt-5.1-codex-mini",
    "gpt-5.1-codex",
    "gpt-5",
    "gpt-5-nano",
    "gpt-5-mini",         
]
