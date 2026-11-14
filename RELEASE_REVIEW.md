# Release review - v0.5 candidate

## Observed testing
- 15 automated evaluation-engine tests passed in the development environment.
- Manual local test: empty Response A produced no numerical score.
- Manual local test: export remained disabled without written reviewer evidence.

## Before public release
- Confirm the GitHub-hosted app matches the locally tested release.
- Run Streamlit and test complete evaluation/export after upload.
- Check mobile layout, keyboard navigation, accessibility and browser behaviour.
- Confirm no secrets, confidential materials or identifiable patient data are present.
- Review Streamlit Community Cloud data handling and deployment settings.
- Keep repository private until owner approves public release.

## Limitations
The rubric has not been validated, scores are subjective and the app does not fact-check responses. Passing unit tests is not proof of end-to-end security or accessibility. The software is an educational prototype.
