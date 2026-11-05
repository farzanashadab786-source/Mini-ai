
# TinyLocalAI

A small offline chatbot designed to run with very little memory (including many 2 GB RAM devices).

## What it does
- Runs locally in Python.
- Needs no internet connection.
- Uses only Python's standard library.
- Finds the closest matching stored question using TF-IDF-style similarity.
- Lets you teach it new question-and-answer pairs.
- Saves what you teach in `knowledge.json`.

## What it is not
This is **not** ChatGPT, a trained large language model, or a neural network.
It does not independently understand or reason about arbitrary questions. It retrieves the answer attached to the closest matching question. Its small memory use comes with that limitation.

## Run

Requires Python 3.8 or newer. No `pip install` is needed.

```bash
python main.py
```

On Android, open the extracted folder in Pydroid 3 and run `main.py`.

## Commands
- `/teach` — add a question and answer
- `/list` — show saved knowledge
- `/forget` — remove the closest matching question
- `/help` — show help
- `/quit` — exit

Your learned knowledge is saved in `knowledge.json` in this folder. Back up that file if you want to keep your teaching.

## Improve it
Add more entries to `data/starter_knowledge.json`, or teach it from the chat. Keep answers factual and concise.
