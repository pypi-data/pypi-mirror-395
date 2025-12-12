PROMPT_TEMPLATE_MODEL_CARD = '''<extra_id_0>System
      {system message}
      <extra_id_1>User
      {turn 1 user message}
      <extra_id_1>Assistant
      <extra_id_2>
      {turn 1 assistant message}
      <extra_id_1>User
      {turn 2 user message}
      <extra_id_1>Assistant
      <extra_id_2>
      {turn 2 assistant message}
      <extra_id_1>'''


# Translation of PROMPT_TEMPLATE_MODEL_CARD to jinja
# Change it for testing
CHAT_TEMPLATE = '''<extra_id_0>System
{% if messages[0].role == 'system' %}
{% set loop_messages = messages[1:] %}
{{ messages[0].content }}
{% else %}
{% set loop_messages = messages %}
{% endif %}
{% for message in loop_messages %}
{% if message.role == 'user' %}
<extra_id_1>User
{% else %}
<extra_id_2>Assistant
{% endif %}
{{ message.content }}
{% endfor %}
{% if messages[-1].role == 'user' and add_generation_prompt %}
<extra_id_2>Assistant
{% endif %}'''


MESSAGES = [
    {
        "role": "system",
        "content": "Be a helpful assistant."
    },
    {
        "role": "user",
        "content": "What is the capital of GB?"
    },
    {
        "role": "assistant",
        "content": "London"
    },
    {
        "role": "user",
        "content": "What about Spain?"
    }
]


if __name__ == "__main__":
    import json
    from pathlib import Path
    from transformers import LlamaTokenizerFast

    tokenizer = LlamaTokenizerFast.from_pretrained(
        Path(__file__).parent.parent / "models" / "llama_tokenizer"
    )
    # overwrite chat template
    tokenizer.chat_template = CHAT_TEMPLATE

    print("Messages:")
    print(json.dumps(MESSAGES, indent=4))
    print("\n" * 3)
    print("Prompt:")
    prompt = tokenizer.apply_chat_template(MESSAGES, tokenize=False, add_generation_prompt=True)
    print(prompt)
