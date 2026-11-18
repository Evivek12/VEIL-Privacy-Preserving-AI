# VEIL Project – Starter Prototype

**VEIL** means *Verified, Intent-Preserving Delegation between Local and Remote Language Models*.

This folder contains a starter Streamlit application with:
- Query profiling (basic task classification and regex PII detection)
- Rule-based routing
- Prompt sanitization using placeholders
- Basic verification checks
- A placeholder final-answer module
- A small evaluation record shown in the app

## 1. Open in VS Code

1. Extract `VEIL_Project.zip`.
2. Open VS Code.
3. Select **File → Open Folder**.
4. Select the extracted `VEIL_Project` folder.

## 2. Create a virtual environment (Mac)

Open the VS Code terminal (**Terminal → New Terminal**) and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 3. Run the application

```bash
streamlit run app.py
```

Streamlit should open the app in your browser. If it does not, open the local URL printed in the terminal (usually http://localhost:8501).

## 4. Try this sample

```text
My name is Alex Kumar and my phone number is 9876543210.
Please draft an internship application email.
```

Try a second query:

```text
Rewrite this sentence in simple English: The system demonstrates privacy-preserving delegation.
```

## 5. Important limitations

This is a **starter prototype**, not the completed VEIL research system:
- Name detection is a simple heuristic and will miss many names or produce false positives.
- Regex detection does not detect every type of PII.
- The intent check is a basic heuristic, not a semantic language-model judge.
- The router uses simple rules, not a trained classifier.
- No local or remote LLM is connected yet.
- No PUPA dataset is included. Obtain it from the official PAPILLON project, check its licence and release notes, and place only permitted data in `dataset/`.
- Do not enter real personal or confidential information during testing.

Do not report the demo's PASS labels as validated privacy guarantees or research results. Run experiments, record actual outputs, and document limitations before making research claims.

## 6. Suggested next development steps

1. Improve PII detection with a maintained recognizer such as Microsoft Presidio and spaCy.
2. Add a local model through Ollama for prompt creation, intent checking and local fallback.
3. Add a remote model adapter; send only prompts that pass the gate, after reviewing the provider's data policy.
4. Implement dataset loading and the evaluation metrics described in the research report.
5. Compare local-only, redaction, direct-remote, PAPILLON-style and VEIL configurations.
6. Save real experiment outputs to `results/` and create tables/graphs from those outputs.

## Project files

- `app.py`: Streamlit user interface and pipeline orchestration
- `profiler.py`: task classification and candidate PII detection
- `router.py`: local/delegation decision
- `prompt_creator.py`: replaces detected private spans
- `verifier.py`: checks detected-span leakage and basic prompt structure
- `aggregator.py`: placeholder final response
