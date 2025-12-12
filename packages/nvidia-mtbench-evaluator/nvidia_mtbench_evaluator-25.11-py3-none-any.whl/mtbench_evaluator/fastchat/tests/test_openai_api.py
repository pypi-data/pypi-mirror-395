"""
Test the OpenAI compatible server

Launch:
python3 launch_openai_api_test_server.py
"""

import openai
from openai import OpenAI

client = OpenAI(api_key="EMPTY", base_url="http://localhost:8000/v1")

from fastchat.utils import run_cmd

def test_list_models():
    model_list = client.models.list()
    names = [x["id"] for x in model_list.data]
    return names


def test_completion(model, logprob):
    prompt = "Once upon a time"
    completion = client.completions.create(model=model,
    prompt=prompt,
    logprobs=logprob,
    max_tokens=64,
    temperature=0)
    print(f"full text: {prompt + completion.choices[0].text}", flush=True)
    if completion.choices[0].logprobs is not None:
        print(
            f"logprobs: {completion.choices[0].logprobs.token_logprobs[:10]}",
            flush=True,
        )


def test_completion_stream(model):
    prompt = "Once upon a time"
    res = client.completions.create(model=model,
    prompt=prompt,
    max_tokens=64,
    stream=True,
    temperature=0)
    print(prompt, end="")
    for chunk in res:
        content = chunk.choices[0].text
        print(content, end="", flush=True)
    print()


def test_embedding(model):
    embedding = client.embeddings.create(model=model, input="Hello world!")
    print(f"embedding len: {len(embedding.data[0].embedding)}")
    print(f"embedding value[:5]: {embedding.data[0].embedding[:5]}")


def test_chat_completion(model):
    completion = client.chat.completions.create(model=model,
    messages=[{"role": "user", "content": "Hello! What is your name?"}],
    temperature=0)
    print(completion.choices[0].message.content)


def test_chat_completion_stream(model):
    messages = [{"role": "user", "content": "Hello! What is your name?"}]
    res = client.chat.completions.create(model=model, messages=messages, stream=True, temperature=0)
    for chunk in res:
        content = chunk["choices"][0]["delta"].get("content", "")
        print(content, end="", flush=True)
    print()


def test_openai_curl():
    run_cmd("curl http://localhost:8000/v1/models")

    run_cmd(
        """
curl http://localhost:8000/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "vicuna-7b-v1.5",
    "messages": [{"role": "user", "content": "Hello! What is your name?"}]
  }'
"""
    )

    run_cmd(
        """
curl http://localhost:8000/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "vicuna-7b-v1.5",
    "prompt": "Once upon a time",
    "max_tokens": 41,
    "temperature": 0.5
  }'
"""
    )

    run_cmd(
        """
curl http://localhost:8000/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "vicuna-7b-v1.5",
    "input": "Hello world!"
  }'
"""
    )


if __name__ == "__main__":
    models = test_list_models()
    print(f"models: {models}")

    for model in models:
        print(f"===== Test {model} ======")

        if model in ["fastchat-t5-3b-v1.0"]:
            logprob = None
        else:
            logprob = 1

        test_completion(model, logprob)
        test_completion_stream(model)
        test_chat_completion(model)
        test_chat_completion_stream(model)
        try:
            test_embedding(model)
        except openai.APIError as e:
            print(f"Embedding error: {e}")

    print("===== Test curl =====")
    test_openai_curl()
