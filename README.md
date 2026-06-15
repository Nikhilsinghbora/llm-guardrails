# LLM Guard Rails - Comprehensive Security Toolkit for LLM Interactions

> **About**: This is an actively maintained fork of the original [LLM Guard](https://github.com/protectai/llm-guard) project by [Protect AI](https://protectai.com/llm-guard). We maintain enhancements and improvements beyond the original project, ensuring continuous updates and feature development.

LLM Guard Rails is a comprehensive security toolkit designed to fortify the safety and security of Large Language Model (LLM) interactions. It provides robust protection against various attack vectors and malicious inputs with actively maintained enhancements.

[**Documentation**](https://github.com/Nikhilsinghbora/llm-guardrails) | [**Original Project**](https://github.com/protectai/llm-guard) | [**Getting Started**](./docs/get_started/quickstart.md)

[![GitHub
stars](https://img.shields.io/github/stars/protectai/llm-guard.svg?style=social&label=Star&maxAge=2592000)](https://GitHub.com/protectai/llm-guard/stargazers/)
[![MIT license](https://img.shields.io/badge/license-MIT-brightgreen.svg)](http://opensource.org/licenses/MIT)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![PyPI - Python Version](https://img.shields.io/pypi/v/llm-guard)](https://pypi.org/project/llm-guard)
[![Downloads](https://static.pepy.tech/badge/llm-guard)](https://pepy.tech/project/llm-guard)
[![Downloads](https://static.pepy.tech/badge/llm-guard/month)](https://pepy.tech/project/llm-guard)

<a href="https://mlsecops.com/slack"><img src="https://github.com/protectai/llm-guard/blob/main/docs/assets/join-our-slack-community.png?raw=true" width="200" alt="Join Our Slack Community"></a>

## What is LLM Guard?

![LLM-Guard](https://github.com/protectai/llm-guard/blob/main/docs/assets/flow.png?raw=true)

By offering sanitization, detection of harmful language, prevention of data leakage, and resistance against prompt
injection attacks, LLM-Guard ensures that your interactions with LLMs remain safe and secure.

## Installation

Begin your journey with LLM Guard Rails by downloading the package:

```sh
pip install llm-guardrails-maintained
```

Or install from source:

```sh
git clone https://github.com/Nikhilsinghbora/llm-guardrails.git
cd llm-guardrails
pip install -e .
```

## Getting Started

**Important Notes**:

- LLM Guard Rails is designed for easy integration and deployment in production environments. While it's ready to use
  out-of-the-box, please be informed that we're constantly improving and updating the repository.
- Base functionality requires a limited number of libraries. As you explore more advanced features, necessary libraries
  will be automatically installed.
- Ensure you're using Python version 3.10 or higher. Confirm with: `python --version`.
- We fully support Python 3.10, 3.11, 3.12, 3.13, and 3.14.
- Library installation issues? Consider upgrading pip: `python -m pip install --upgrade pip`.

**Examples**:

- Get started with [ChatGPT and LLM Guard](./examples/openai_api.py).
- Deploy LLM Guard as [API](https://protectai.github.io/llm-guard/api/overview/)

## Supported scanners

### Prompt scanners

- [Anonymize](https://protectai.github.io/llm-guard/input_scanners/anonymize/)
- [ATRScanner](./docs/input_scanners/atr.md) ⭐ **NEW**
- [BanCode](./docs/input_scanners/ban_code.md)
- [BanCompetitors](https://protectai.github.io/llm-guard/input_scanners/ban_competitors/)
- [BanSubstrings](https://protectai.github.io/llm-guard/input_scanners/ban_substrings/)
- [BanTopics](https://protectai.github.io/llm-guard/input_scanners/ban_topics/)
- [Code](https://protectai.github.io/llm-guard/input_scanners/code/)
- [Gibberish](https://protectai.github.io/llm-guard/input_scanners/gibberish/)
- [InvisibleText](https://protectai.github.io/llm-guard/input_scanners/invisible_text/)
- [Language](https://protectai.github.io/llm-guard/input_scanners/language/)
- [PromptInjection](https://protectai.github.io/llm-guard/input_scanners/prompt_injection/)
- [Regex](https://protectai.github.io/llm-guard/input_scanners/regex/)
- [Secrets](https://protectai.github.io/llm-guard/input_scanners/secrets/)
- [Sentiment](https://protectai.github.io/llm-guard/input_scanners/sentiment/)
- [TokenLimit](https://protectai.github.io/llm-guard/input_scanners/token_limit/)
- [Toxicity](https://protectai.github.io/llm-guard/input_scanners/toxicity/)

### Output scanners

- [ATRScanner](./docs/output_scanners/atr.md) ⭐ **NEW**
- [BanCode](./docs/output_scanners/ban_code.md)
- [BanCompetitors](https://protectai.github.io/llm-guard/output_scanners/ban_competitors/)
- [BanSubstrings](https://protectai.github.io/llm-guard/output_scanners/ban_substrings/)
- [BanTopics](https://protectai.github.io/llm-guard/output_scanners/ban_topics/)
- [Bias](https://protectai.github.io/llm-guard/output_scanners/bias/)
- [Code](https://protectai.github.io/llm-guard/output_scanners/code/)
- [Deanonymize](https://protectai.github.io/llm-guard/output_scanners/deanonymize/)
- [JSON](https://protectai.github.io/llm-guard/output_scanners/json/)
- [Language](https://protectai.github.io/llm-guard/output_scanners/language/)
- [LanguageSame](https://protectai.github.io/llm-guard/output_scanners/language_same/)
- [MaliciousURLs](https://protectai.github.io/llm-guard/output_scanners/malicious_urls/)
- [NoRefusal](https://protectai.github.io/llm-guard/output_scanners/no_refusal/)
- [ReadingTime](https://protectai.github.io/llm-guard/output_scanners/reading_time/)
- [FactualConsistency](https://protectai.github.io/llm-guard/output_scanners/factual_consistency/)
- [Gibberish](https://protectai.github.io/llm-guard/output_scanners/gibberish/)
- [Regex](https://protectai.github.io/llm-guard/output_scanners/regex/)
- [Relevance](https://protectai.github.io/llm-guard/output_scanners/relevance/)
- [Sensitive](https://protectai.github.io/llm-guard/output_scanners/sensitive/)
- [Sentiment](https://protectai.github.io/llm-guard/output_scanners/sentiment/)
- [Toxicity](https://protectai.github.io/llm-guard/output_scanners/toxicity/)
- [URLReachability](https://protectai.github.io/llm-guard/output_scanners/url_reachability/)

## Community, Contributing, Docs & Support

LLM Guard Rails is an open source solution maintained as an active fork of the original LLM Guard project.
We are committed to a transparent development process and highly appreciate any contributions.
Whether you are helping us fix bugs, propose new features, improve our documentation or spread the word,
we would love to have you as part of our community.

### How We Differ

- **Active Development**: We maintain and release updates more frequently than the original project
- **Feature Requests Welcome**: We actively review and implement community feature requests
- **Responsive Maintenance**: Issues and PRs receive timely reviews and updates

### Recent Improvements & Updates

**Security & Bug Fixes:**
- ✅ Fixed CVE-2026-26007: Updated `presidio-anonymizer` to ≥2.2.362
- ✅ Fixed critical transformers vulnerability (GHSA-phhr-52qp-3mj4)
- ✅ Fixed Anonymize scanner to properly respect language parameter (#337)
- ✅ Fixed PromptInjection tokenizer initialization bug (#331)
- ✅ Fixed MaliciousURLs missing top_k parameter TypeError (#318)

**New Features & Enhancements:**
- ✅ **Python 3.13+ Support**: Full compatibility with Python 3.13 and 3.14
- ✅ **ATRScanner**: New Agent Threat Rule scanner with 10+ built-in detection patterns
- ✅ **ThresholdMixin**: Dynamically adjust scanner sensitivity without model reloading
- ✅ **Model.from_local()**: Factory method for locally-downloaded HuggingFace models
- ✅ Improved dependency management for better compatibility

### Get Involved

- Give us a ⭐️ github star ⭐️ on the top of this page to support what we're doing,
  it means a lot for open source projects!
- Read our
  [docs](./docs/index.md)
  for more info about how to use and customize LLM Guard Rails, and for step-by-step tutorials.
- Post a [Github Issue](https://github.com/Nikhilsinghbora/llm-guardrails/issues) to submit a bug report, feature request, or suggest an improvement.
- To contribute to the package, check out our [contribution guidelines](CONTRIBUTING.md), and open a PR.

### Support & Contact

We're eager to provide personalized assistance and discuss feature requests or improvements.

- [Send Email ✉️](mailto:nikhilsinghbora17@gmail.com) - Open to feature requests, improvements, and collaboration
- [GitHub Issues](https://github.com/Nikhilsinghbora/llm-guardrails/issues) - Report bugs or request features
