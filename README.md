# Verity

**How good is that AI answer?**

**[Try the live demo](https://verity-ai-evaluation.streamlit.app)** · **[Read the product case study](CASE_STUDY.md)**

Verity is a general-purpose, human-led Streamlit application for comparing two AI-generated responses against five quality criteria. It is an educational portfolio prototype, **not an automated fact-checker or clinically validated tool**.

## What it does
- Compare two responses to the same question
- Score factual accuracy (30%), completeness (20%), ease of understanding (15%), safety (25%), and appropriate handling of uncertainty (10%)
- Use standard weights or customise them (total must equal 100%)
- Block threshold approval when accuracy or safety is rated 2 or below, or a reviewer flags a critical failure
- Require a written rationale and reference material before exporting a completed JSON record
- Show no score for an empty response

A score of at least 4/5 with no blocking flags **meets the rubric threshold**; it does not establish factual correctness or independent validation. Weights and thresholds are design assumptions, not a validated assessment instrument.

## Run locally
Install Python 3.11+ and run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py --server.address 127.0.0.1
```

Open http://127.0.0.1:8501.

## Run tests
```bash
python -m pytest -q
```

## Privacy and limitations
Use synthetic or public information only. Do not submit personal, confidential or patient-identifiable data. Verity has no LLM API integration, database or user authentication. Public hosting will process user inputs on the hosting provider's infrastructure. The user supplies all ratings and reference material, which Verity does not independently verify. Ratings may vary between reviewers. The tool is not suitable for clinical decision-making.

## Development and authorship
Product scope, rubric customisation, usability observations, review of scoring ambiguity and manual acceptance testing were directed by the project owner. ChatGPT generated and revised implementation code and supported testing. The portfolio case study should distinguish human product decisions from AI-assisted implementation.

## Project files
- `app.py`: Streamlit UI
- `evaluation.py`: deterministic scoring and decision rules
- `data/examples.json`: synthetic demonstration cases
- `tests/test_evaluation.py`: automated tests
- `PRODUCT_BRIEF.md`: scope and success measures
- `RELEASE_REVIEW.md`: release checks and remaining limitations
