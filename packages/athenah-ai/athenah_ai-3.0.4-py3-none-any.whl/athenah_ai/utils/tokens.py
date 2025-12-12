#!/usr/bin/env python
# coding: utf-8

import os
import openai

OPENAI_API_KEY: str = os.environ.get("OPENAI_API_KEY")
openai.api_key = OPENAI_API_KEY
OPENAI_API_MODEL: str = "gpt-4o"


def get_token_total(prompt: str) -> int:
    import tiktoken

    openai_model = OPENAI_API_MODEL
    encoding = tiktoken.encoding_for_model(openai_model)
    # print(
    #     "\033[37m" + str(len(encoding.encode(prompt))) + " tokens\033[0m" + " in prompt"
    # )
    return len(encoding.encode(prompt))
