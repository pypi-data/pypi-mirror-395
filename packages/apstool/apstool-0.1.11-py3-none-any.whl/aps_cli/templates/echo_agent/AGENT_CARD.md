---
card_version: 0.1
id: dev.rag
name: Local RAG (TF-IDF)
version: 0.0.1
publisher:
  name: Veda Hegde
  url: https://github.com/vedahegde60/agent-packaging-standard
links:
  repo: https://github.com/vedahegde60/agent-packaging-standard
  docs: ./README.md
tags: [rag, local, tfidf, python, offline]
license: Apache-2.0
compliance:
  claims:
    - nist_ai_rmf: "profile: low-risk, controls: GOV-1, MAP-1"
    - iso_42001: "process: in-progress"
    - eu_ai_act: "category: minimal/no-risk (informational)"
  evidence:
    - threat_model: ./SECURITY.md
    - data_privacy: "no external network; local files only"
safety:
  known_limitations:
    - "Not suitable for sensitive data without review."
    - "No semantic embeddings; TF-IDF quality varies."
monetization:
  model: free
runtime:
  language: "Python 3.11"
  platform: "Posix/Windows"
  network: "none"
---

# Agent Card — Local RAG (TF-IDF)

## Summary
A minimal retrieval-augmented QA agent that searches local `.txt` files with TF-IDF and returns the best match.

## Use Cases
- Quick Q&A over a small docs folder
- Demonstrate APS packaging contract without ML stacks
- Air-gapped demos

## Inputs
```json
{ "query": "string", "top_k": 1 }

