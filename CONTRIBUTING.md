# Contributing

This repository is in private preview. Propose changes through a branch and pull request; do not publish or mirror the collection without an explicit release decision.

## Make a change

1. Read [AUTHORING.md](AUTHORING.md).
2. Change the smallest relevant skill and its tests.
3. Add or update an eval case that would have caught the issue.
4. Run:

   ```sh
   python3 scripts/validate_repository.py
   python3 -m unittest discover -s tests -v
   ```

5. In the pull request, distinguish deterministic test results from unperformed live-agent evaluation.

Do not add a dependency unless the standard library cannot express the required check and the provenance, maintenance and security cost is justified.

