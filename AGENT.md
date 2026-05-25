# AGENT.md

## 1. Project overview

This repository is a Vietnamese Docusaurus curriculum and runnable Python lab for simultaneous text-to-text translation. It teaches the problem as a streaming decision system layered on top of sequence generation.

The goal is to help learners understand the latency-quality tradeoff, READ/WRITE control, latency metrics, policy design, and a compact PyTorch implementation that can be inspected end to end.

## 2. Repository map

- `docs/`: public Vietnamese curriculum chapters.
- `docs/resources/`: public syllabus, glossary, checklists, and learning resources.
- `src/pages/`: Docusaurus homepage.
- `src/css/`: Docusaurus styling.
- `src/simulst_edu/`: Python package for toy simultaneous translation experiments.
- `examples/`: runnable teaching demos.
- `tests/`: Python tests for metrics and policies.
- `scripts/`: local QA scripts.
- `.github/workflows/`: GitHub Pages deployment workflow.

## 3. Curriculum-wide content standard

Public content must be educational, neutral, technically rigorous, and written for learners. Do not expose private task instructions, local absolute paths, credentials, internal notes, or agent coordination details in public docs.

A chapter should teach by building intuition before formal definitions. It should make the reader understand why the concept exists and how it appears in code.

Use `Phần` for course sections. Do not use em dash characters. Use commas, colons, semicolons, or parentheses instead.

## 4. Pedagogical writing style

Write like a strong Vietnamese university lecturer: precise, patient, natural, serious, and practical. The prose must not sound like a slide dump, marketing copy, literal translation, or terse developer note.

For each important concept, prefer this flow:

1. Start from a concrete tension or question.
2. Build intuition with a small example.
3. Formalize with notation or terminology.
4. Map the idea to the Python implementation.
5. Explain common failure modes.
6. End with what the learner should retain.

## 5. Math, diagrams, and examples

Math is welcome, but every symbol must be explained in words. Equations should compress an idea after intuition has been built.

Examples should stay close to the repository:

- source prefixes and target commitments
- READ and WRITE traces
- wait-k and adaptive policies
- Average Proportion and Average Lagging
- synthetic reorderings
- model confidence versus hypothesis stability
- streaming systems constraints

## 6. Source material and attribution policy

Use external materials only to understand standard concepts. Public chapters must be original Vietnamese teaching material. Do not copy paragraphs from papers, docs, tutorials, or benchmark pages.

Standard terminology, formulas, and algorithm names can be used when they are part of the field.

## 7. Public privacy and safety constraints

Public docs must not mention:

- private user instructions
- hidden constraints
- local absolute paths
- credentials, tokens, secrets, API keys, or private URLs
- agent memory contents
- internal planning files

Privacy controls must remain intact unless the user explicitly asks to change them:

- `static/robots.txt` must disallow all crawling.
- Docusaurus must include `noindex,nofollow,noarchive,nosnippet` metadata.
- Sitemap generation must stay disabled.

Do not rewrite git history, delete the Python lab, mutate dependencies, or change privacy posture unless the user explicitly asks.

## 8. Commands and verification

Use these commands before reporting completion:

- `npm run qa:docs`: run documentation QA.
- `npm run typecheck`: run TypeScript typecheck.
- `npm run build`: build Docusaurus site.
- `npm run verify`: run docs QA, typecheck, and build.
- `pytest`: run Python tests after Python dependencies are installed.

GitHub Pages deploy runs from `.github/workflows/deploy.yml` and uses `npm run verify` before upload.

## 9. Completion checklist

Before reporting completion, verify the relevant items:

- `npm run verify` passes.
- Python tests pass if Python code changed.
- No em dash characters appear in public or source text.
- Public docs do not contain local absolute paths.
- Sidebar doc IDs exist.
- Absolute `/docs/...` links do not point to missing docs.
- The site deploy workflow succeeds after push.
- Important live URLs return HTTP 200 with noindex metadata.
- `/sitemap.xml` remains 404 if privacy controls are expected.

## 10. Repo specialization: Simultaneous Translation Edu

The central learning promise is this: simultaneous translation is not only about predicting the right target sentence, it is about deciding when the system has enough source evidence to safely commit each target token.

Always separate three layers:

- the model predicts plausible target tokens from a source prefix;
- the policy decides when a token is stable enough to emit;
- the evaluator measures both quality and latency.

Important misconceptions to prevent:

- A better offline model does not remove the need for a timing policy.
- Low latency is not automatically better if early tokens become wrong.
- High local probability is not the same as sequence-level stability.
- Average metrics can hide bursty user experience.
- The toy dataset is a teaching environment, not a claim of benchmark performance.

## 11. Maintenance notes for future agents

Keep this file as the operational guide for future agents. Update it when commands, directory structure, deploy posture, QA rules, or course scope change.

Do not use this file as a task log. Use git history for history and issue or plan files for task-specific work.
