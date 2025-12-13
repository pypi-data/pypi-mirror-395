from __future__ import annotations
from dataclasses import dataclass
from typing import Optional, Dict, Any


@dataclass
class SkillVector:
    memory: Optional[float] = None
    reasoning: Optional[float] = None
    numerical: Optional[float] = None
    language: Optional[float] = None

    def is_auto(self) -> bool:
        """True if user left all skills unspecified."""
        return all(
            v is None for v in
            (self.memory, self.reasoning, self.numerical, self.language)
        )

    def to_prompt_fragment(self) -> str:
        """Human-readable description passed to LLM."""
        if self.is_auto():
            return (
                "Skill profile: auto (you choose appropriate memory, reasoning, "
                "numerical, and language load based on the rubric and target difficulty)."
            )

        def fmt(name: str, v: Optional[float]) -> str:
            return f"{name}={v:.2f}" if v is not None else f"{name}=auto"

        return (
            "Skill profile: "
            + ", ".join([
                fmt("memory", self.memory),
                fmt("reasoning", self.reasoning),
                fmt("numerical", self.numerical),
                fmt("language", self.language),
            ])
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "memory": self.memory,
            "reasoning": self.reasoning,
            "numerical": self.numerical,
            "language": self.language,
        }

