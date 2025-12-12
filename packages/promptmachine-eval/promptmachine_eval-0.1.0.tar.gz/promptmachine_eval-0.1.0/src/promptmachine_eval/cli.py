"""
CLI for promptmachine-eval

Provides command-line tools for:
- Testing prompts across models
- Running arena battles
- Estimating costs
- Managing configurations

Example:
    $ pm-eval test "What is 2+2?" --models gpt-4o-mini,claude-3-5-haiku
    $ pm-eval battle "Write a poem" -a gpt-4o -b claude-3-5-sonnet
    $ pm-eval cost "Your prompt here" --models gpt-4o,gpt-4o-mini
"""

import asyncio
import os
import sys
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import print as rprint

app = typer.Typer(
    name="pm-eval",
    help="LLM evaluation toolkit by PromptMachine",
    add_completion=False,
)

console = Console()


def get_api_keys() -> tuple[Optional[str], Optional[str], Optional[str]]:
    """Get API keys from environment."""
    return (
        os.getenv("OPENAI_API_KEY"),
        os.getenv("ANTHROPIC_API_KEY"),
        os.getenv("OPENROUTER_API_KEY"),
    )


@app.command("test")
def test_prompt(
    prompt: str = typer.Argument(..., help="Prompt to test"),
    models: str = typer.Option(
        "gpt-4o-mini",
        "--models", "-m",
        help="Comma-separated list of models to test",
    ),
    system: Optional[str] = typer.Option(
        None,
        "--system", "-s",
        help="System prompt",
    ),
    temperature: float = typer.Option(
        0.7,
        "--temperature", "-t",
        help="Generation temperature",
    ),
    max_tokens: int = typer.Option(
        1024,
        "--max-tokens",
        help="Maximum output tokens",
    ),
    output_format: str = typer.Option(
        "table",
        "--format", "-f",
        help="Output format: table, json, simple",
    ),
) -> None:
    """
    Test a prompt across multiple LLM models.
    
    Example:
        pm-eval test "Explain recursion" --models gpt-4o,gpt-4o-mini,claude-3-5-haiku
    """
    from promptmachine_eval.runner import PromptTester
    
    openai_key, anthropic_key, openrouter_key = get_api_keys()
    model_list = [m.strip() for m in models.split(",")]
    
    if not any([openai_key, anthropic_key, openrouter_key]):
        console.print(
            "[red]Error:[/red] No API keys found. Set OPENAI_API_KEY, "
            "ANTHROPIC_API_KEY, or OPENROUTER_API_KEY environment variable."
        )
        raise typer.Exit(1)
    
    tester = PromptTester(
        openai_api_key=openai_key,
        anthropic_api_key=anthropic_key,
        openrouter_api_key=openrouter_key,
    )
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task(f"Testing {len(model_list)} models...", total=None)
        results = asyncio.run(
            tester.test(
                prompt=prompt,
                models=model_list,
                system_prompt=system,
                temperature=temperature,
                max_tokens=max_tokens,
            )
        )
    
    if output_format == "table":
        table = Table(title="Test Results")
        table.add_column("Model", style="cyan")
        table.add_column("Tokens", justify="right")
        table.add_column("Latency", justify="right")
        table.add_column("Cost", justify="right", style="green")
        table.add_column("Status")
        
        for r in results:
            status = "[red]ERROR[/red]" if r.error else "[green]OK[/green]"
            table.add_row(
                r.model,
                str(r.tokens_total),
                f"{r.latency_ms}ms",
                f"${r.cost:.4f}",
                status,
            )
        
        console.print(table)
        
        # Show responses
        for r in results:
            if not r.error:
                console.print(Panel(
                    r.response[:500] + ("..." if len(r.response) > 500 else ""),
                    title=f"[cyan]{r.model}[/cyan]",
                    border_style="dim",
                ))
    
    elif output_format == "json":
        import json
        output = [
            {
                "model": r.model,
                "response": r.response,
                "tokens": r.tokens_total,
                "latency_ms": r.latency_ms,
                "cost": r.cost,
                "error": r.error,
            }
            for r in results
        ]
        print(json.dumps(output, indent=2))
    
    else:  # simple
        for r in results:
            print(f"\n=== {r.model} ===")
            if r.error:
                print(f"ERROR: {r.error}")
            else:
                print(r.response)
            print(f"\n({r.tokens_total} tokens, {r.latency_ms}ms, ${r.cost:.4f})")


@app.command("battle")
def run_battle(
    prompt: str = typer.Argument(..., help="Battle prompt"),
    model_a: str = typer.Option(
        ...,
        "-a", "--model-a",
        help="First model",
    ),
    model_b: str = typer.Option(
        ...,
        "-b", "--model-b",
        help="Second model",
    ),
    judge: str = typer.Option(
        "gpt-4o-mini",
        "-j", "--judge",
        help="Judge model",
    ),
    system: Optional[str] = typer.Option(
        None,
        "-s", "--system",
        help="System prompt for contestants",
    ),
    verbose: bool = typer.Option(
        False,
        "-v", "--verbose",
        help="Show full responses",
    ),
) -> None:
    """
    Run a head-to-head battle between two models.
    
    Example:
        pm-eval battle "Write a haiku" -a gpt-4o -b claude-3-5-sonnet
    """
    from promptmachine_eval.battle import BattleRunner
    
    openai_key, anthropic_key, openrouter_key = get_api_keys()
    
    if not any([openai_key, anthropic_key]):
        console.print(
            "[red]Error:[/red] No API keys found. Set OPENAI_API_KEY or "
            "ANTHROPIC_API_KEY environment variable."
        )
        raise typer.Exit(1)
    
    runner = BattleRunner(
        openai_api_key=openai_key,
        anthropic_api_key=anthropic_key,
        openrouter_api_key=openrouter_key,
    )
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        progress.add_task(f"Running battle: {model_a} vs {model_b}...", total=None)
        result = asyncio.run(
            runner.battle(
                prompt=prompt,
                model_a=model_a,
                model_b=model_b,
                judge_model=judge,
                system_prompt=system,
            )
        )
    
    # Winner announcement
    if result.winner == model_a:
        winner_display = f"[bold green]{model_a}[/bold green] wins! 🏆"
    elif result.winner == model_b:
        winner_display = f"[bold green]{model_b}[/bold green] wins! 🏆"
    else:
        winner_display = "[yellow]It's a draw![/yellow]"
    
    console.print(Panel(
        winner_display,
        title="Battle Result",
        border_style="green",
    ))
    
    console.print(f"\n[dim]Judge reasoning:[/dim] {result.judgement.reasoning}")
    console.print(f"\n[dim]Total cost:[/dim] ${result.total_cost:.4f}")
    
    if verbose:
        console.print(Panel(
            result.response_a[:800] + ("..." if len(result.response_a) > 800 else ""),
            title=f"[cyan]{model_a}[/cyan]",
            border_style="dim",
        ))
        console.print(Panel(
            result.response_b[:800] + ("..." if len(result.response_b) > 800 else ""),
            title=f"[cyan]{model_b}[/cyan]",
            border_style="dim",
        ))


@app.command("cost")
def estimate_cost(
    prompt: str = typer.Argument(..., help="Prompt to estimate cost for"),
    models: str = typer.Option(
        "gpt-4o,gpt-4o-mini,claude-3-5-sonnet,claude-3-5-haiku",
        "--models", "-m",
        help="Comma-separated list of models",
    ),
    output_tokens: int = typer.Option(
        500,
        "--output-tokens", "-o",
        help="Expected output tokens",
    ),
) -> None:
    """
    Estimate costs for a prompt across models.
    
    Example:
        pm-eval cost "Write a detailed essay about AI" --output-tokens 2000
    """
    from promptmachine_eval.cost import CostTracker
    
    tracker = CostTracker()
    model_list = [m.strip() for m in models.split(",")]
    
    table = Table(title="Cost Estimates")
    table.add_column("Model", style="cyan")
    table.add_column("Input Tokens", justify="right")
    table.add_column("Output Tokens", justify="right")
    table.add_column("Input Cost", justify="right")
    table.add_column("Output Cost", justify="right")
    table.add_column("Total", justify="right", style="green")
    
    for model in model_list:
        estimate = tracker.estimate(
            prompt=prompt,
            model=model,
            expected_output_tokens=output_tokens,
        )
        table.add_row(
            model,
            str(estimate.input_tokens),
            str(estimate.output_tokens),
            f"${estimate.input_cost:.6f}",
            f"${estimate.output_cost:.6f}",
            f"${estimate.total:.6f}",
        )
    
    console.print(table)
    
    # Show cheapest option
    estimates = [
        tracker.estimate(prompt, m, output_tokens)
        for m in model_list
    ]
    cheapest = min(estimates, key=lambda e: e.total)
    console.print(f"\n💡 [green]Cheapest option:[/green] {cheapest.model} at ${cheapest.total:.6f}")


@app.command("models")
def list_models() -> None:
    """
    List available models and their pricing.
    """
    from promptmachine_eval.cost import MODEL_PRICING
    
    table = Table(title="Supported Models")
    table.add_column("Model", style="cyan")
    table.add_column("Input ($/1K)", justify="right")
    table.add_column("Output ($/1K)", justify="right")
    table.add_column("Provider")
    
    for model, pricing in sorted(MODEL_PRICING.items()):
        # Determine provider
        if "gpt" in model.lower() or "o1" in model.lower():
            provider = "OpenAI"
        elif "claude" in model.lower():
            provider = "Anthropic"
        elif "google/" in model.lower() or "gemini" in model.lower():
            provider = "Google"
        elif "meta-llama" in model.lower():
            provider = "Meta"
        elif "mistral" in model.lower():
            provider = "Mistral"
        elif "deepseek" in model.lower():
            provider = "DeepSeek"
        elif "qwen" in model.lower():
            provider = "Qwen"
        else:
            provider = "Other"
        
        table.add_row(
            model,
            f"${pricing['input']:.5f}",
            f"${pricing['output']:.5f}",
            provider,
        )
    
    console.print(table)


@app.command("version")
def show_version() -> None:
    """Show version information."""
    from promptmachine_eval import __version__
    
    rprint(f"[bold cyan]promptmachine-eval[/bold cyan] v{__version__}")
    rprint("[dim]LLM Evaluation Framework by Frame.dev[/dim]")
    rprint("[dim]https://promptmachine.io[/dim]")


@app.command("init")
def init_config(
    force: bool = typer.Option(False, "--force", "-f", help="Overwrite existing config"),
) -> None:
    """
    Create a default promptmachine.yaml config file.
    """
    config_content = """# promptmachine.yaml
# Configuration for promptmachine-eval CLI

version: 1

# Default models for testing
default_models:
  - gpt-4o-mini
  - claude-3-5-haiku

# Battle settings
battle:
  judge_model: gpt-4o-mini
  temperature: 0.7
  max_tokens: 1024

# Cost limits (optional)
# limits:
#   max_cost_per_test: 0.10
#   daily_budget: 5.00

# ELO settings
elo:
  k_factor: 32
  initial_rating: 1000
  initial_sd: 350

# API keys - prefer environment variables instead
# openai_api_key: sk-...
# anthropic_api_key: sk-ant-...
"""
    
    config_path = "promptmachine.yaml"
    
    if os.path.exists(config_path) and not force:
        console.print(f"[yellow]Config file already exists:[/yellow] {config_path}")
        console.print("Use --force to overwrite.")
        raise typer.Exit(1)
    
    with open(config_path, "w") as f:
        f.write(config_content)
    
    console.print(f"[green]Created config file:[/green] {config_path}")
    console.print("\n[dim]Set your API keys as environment variables:[/dim]")
    console.print("  export OPENAI_API_KEY=sk-...")
    console.print("  export ANTHROPIC_API_KEY=sk-ant-...")


def main() -> None:
    """Entry point for CLI."""
    app()


if __name__ == "__main__":
    main()

