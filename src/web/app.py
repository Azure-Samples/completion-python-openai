# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import os
import openai
from flask import Flask, render_template, request
from pathlib import Path
from dotenv import load_dotenv
from azure.identity import DefaultAzureCredential

default_credential = DefaultAzureCredential()
token = default_credential.get_token("https://cognitiveservices.azure.com/.default")

load_dotenv()

app = Flask(__name__, static_folder=Path("static").resolve())


@app.route("/")
def index():
    return render_template("index.html", prompt="What is Open AI?")


@app.route("/", methods=["POST"])
def completions_demo():
    model = os.getenv("AZURE_OPENAI_MODEL", "text-davinci-003")
    prompt = request.form["text"]
    if not prompt:
        prompt = "What is Open AI?"

    openai.api_type = "azure_ad"
    openai.api_key = token.token
    openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT", None)
    openai.api_version = "2022-12-01"
    response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=256)

    answer = response.choices[0].text
    return render_template("index.html", prompt=prompt, result=answer)


if __name__ == "__main__":
    app.run(debug=True)
