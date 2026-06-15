from __future__ import annotations

from pathlib import Path

from llm_guard.input_scanners.atr import _SEVERITY_SCORES, _compile_rules, _load_yaml_rules
from llm_guard.input_scanners.atr import _BUILT_IN_RULES, _CompiledRule
from llm_guard.util import get_logger

from .base import Scanner

LOGGER = get_logger()


class ATRScanner(Scanner):
    """
    Output scanner based on Agent Threat Rules (ATR).

    Detects agent-based attack patterns in LLM output across five categories:
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

    def scan(self, prompt: str, output: str) -> tuple[str, bool, float]:
        if output.strip() == "":
            return output, True, -1.0

        for rule_id, rule_name, severity, patterns in self._rules:
            for pattern in patterns:
                if pattern.search(output):
                    score = _SEVERITY_SCORES.get(severity, 0.5)
                    LOGGER.warning(
                        "ATR rule matched in output",
                        rule_id=rule_id,
                        rule_name=rule_name,
                        severity=severity,
                    )
                    return output, False, score

        LOGGER.debug("No ATR rules matched in output")
        return output, True, -1.0
