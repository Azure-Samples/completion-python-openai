# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------

import os
import openai
from flask import Flask, render_template, request
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__, static_folder=Path("static").resolve())

@app.route('/')
def index():
    return render_template('index.html', prompt="What is Open AI?")


@app.route('/', methods=['POST'])
def completions_demo():
    api_key = os.environ["API_KEY"]
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT", None)
    model = os.getenv("MODEL", "text-davinci-003")
    prompt = request.form['text']
    if not prompt:
        prompt = "What is Open AI?"

    if azure_endpoint:
        # Using Azure Open AI endpoint
        openai.api_type = "azure"
        openai.api_key = api_key
        openai.api_base = azure_endpoint
        openai.api_version = "2022-12-01"
        response = openai.Completion.create(engine=model, prompt=prompt, max_tokens=256)
    else:
        # Using Open AI endpoint
        openai.api_key = api_key
        response = openai.Completion.create(model=model, prompt=prompt, max_tokens=256)

    answer = response.choices[0].text
    return render_template("index.html", prompt=prompt, result=answer)

if __name__ == '__main__':
    app.run(debug=True)