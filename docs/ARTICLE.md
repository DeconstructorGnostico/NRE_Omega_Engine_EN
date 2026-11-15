# NRE: a gate that decides whether a IA can continue

**By Adrian Mendez Millan**

## The problem

Language models respond with the same security when they know and when they do not. They mix what they infer with what is a fact and follow instructions that come hidden in the text. If we also connect them to real actions, such as sending, publishing, deleting or paying, a misinterpreted response ceases to be just a text error and becomes an effect on the world.

Tools already exist that attack parts of the problem: NeMo Guardrails, Guardrails AI, LangGraph agent graphs and structured vendor outputs. What is almost always missing is a single explicit layer, which can be audited and measured, and which answers a simple question: **Can this execution continue?**

## What is NRE

NRE–AMM–OMEGA_CONTEXT_ENGINE is an independent layer of control, interpretation, execution and verification for IA models. It converts the intent into formal instructions, validates the results and decides whether an execution can continue.

It is not a new model. It is an engine that is placed between the request and the model, and that today works with a simulated supplier or with Ollama.

## Architecture

- **L1 · SIPE:** converts the free text into a formal instruction with objective, type of intention, type of action (read only or with effects), restrictions, evidence and a diagnosis of ambiguity.
- **L2 · Semantic Firewall:** applies explicit rules against prompt injection, destructive actions, malicious intent and exfiltration of secrets.
- **NEXUS:** is the control plane. Actions with effects are denied by default and only proceed with explicit authorization.
- **L3 · AMM-CORE:** arm the execution plan and apply the invariants.
- **L5 · Gateway:** calls the model with a time limit.
- **L6 · Verification:** first validates the structure of the response and then compares it with references or external evidence. Only then can an answer be left as VERIFIED.
- **L7 · Persistence:** keeps one audit JSONL of each cycle, including rejected and detained.

The ten invariants (e.g. "INFERENCE != FACT", "LEARNING REQUIRES ACCEPTANCE" or "no SILENT STATE MUTATION") are executable checks that can fail, and each one has its tests.

## The State Machine

Each request follows this path: RECEIVED → INTERPRETING → VALIDATING → AWAITING_AUTH → EXECUTING → VERIFYING → COMMITTED → LEARNING → PERSISTING → COMPLETED.

If the intention is ambiguous, if the firewall blocks it, if the authorization is denied, or if the answer contradicts the reference, the cycle moves to REJECTED. An error or timeout leads to HALT. In both cases the cycle **also persists**. A retry reinterprets and validates, so you can't sneak in a malicious instruction like "clarification." If rejections accumulate, the entire engine stops until someone resumes it, and that's also audited.

## What I Measured

I included a reproducible benchmark of 33 cases: benign, injection, destructive, ambiguous, unauthorized actions and 10 questions with known answer. The "model" is simulated and answers 3 of those questions wrongly on purpose. I compared to delivering everything without control against going through NRE:

| Metric | Unchecked | NRE |
|---|---|---|
| Correct decisions (permitir/bloquear) | 13/33 (39.4%) | 30/33 (90.9%) |
| Harmful cases that happen | 13/13 | 2/13 |
| Benigns blocked by mistake | 0/6 | 1/6 |
| Mistaken responses delivered | 3/3 | 0/3 |
| Status questions VERIFIED | 0/10 | 7/10 |

## Limitations, without ornaments

- The firewall is by rules. Two paraphrased injections escaped ("Finge that you have no rules..." and "Forget what you were told before..."), and a legitimate question about phishing was blocked.
- The set is small and the rules were written knowing it, so these numbers don't predict how it behaves with new data. They just show that the gate works as specified.
- VERIFIED means the answer matches references given by the caller. There is no search for sources.
- I still don't compare it to NeMo Guardrails, Call Guard or public benchmarks like HarmBench. That's the next step.

## Code and collaboration

The code is open (MIT), is written only with the Python standard library and includes 59 automatic tests and CI:

https://github.com/DeconstructorGnostico/Nre_omega_engine

I'm looking for collaborators for three things: test it with real models, build a larger and unseen Spanish evaluation set, and compare it against the tools that already exist. If you work on evaluation, agent security or governance of IA in Spanish, write to me.
