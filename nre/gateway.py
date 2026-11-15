"""L5 — Multimodel gateway and time-bound executioner."""

from __future__ import annotations

import json
import os
import urllib.request
from concurrent.futures import ThreadPoolExecutor, TimeoutError as FutureTimeout

from .text import fold


class ExecutionTimeout(RuntimeError):
    pass


class MockProvider:
    """Deterministic supplier without real model.

    Without `answers` returns an honest scoreboard ("no inference executed").With `answers` ({question: answer}) simulates a model that responds (correctly or incorrectly) for tests and benchmarks.
    """

    name = "mock"

    def __init__(self, answers: dict[str, str] | None = None):
        self.answers = {fold(k): v for k, v in (answers or {}).items()}

    def generate(self, instruction: dict, plan: dict) -> dict:
        key = fold(instruction["objective"])
        if key in self.answers:
            answer = self.answers[key]
            return {"provider": self.name, "facts": [answer], "inferences": [],
                    "unknowns": [], "proposed_solution": answer}
        return {
            "provider": self.name,
            "facts": [],
            "inferences": ["No model inference (mock supplier) was executed."],
            "unknowns": ["No external evidence available."],
            "proposed_solution": "Connect a model provider to process the target.",
        }


class OllamaProvider:
    name = "ollama"

    def __init__(self, model: str | None = None, endpoint: str | None = None):
        self.model = model or os.getenv("OMEGA_MODEL", "llama3.2")
        self.endpoint = endpoint or os.getenv("OLLAMA_ENDPOINT", "http://localhost:11434/api/chat")

    def generate(self, instruction: dict, plan: dict) -> dict:
        prompt = json.dumps({
            "objective": instruction["objective"],
            "constraints": instruction["constraints"],
            "execution_plan": plan,
            "output_requirements": {"facts": [], "inferences": [], "unknowns": [],
                                    "proposed_solution": ""},
        }, ensure_ascii=False)
        payload = json.dumps({
            "model": self.model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False, "format": "json", "options": {"temperature": 0.1},
        }).encode("utf-8")
        req = urllib.request.Request(self.endpoint, data=payload,
                                     headers={"Content-Type": "application/json"}, method="POST")
        with urllib.request.urlopen(req, timeout=120) as resp:
            data = json.loads(resp.read())
        content = json.loads(data["message"]["content"])
        return {"provider": self.name, "model": self.model, **content}


class ModelGateway:

    def __init__(self, provider=None):
        if provider is None:
            provider = os.getenv("OMEGA_PROVIDER", "mock")
        if isinstance(provider, str):
            if provider == "mock":
                provider = MockProvider()
            elif provider == "ollama":
                provider = OllamaProvider()
            else:
                raise ValueError("UNSUPPORTED_PROVIDER")
        self.provider = provider

    def generate(self, instruction: dict, plan: dict) -> dict:
        return self.provider.generate(instruction, plan)


class Executor:
    """Run the gateway with time limit. A timeout translates to HALT."""

    def __init__(self, gateway: ModelGateway | None = None, timeout_s: float = 120.0):
        self.gateway = gateway or ModelGateway()
        self.timeout_s = timeout_s

    def run(self, instruction: dict, plan: dict) -> dict:
        pool = ThreadPoolExecutor(max_workers=1)
        future = pool.submit(self.gateway.generate, instruction, plan)
        try:
            return future.result(timeout=self.timeout_s)
        except FutureTimeout as exc:
            raise ExecutionTimeout(f"EXECUTION_TIMEOUT after {self.timeout_s}s") from exc
        finally:
            pool.shutdown(wait=False, cancel_futures=True)
