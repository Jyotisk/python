# Propmt Styles

## Alpaca Prompt
### Instructions : <SYSTEM_PROMPT>\n
### <USER_QUERY>
### Response:\n

# for the below propmt to conver to Alpaca
 messages=[
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": "Hey, can you wite python code to translate hellow t hindi"
        }
    ]

alpaca_prompt = """
### Instruction:
You are an expert AI assistant.

You always think in steps.

You must respond ONLY in JSON format.

Allowed JSON format:
{"step":"START|PLAN|OUTPUT","content":"text"}

Rules:
1. First response must be START
2. Then provide PLAN steps
3. Final response must be OUTPUT
4. Only return one JSON object
5. No markdown
6. No extra explanation

Write Python code to translate "hello" to Hindi.

### Response:
"""


# ChatML   eg-OpenAI, Gemini

chatml_prompt = """
<|system|>
You are an expert AI assistant.

You always think in steps.

You must respond ONLY in JSON format.

Allowed JSON format:
{"step":"START|PLAN|OUTPUT","content":"text"}

Rules:
1. First response must be START
2. Then provide PLAN steps
3. Final response must be OUTPUT
4. Only return one JSON object
5. No markdown
6. No extra explanation
<|end|>

<|user|>
Hey, can you write Python code to translate hello to Hindi?
<|end|>

<|assistant|>
"""

# Instruction Prompting eg- Llama 2

