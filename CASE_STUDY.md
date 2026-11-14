# Verity | Product case study

**Project:** Verity - human-led AI response evaluation  
**Stage:** Deployed educational prototype, November 2026  
**Live demo:** https://verity-ai-evaluation.streamlit.app

## Why I built it

AI-generated answers can sound convincing even when they contain errors, omit important context or express more certainty than the evidence supports. I wanted to explore a practical product question: how can a reviewer compare two answers consistently, explain their judgement and retain a record of the evaluation?

Verity is a small, working prototype built to explore that question. It is general-purpose, with synthetic healthcare-related examples reflecting my interests in responsible AI and clinical safety. It does not diagnose, fact-check independently or certify a response as safe.

## Product decisions

I scoped the first version around a single workflow: enter a question and reference material, compare two answers, assign ratings, record the reasons and export the evaluation.

The reviewer rates five dimensions: factual accuracy (30%), safety (25%), completeness (20%), ease of understanding (15%) and handling of uncertainty (10%). These weights are configurable, but must total 100%. The weights, 4/5 threshold and rating anchors are initial design choices, not a validated assessment instrument.

A simple weighted average could conceal a serious weakness. I therefore included explicit overrides: accuracy or safety rated 2 or below, or a reviewer-flagged critical failure, blocks a 'meets rubric threshold' decision regardless of the overall score. The interface says 'not independently verified' because the result depends on human-assigned ratings and reference material.

I also chose to make the evidence record conditional on completion: both answers, the question, reference material and written rationales are required before JSON export. An empty answer receives no numerical score.

## What I built

- A Streamlit interface for side-by-side response comparison
- A deterministic scoring engine with standard or custom rubric weights
- Safety, accuracy and critical-failure overrides
- Synthetic demonstration examples
- Reviewer rationale fields and a downloadable structured JSON record
- Automated scoring-rule tests and manual acceptance checks

There is no LLM API, user account system or database. Reviewers should use synthetic or public content only; the public hosting service processes information entered into the app.

## Testing and evidence

I deployed Verity to Streamlit Community Cloud and manually tested the live workflow in November 2026. The app loaded a synthetic diagnosis-related question and both candidate answers. Human-entered scores produced the expected review-required decision when safety and factual accuracy were rated 2 or lower. The app displayed the blocking reasons, permitted a completed evaluation record to be downloaded, removed the numerical score when an answer was emptied, and disabled export when a written rationale was removed.

These are functional acceptance observations, not a formal usability study, a security audit, clinical validation or evidence of inter-rater reliability. The exported JSON was downloaded successfully; its full contents have not yet been independently checked against the input fields.

## My role and AI-assisted development

I directed the product scope, rubric and safeguard requirements, made decisions about the interface and evidence needed, reviewed ambiguous behaviour, and performed hands-on acceptance testing of the deployed application. ChatGPT supported implementation by generating and revising code, tests and documentation. I am developing product and technical fluency through the process, and I do not present this as independently hand-coded software engineering work.

## What I learnt and what comes next

A product can calculate a score correctly while still inviting an unsafe interpretation of that score. Wording, reviewer accountability and override rules therefore matter as much as the arithmetic. Building and testing Verity also highlighted the difference between a working demonstration and a validated evaluation method.

The next priorities would be observing independent first-time users, checking agreement between reviewers, testing accessibility with assistive technology, examining whether the rating anchors are interpreted consistently, and investigating whether the chosen weights and thresholds are appropriate for different contexts. Until then, Verity remains a learning and portfolio prototype.
