from __future__ import annotations

import re
from pathlib import Path

from llm_guard.util import get_logger

from .base import Scanner

LOGGER = get_logger()

_SEVERITY_SCORES: dict[str, float] = {
    "high": 1.0,
    "medium": 0.7,
    "low": 0.5,
}

# Built-in Agent Threat Rules covering 5 attack categories.
_BUILT_IN_RULES: list[dict] = [
    # --- Agent Manipulation: system prompt / role override attacks ---
    {
        "id": "ATR-AM-001",
        "name": "Override System Instructions",
        "category": "agent-manipulation",
        "severity": "high",
        "patterns": [
            r"(?i)\b(ignore|disregard|forget|override)\b.{0,40}\b(instructions|guidelines|rules|constraints|prompt)\b",
            r"(?i)\b(previous|prior|above|original|initial)\s+(instructions?|guidelines?|rules?|prompts?)\s+(are|were|is|was)\s+(wrong|invalid|false|outdated|no longer)",
        ],
    },
    {
        "id": "ATR-AM-002",
        "name": "Jailbreak Mode Activation",
        "category": "agent-manipulation",
        "severity": "high",
        "patterns": [
            r"(?i)\b(jailbreak|DAN|unrestricted|no.?filter|god.?mode)\b.{0,30}\b(mode|version|persona|form)\b",
            r"(?i)you are now (an? )?(unrestricted|jailbroken|uncensored|unfiltered)",
            r"(?i)enter\s+.{0,20}(developer|debug|maintenance|admin)\s+mode",
        ],
    },
    {
        "id": "ATR-AM-003",
        "name": "Persona Hijacking",
        "category": "agent-manipulation",
        "severity": "medium",
        "patterns": [
            r"(?i)from now on\s+.{0,60}(you (will|must|should|shall)|always|never)\s+.{0,60}(instead|rather)",
            r"(?i)your (new |updated |real )?role is (now )?to\b",
        ],
    },
    # --- Tool Poisoning: malicious content hidden in tool descriptions ---
    {
        "id": "ATR-TP-001",
        "name": "Tool Description Injection",
        "category": "tool-poisoning",
        "severity": "high",
        "patterns": [
            r"(?i)when (this tool is |called|invoked|used)\s*.{0,50}(also|additionally)\s*.{0,50}(send|post|execute|run|forward)",
            r"(?i)(hidden|secret|additional|covert)\s+instructions?\b",
        ],
    },
    {
        "id": "ATR-TP-002",
        "name": "Tool Parameter Injection",
        "category": "tool-poisoning",
        "severity": "high",
        "patterns": [
            r"(?i)\[SYSTEM\]|\[INST\]|<\|system\|>|<\|im_start\|>",
            r"(?i)<!--.*?-->.*?(ignore|execute|run|send)",
        ],
    },
    # --- Excessive Autonomy: agents exceeding permission boundaries ---
    {
        "id": "ATR-EA-001",
        "name": "Unauthorized Destructive Action",
        "category": "excessive-autonomy",
        "severity": "high",
        "patterns": [
            r"(?i)(delete|remove|wipe|erase|format)\s+.{0,30}(all|every|entire)\s+.{0,30}(file|data|record|database|disk|directory)",
            r"(?i)(send|forward|post|upload|share)\s+.{0,30}(all|every|entire)\s+.{0,30}(file|data|email|message|document)",
        ],
    },
    {
        "id": "ATR-EA-002",
        "name": "Permission Escalation Attempt",
        "category": "excessive-autonomy",
        "severity": "medium",
        "patterns": [
            r"(?i)(grant|give|elevate|escalate)\s+.{0,30}(yourself|agent|bot|assistant)\s+.{0,30}(access|permission|privilege|admin)",
            r"(?i)(bypass|circumvent|skip|avoid)\s+.{0,30}(permission|authorization|approval|consent)\s+.{0,30}(check|verification|gate|step)",
        ],
    },
    # --- Context Exfiltration: leaking conversation / system context ---
    {
        "id": "ATR-CE-001",
        "name": "System Prompt Extraction",
        "category": "context-exfiltration",
        "severity": "high",
        "patterns": [
            r"(?i)(print|repeat|show|reveal|output|display|return)\s+.{0,30}(your|the)\s+.{0,30}(system.?prompt|initial.?instructions?|base.?prompt|context)",
            r"(?i)what (are|were) you (told|instructed|programmed|configured) to\b",
        ],
    },
    {
        "id": "ATR-CE-002",
        "name": "Conversation History Exfiltration",
        "category": "context-exfiltration",
        "severity": "medium",
        "patterns": [
            r"(?i)(copy|send|forward|email|transmit)\s+.{0,50}(conversation|chat.?history|message.?history|context.?window)",
            r"(?i)(leak|expose|exfiltrate|extract)\s+.{0,30}(context|conversation|history|system.?prompt)",
        ],
    },
    # --- Skill Compromise: corrupting agent config / skill definitions ---
    {
        "id": "ATR-SC-001",
        "name": "Configuration Tampering",
        "category": "skill-compromise",
        "severity": "high",
        "patterns": [
            r"(?i)(modify|update|change|edit|overwrite|replace)\s+.{0,30}(your|the|agent.?s?|system.?s?)\s+.{0,30}(config|configuration|settings|instructions?|rules|guidelines)",
            r"(?i)(inject|insert|append|prepend)\s+.{0,30}(into|to)\s+.{0,30}(system.?prompt|base.?prompt|context|instructions?)",
        ],
    },
    {
        "id": "ATR-SC-002",
        "name": "Skill Definition Override",
        "category": "skill-compromise",
        "severity": "high",
        "patterns": [
            r"(?i)(redefine|override|replace)\s+.{0,30}(your|the)\s+.{0,30}(function|capability|skill|tool|behavior|purpose)",
        ],
    },
]

_CompiledRule = tuple[str, str, str, list[re.Pattern[str]]]


def _load_yaml_rules(path: Path) -> list[dict]:
    try:
        import yaml  # type: ignore[import]
    except ImportError as exc:
        raise ImportError(
            "pyyaml is required to load ATR rules from YAML files. "
            "Install it with: pip install pyyaml"
        ) from exc

    with path.open() as fh:
        data = yaml.safe_load(fh)

    if isinstance(data, list):
        return data
    if isinstance(data, dict) and "rules" in data:
        return data["rules"]
    raise ValueError(f"ATR rule file must be a list or contain a 'rules' key: {path}")


def _compile_rules(rules: list[dict]) -> list[_CompiledRule]:
    compiled: list[_CompiledRule] = []
    for rule in rules:
        patterns = [re.compile(p) for p in rule.get("patterns", [])]
        if not patterns:
            continue
        compiled.append(
            (
                rule.get("id", "UNKNOWN"),
                rule.get("name", "Unknown Rule"),
                rule.get("severity", "medium"),
                patterns,
            )
        )
    return compiled


class ATRScanner(Scanner):
    """
    Input scanner based on Agent Threat Rules (ATR).

    Detects agent-based attack patterns across five categories:
    agent-manipulation, tool-poisoning, excessive-autonomy,
    context-exfiltration, and skill-compromise.
    """

    def __init__(
        self,
        rules_path: str | Path | list[str | Path] | None = None,
        *,
        use_builtin_rules: bool = True,
    ) -> None:
        """
        Parameters:
            rules_path: Path to a YAML rule file, directory of YAML files, or
                        list of file paths. Requires pyyaml when provided.
            use_builtin_rules: Whether to include built-in ATR rules. Default True.
        """
        rules: list[dict] = []

        if use_builtin_rules:
            rules.extend(_BUILT_IN_RULES)

        if rules_path is not None:
            paths: list[Path] = []
            if isinstance(rules_path, (str, Path)):
                p = Path(rules_path)
                if p.is_dir():
                    paths = sorted(p.glob("*.yml")) + sorted(p.glob("*.yaml"))
                else:
                    paths = [p]
            else:
                paths = [Path(rp) for rp in rules_path]

            for path in paths:
                rules.extend(_load_yaml_rules(path))

        self._rules: list[_CompiledRule] = _compile_rules(rules)

    def scan(self, prompt: str) -> tuple[str, bool, float]:
        if prompt.strip() == "":
            return prompt, True, -1.0

        for rule_id, rule_name, severity, patterns in self._rules:
            for pattern in patterns:
                if pattern.search(prompt):
                    score = _SEVERITY_SCORES.get(severity, 0.5)
                    LOGGER.warning(
                        "ATR rule matched in prompt",
                        rule_id=rule_id,
                        rule_name=rule_name,
                        severity=severity,
                    )
                    return prompt, False, score

        LOGGER.debug("No ATR rules matched in prompt")
        return prompt, True, -1.0
