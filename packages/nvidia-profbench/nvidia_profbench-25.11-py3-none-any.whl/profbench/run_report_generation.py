# SPDX-FileCopyrightText: Copyright (c) 2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: MIT
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.

import os
import copy
import base64
import argparse
import random

from datasets import load_dataset
from huggingface_hub import snapshot_download

from profbench.utils import parallel_launcher, instantiate_client

try:
    from google.genai.types import GenerateContentConfig, Tool, GoogleSearch, ThinkingConfig
except:
    print("Google GenAI failed to import; ignore if not using otherwise please pip install google-genai")

def load_hf_data():
    dataset = load_dataset("nvidia/ProfBench")["test"]
    snapshot_download(repo_id="nvidia/ProfBench",local_dir=".",repo_type="dataset", allow_patterns="documents/*")

    processed_data = []
    for dp in dataset:
        domain = dp["domain"]
        task_id = dp["task_id"]
        prompt = dp["prompt"]
        filepaths = dp["filepaths"] if "filepaths" in dp else []
        processed_data.append({"task_id": task_id, "domain":domain, "prompt": prompt, "filepaths": filepaths, "rubrics": dp["rubrics"]})
    return processed_data

def filter_data(prompt_data, version, limit_samples=None):
    if version == "debug":
        prompt_data = prompt_data[:1]
    elif version == "full":
        prompt_data = prompt_data * 16
    elif version == "lite":
        task_id_to_samples = {'Chem-0': 4, 'Chem-1': 4, 'Fin-0': 4, 'Fin-1': 4, 'Cons-0': 4, 'Fin-2': 4, 'Phys-0': 4, 'Phys-1': 4, 'Phys-2': 4, 'Fin-3': 4, 'Chem-2': 4, 'Chem-3': 5, 'Chem-4': 3, 'Phys-3': 4, 'Cons-1': 3, 'Phys-4': 4, 'Fin-4': 4, 'Cons-2': 3, 'Fin-5': 4, 'Cons-3': 4, 'Chem-5': 4, 'Fin-6': 4, 'Chem-6': 5, 'Chem-7': 4, 'Chem-8': 4, 'Phys-5': 4, 'Cons-4': 4, 'Phys-6': 4, 'Chem-9': 5, 'Phys-7': 4, 'Fin-7': 4, 'Cons-5': 3, 'Phys-8': 3, 'Cons-6': 4, 'Fin-8': 5, 'Fin-9': 5, 'Cons-7': 3, 'Cons-8': 4, 'Cons-9': 5, 'Phys-9': 4}
        new_data = []
        for dp in prompt_data:
            task_id = dp["task_id"]
            n_samples = task_id_to_samples[task_id]
            for i in range(n_samples):
                new_data.append(copy.deepcopy(dp))
        # shuffling to increase the likelihood of cache hit of common prefix rather than concurrent processing
        random.shuffle(new_data)
        prompt_data = new_data
    
    # Apply limit_samples if specified
    if limit_samples is not None and limit_samples > 0:
        prompt_data = prompt_data[:limit_samples]
    
    print("total samples:", len(prompt_data))
    return prompt_data

def get_openai_existing_filename_to_file_id(client):
    existing_file_list = client.files.list()
    existing_filename_to_file_id = {file_obj.filename: file_obj.id for file_obj in existing_file_list.data}
    return existing_filename_to_file_id

def get_openai_response(prompt, client=None, model=None, filepaths=None, reasoning=False, web_search=False, temperature=None, top_p=None, max_tokens=None):
    # Use provided values or defaults based on reasoning
    if temperature is None:
        temperature = 0.6 if reasoning else 0
    if top_p is None:
        top_p = 0.95 if reasoning else 0
    if max_tokens is None:
        max_tokens = 64000 if reasoning else 32000
    
    # Note: Web search is not supported in standard OpenAI API
    # This feature would require custom API endpoints
    if web_search:
        raise NotImplementedError("Web search is not supported with standard OpenAI chat completions API. Use Google API or a custom endpoint.")
    
    # Standard OpenAI chat completion format
    messages = [{"role": "user", "content": prompt}]

    request_params = {
        "model": model,
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "stream": False
    }
    
    # Add reasoning_effort if reasoning is a string (for o1/o3 models)
    if isinstance(reasoning, str) and ('o1' in model.lower() or 'o3' in model.lower()):
        request_params["reasoning_effort"] = reasoning

    completion = client.chat.completions.create(**request_params)
    
    # Handle cases where response might be None or missing expected fields
    if not completion or not completion.choices:
        raise ValueError("API returned empty response")
    
    content = completion.choices[0].message.content
    if content is None:
        raise ValueError("API returned None content")
    
    # Get token usage, default to 0 if not available
    prompt_tokens = completion.usage.prompt_tokens if completion.usage else 0
    completion_tokens = completion.usage.completion_tokens if completion.usage else 0
    
    return content, prompt_tokens, completion_tokens

def get_google_response(prompt, filepaths=None, client=None, model=None, reasoning=False, web_search=False, temperature=None, top_p=None, max_tokens=None):
    contents = prompt

    if web_search:
        tools = [Tool(google_search=GoogleSearch())]
    else:
        tools = []
    
    max_tokens = 64000 if reasoning else 32000

    if not reasoning:
        thinking_budget = 0
    elif reasoning == "low":
        thinking_budget = int(0.2*max_tokens)
    elif reasoning == "medium":
        thinking_budget = int(0.5*max_tokens)
    elif thinking_budget == "high":
        thinking_budget = int(0.8*max_tokens)

    response = client.models.generate_content(model=model, contents=contents, config=GenerateContentConfig(tools=tools, thinking_config=ThinkingConfig(thinking_budget=thinking_budget)))
    
    thinking_tokens = response.usage_metadata.thoughts_token_count if response.usage_metadata.thoughts_token_count is not None else 0
    output_tokens = thinking_tokens + response.usage_metadata.candidates_token_count
    return response.text, response.usage_metadata.prompt_token_count, output_tokens

def encode_pdf_to_base64(pdf_path):
    with open(pdf_path, "rb") as pdf_file:
        return base64.b64encode(pdf_file.read()).decode('utf-8')
            
def get_openrouter_response(prompt, client=None, model=None, filepaths=None, reasoning=False, web_search=False, temperature=None, top_p=None, max_tokens=None):
    prompt_content = [{ "type": "text", "text": prompt}]
    
    messages = [{"role": "user", "content": prompt_content}]

    # Use provided values or defaults based on reasoning
    if temperature is None:
        temperature = 0.6 if reasoning else 0
    if top_p is None:
        top_p = 0.95 if reasoning else 0
    if max_tokens is None:
        max_tokens = 64000 if reasoning else 32000

    request_obj = {
        "model": model+":online" if web_search else model, # this uses Exa AI plugin
        "messages": messages,
        "temperature": temperature,
        "top_p": top_p,
        "max_tokens": max_tokens,
        "stream": False
    }

    if isinstance(reasoning, str):
        request_obj["reasoning_effort"] = reasoning

    completion = client.chat.completions.create(**request_obj)
    return completion.choices[0].message.content, completion.usage.prompt_tokens, completion.usage.completion_tokens

def get_model_response(dp, idx, inference_hyperparameters, client, model):
    library = inference_hyperparameters["library"]

    if library == "openrouter":
        func = get_openrouter_response
    elif library == "openai":
        func = get_openai_response
    elif library == "google":
        func = get_google_response

    # Create a copy without 'library' key for passing to response functions
    params = {k: v for k, v in inference_hyperparameters.items() if k != "library"}

    response, prompt_tokens, completion_tokens = func(dp["prompt"], filepaths=dp["filepaths"], client=client, model=model, **params)
    
    dp["idx"] = idx
    dp["response"] = response
    dp["prompt_tokens"] = prompt_tokens
    dp["completion_tokens"] = completion_tokens
    return dp

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="run llm judge on provided reports")

    parser.add_argument('-m', "--model", required=True)
    parser.add_argument('-ak', "--api-key", default=None, help="API key (if not provided, will use API_KEY env var). For google vertexai, this is the project ID.")
    parser.add_argument('-v', '--version', choices=["debug", "lite", "full"], default="lite")
    parser.add_argument('-l', '--library', choices=["openrouter", "openai", "google"], default="openrouter")
    parser.add_argument('-ws', '--web-search', action='store_true')
    parser.add_argument('-r', '--reasoning', action='store_true')
    parser.add_argument('-re', '--reasoning-effort', choices=["low", "medium", "high", "minimal"], default="high", help="this default to high because openrouter use this value to set budget_tokens for anthropic/gemini models")
    parser.add_argument('-p', "--parallel", type=int, default=32)
    parser.add_argument('-t', "--timeout", type=int, default=600)
    parser.add_argument('-ra', "--retry-attempts", type=int, default=3, help="retry attempts due to sproadic failures e.g. rate limiting or other issues")
    parser.add_argument('-f', "--folder", default="inference")
    parser.add_argument('-bu', "--base-url", default=None, help="custom base URL for API endpoint")
    parser.add_argument('-ls', "--limit-samples", type=int, default=None, help="limit the number of samples to process")
    parser.add_argument('-temp', "--temperature", type=float, default=None, help="temperature for sampling")
    parser.add_argument('-tp', "--top-p", type=float, default=None, help="top-p for sampling")
    parser.add_argument('-mt', "--max-tokens", type=int, default=None, help="max tokens for generation")
    args = parser.parse_args()

    # Get API key from args or environment variable
    api_key = args.api_key if args.api_key else os.environ.get("API_KEY")
    if not api_key:
        raise ValueError("API key must be provided via --api-key or API_KEY environment variable")

    model = args.model

    reasoning = args.reasoning if not args.reasoning else args.reasoning_effort
    web_search = int(args.web_search)

    os.makedirs(args.folder, exist_ok=True)
    clean_judge_name = model.replace("/", "_").replace(":", "-")
    output_filename = f"{args.folder}/{clean_judge_name}_reasoning_{reasoning}_search_{web_search}.jsonl"

    prompt_data = load_hf_data()
    prompt_data = filter_data(prompt_data, args.version, args.limit_samples)

    client = instantiate_client(args.library, api_key, args.timeout, args.base_url)

    inference_hyperparameters = {
        "reasoning": reasoning,
        "web_search": web_search,
        "library": args.library,
        "temperature": args.temperature,
        "top_p": args.top_p,
        "max_tokens": args.max_tokens
    }
    parallel_launcher(get_model_response, args.parallel, args.retry_attempts, prompt_data, output_filename, inference_hyperparameters, client, model)
