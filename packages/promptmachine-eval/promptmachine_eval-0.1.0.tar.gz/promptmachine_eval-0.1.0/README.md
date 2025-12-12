<p align="center">
  <img src="https://promptmachine.io/logo-eval.svg" alt="promptmachine-eval" width="120" height="120">
</p>

<h1 align="center">promptmachine-eval</h1>

<p align="center">
  <strong>LLM Evaluation Framework</strong><br>
  ELO ratings • Arena battles • Benchmark testing • Cost tracking
</p>

<p align="center">
  <a href="https://pypi.org/project/promptmachine-eval/"><img src="https://img.shields.io/pypi/v/promptmachine-eval?color=blue&logo=pypi&logoColor=white" alt="PyPI"></a>
  <a href="https://pypi.org/project/promptmachine-eval/"><img src="https://img.shields.io/pypi/pyversions/promptmachine-eval?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://github.com/framersai/promptmachine-eval/actions"><img src="https://img.shields.io/github/actions/workflow/status/framersai/promptmachine-eval/ci.yml?branch=main&logo=github" alt="CI"></a>
  <a href="https://codecov.io/gh/framersai/promptmachine-eval"><img src="https://img.shields.io/codecov/c/github/framersai/promptmachine-eval?logo=codecov&logoColor=white" alt="Coverage"></a>
  <a href="https://github.com/framersai/promptmachine-eval/blob/main/LICENSE"><img src="https://img.shields.io/github/license/framersai/promptmachine-eval?color=green" alt="License"></a>
</p>

<p align="center">
  <a href="https://promptmachine.io/docs/eval">Documentation</a> •
  <a href="https://promptmachine.io/leaderboard">Live Leaderboard</a> •
  <a href="https://promptmachine.io/arena">Arena</a> •
  <a href="https://frame.dev">Frame.dev</a>
</p>

---

## Overview

**promptmachine-eval** is a Python toolkit for evaluating and comparing Large Language Models. Built by [Frame.dev](https://frame.dev) as part of [PromptMachine](https://promptmachine.io).

### Key Features

- 🏆 **ELO Rating System** — Chess-style ratings for fair LLM comparisons
- ⚔️ **Arena Battles** — Head-to-head comparisons with LLM-as-judge
- 📊 **Benchmarks** — Run standard evals (MMLU, GSM8K, HumanEval)
- 🎯 **Smart Matchmaking** — Monte Carlo sampling for informative pairings
- 💰 **Cost Tracking** — Real-time token counting and spend estimation
- 📈 **Reports** — Generate Markdown evaluation reports

## Installation

```bash
pip install promptmachine-eval
```

For development:

```bash
pip install promptmachine-eval[dev]
```

## Quick Start

### CLI Usage

```bash
# Set your API keys
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...

# Test a prompt across models
pm-eval test "Explain quantum computing simply" \
  --models gpt-4o-mini,claude-3-5-haiku

# Run a head-to-head battle
pm-eval battle "Write a haiku about coding" \
  -a gpt-4o -b claude-3-5-sonnet

# Estimate costs before running
pm-eval cost "Your long prompt..." \
  --models gpt-4o,gpt-4o-mini,claude-3-5-sonnet

# List all supported models and pricing
pm-eval models
```

### Python API

```python
import asyncio
from promptmachine_eval import EloCalculator, BattleRunner, PromptTester

# --- ELO Calculations ---
elo = EloCalculator()

# Calculate rating changes after a battle
new_a, new_b = elo.update_ratings(
    rating_a=1200,
    rating_b=1000,
    score_a=1.0  # A wins
)
print(f"New ratings: A={new_a:.0f}, B={new_b:.0f}")

# --- Run Arena Battle ---
runner = BattleRunner(
    openai_api_key="sk-...",
    anthropic_api_key="sk-ant-..."
)

result = asyncio.run(runner.battle(
    prompt="Write a function to reverse a linked list",
    model_a="gpt-4o",
    model_b="claude-3-5-sonnet",
    judge_model="gpt-4o-mini"
))

print(f"Winner: {result.winner}")
print(f"Reasoning: {result.judgement.reasoning}")
print(f"Cost: ${result.total_cost:.4f}")

# --- Test Multiple Models ---
tester = PromptTester(openai_api_key="sk-...")

results = asyncio.run(tester.test(
    prompt="Explain recursion to a beginner",
    models=["gpt-4o", "gpt-4o-mini", "gpt-3.5-turbo"]
))

for r in results:
    print(f"{r.model}: {r.latency_ms}ms, ${r.cost:.4f}")
```

### Matchmaking

Select optimal battle pairings using Monte Carlo simulation:

```python
from promptmachine_eval import MatchmakingService, ModelInfo

service = MatchmakingService()

models = [
    ModelInfo(id="gpt4o", rating=1200, sd=100, battles_count=50),
    ModelInfo(id="claude", rating=1180, sd=120, battles_count=40),
    ModelInfo(id="gemini", rating=1100, sd=200, battles_count=10),
]

# Get optimal pairing (balances competitiveness + uncertainty)
model_a, model_b = service.select_pair_for_battle(models)
print(f"Recommended battle: {model_a.id} vs {model_b.id}")
```

## Configuration

Create `promptmachine.yaml` in your project:

```yaml
version: 1

default_models:
  - gpt-4o-mini
  - claude-3-5-haiku

battle:
  judge_model: gpt-4o-mini
  temperature: 0.7

elo:
  k_factor: 32
  initial_rating: 1000

limits:
  max_cost_per_test: 0.10
  daily_budget: 5.00
```

Or use environment variables:

```bash
export OPENAI_API_KEY=sk-...
export ANTHROPIC_API_KEY=sk-ant-...
export OPENROUTER_API_KEY=sk-or-...
```

## Supported Models

| Provider | Models |
|----------|--------|
| **OpenAI** | gpt-4o, gpt-4o-mini, gpt-4-turbo, gpt-3.5-turbo, o1-preview, o1-mini |
| **Anthropic** | claude-3-5-sonnet, claude-3-5-haiku, claude-3-opus |
| **OpenRouter** | gemini-pro-1.5, llama-3.1-70b, mistral-large, deepseek-coder, qwen-max, + more |

<details>
<summary>View full pricing table</summary>

| Model | Input ($/1K) | Output ($/1K) |
|-------|-------------|---------------|
| gpt-4o | $0.0025 | $0.01 |
| gpt-4o-mini | $0.00015 | $0.0006 |
| claude-3-5-sonnet | $0.003 | $0.015 |
| claude-3-5-haiku | $0.001 | $0.005 |
| gemini-pro-1.5 | $0.00125 | $0.005 |
| llama-3.1-70b | $0.00052 | $0.00075 |

</details>

## ELO Rating System

We use a modified ELO system inspired by [Chatbot Arena](https://chat.lmsys.org/):

```python
from promptmachine_eval import EloCalculator, EloConfig

# Custom configuration
config = EloConfig(
    k_factor=32,        # Rating volatility (higher = more change)
    initial_rating=1000,
    initial_sd=350,     # Uncertainty (decreases with more battles)
)

elo = EloCalculator(config)

# Expected win probability
prob = elo.expected_score(1200, 1000)
print(f"1200-rated has {prob:.1%} chance vs 1000-rated")
# Output: 1200-rated has 75.9% chance vs 1000-rated

# With uncertainty (Monte Carlo)
prob = elo.win_probability(1200, 1000, sd_a=100, sd_b=200)
```

## Documentation

- 📖 [Full Documentation](https://promptmachine.io/docs/eval)
- 📚 [API Reference](https://promptmachine.io/docs/eval/api)
- 💡 [Examples](https://github.com/framersai/promptmachine-eval/tree/main/examples)
- 🎯 [Live Leaderboard](https://promptmachine.io/leaderboard)

## Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

```bash
# Clone the repo
git clone https://github.com/framersai/promptmachine-eval.git
cd promptmachine-eval

# Install for development
pip install -e ".[dev]"

# Run tests
pytest

# Run linting
ruff check .
black --check .
mypy src/
```

## License

MIT License — see [LICENSE](LICENSE) for details.

## Links

<p align="center">
  <a href="https://promptmachine.io">🌐 PromptMachine</a> •
  <a href="https://frame.dev">🏢 Frame.dev</a> •
  <a href="https://github.com/framersai/promptmachine-eval">🐙 GitHub</a> •
  <a href="https://twitter.com/framedev">🐦 Twitter</a>
</p>

<p align="center">
  <sub>Built with ❤️ by <a href="https://frame.dev">Frame.dev</a></sub><br>
  <sub>Questions? <a href="mailto:team@frame.dev">team@frame.dev</a></sub>
</p>
