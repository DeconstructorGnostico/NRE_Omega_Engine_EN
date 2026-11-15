# About this English edition

- Original (Spanish): https://github.com/DeconstructorGnostico/Nre_omega_engine. It was not modified.
- Version: 2.0.0. Behavior is meant to match the Spanish version exactly.
- Tests: Spanish original pytest: 59 passed; English edition pytest: 59 passed.
- Checked for equivalence: same pass/fail on every test, plus identical demo and benchmark/evaluation results case by case where the project has them.

## Stays in Spanish (by design)

benchmark case texts and category labels (`benchmark.py`), Spanish keyword/lexicon lists inside the engine (the engine is bilingual by design).

These are inputs the system is evaluated on, or bilingual detection data. Translating them would change the published numbers.

## Not included

Nothing.

## Freeze hashes (English edition)

SHA-256 over the package's `*.py` files concatenated in alphabetical order:

- `nre/*.py`: `eec2d8ebfcb11e1f968dc574f30552ba012198617890410d52f9458718eb22ce`
