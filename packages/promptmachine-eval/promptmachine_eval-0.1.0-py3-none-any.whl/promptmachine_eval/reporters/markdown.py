"""
Markdown Report Generator

Generate evaluation reports in Markdown format.
"""

from typing import Any, Optional
from datetime import datetime

from promptmachine_eval.reporters.base import Reporter, ReportConfig


class MarkdownReporter(Reporter):
    """
    Generate Markdown evaluation reports.
    
    Example:
        >>> reporter = MarkdownReporter()
        >>> content = reporter.generate({
        ...     "rankings": [...],
        ...     "battles": [...],
        ... })
        >>> reporter.save(content, "report.md")
    """
    
    def generate(self, data: dict[str, Any]) -> str:
        """
        Generate Markdown report.
        
        Expected data keys:
        - rankings: List of (model, elo, battles, win_rate)
        - battles: Optional list of battle results
        - period: Report period (e.g., "Daily", "Weekly")
        - generated_at: Timestamp
        
        Args:
            data: Report data.
            
        Returns:
            Markdown string.
        """
        lines = []
        
        # Header
        period = data.get("period", "Daily")
        generated = data.get("generated_at", datetime.utcnow())
        if isinstance(generated, str):
            generated = datetime.fromisoformat(generated.replace("Z", "+00:00"))
        
        lines.append(f"# {self.config.title}")
        lines.append("")
        lines.append(f"**Period:** {period}")
        lines.append(f"**Generated:** {generated.strftime('%Y-%m-%d %H:%M UTC')}")
        lines.append(f"**Author:** {self.config.author}")
        lines.append("")
        
        # Rankings table
        rankings = data.get("rankings", [])
        if rankings:
            lines.append("## 🏆 Leaderboard")
            lines.append("")
            lines.append("| Rank | Model | ELO | Battles | Win Rate |")
            lines.append("|------|-------|-----|---------|----------|")
            
            for i, entry in enumerate(rankings[:20], 1):
                model = entry.get("model", entry.get("name", "Unknown"))
                elo = entry.get("elo", entry.get("elo_rating", 0))
                battles = entry.get("battles", entry.get("battles_count", 0))
                win_rate = entry.get("win_rate", 0)
                
                # Medal for top 3
                medal = ""
                if i == 1:
                    medal = "🥇 "
                elif i == 2:
                    medal = "🥈 "
                elif i == 3:
                    medal = "🥉 "
                
                lines.append(
                    f"| {i} | {medal}{model} | {elo:.0f} | {battles} | {win_rate:.1f}% |"
                )
            
            lines.append("")
        
        # Top movers
        gainers = data.get("gainers", [])
        losers = data.get("losers", [])
        
        if gainers or losers:
            lines.append("## 📈 Top Movers")
            lines.append("")
            
            if gainers:
                lines.append("### Gainers")
                for entry in gainers[:5]:
                    model = entry.get("model", "Unknown")
                    change = entry.get("change", 0)
                    lines.append(f"- **{model}**: +{change:.0f}")
                lines.append("")
            
            if losers:
                lines.append("### Decliners")
                for entry in losers[:5]:
                    model = entry.get("model", "Unknown")
                    change = entry.get("change", 0)
                    lines.append(f"- **{model}**: {change:.0f}")
                lines.append("")
        
        # Battle summary
        battles = data.get("battles", [])
        if battles:
            lines.append("## ⚔️ Recent Battles")
            lines.append("")
            lines.append(f"Total battles this period: **{len(battles)}**")
            lines.append("")
            
            if self.config.include_responses:
                lines.append("### Sample Battles")
                lines.append("")
                
                for battle in battles[:5]:
                    model_a = battle.get("model_a", "Model A")
                    model_b = battle.get("model_b", "Model B")
                    winner = battle.get("winner", "draw")
                    
                    lines.append(f"#### {model_a} vs {model_b}")
                    lines.append(f"**Winner:** {winner}")
                    lines.append("")
        
        # Benchmark results
        benchmarks = data.get("benchmarks", {})
        if benchmarks:
            lines.append("## 📊 Benchmark Results")
            lines.append("")
            
            for bench_name, results in benchmarks.items():
                lines.append(f"### {bench_name}")
                lines.append("")
                lines.append("| Model | Score |")
                lines.append("|-------|-------|")
                
                for model, score in sorted(
                    results.items(),
                    key=lambda x: x[1],
                    reverse=True,
                ):
                    lines.append(f"| {model} | {score:.1f}% |")
                
                lines.append("")
        
        # Footer
        lines.append("---")
        lines.append("")
        lines.append(
            "Generated by [PromptMachine](https://promptmachine.io) | "
            "[View Live Leaderboard](https://promptmachine.io/leaderboard)"
        )
        
        return "\n".join(lines)
    
    def generate_changelog(
        self,
        changes: list[dict[str, Any]],
        version: str,
    ) -> str:
        """
        Generate a changelog entry.
        
        Args:
            changes: List of changes with type and description.
            version: Version string.
            
        Returns:
            Markdown changelog entry.
        """
        lines = []
        date = datetime.utcnow().strftime("%Y-%m-%d")
        
        lines.append(f"## [{version}] - {date}")
        lines.append("")
        
        # Group by type
        grouped: dict[str, list[str]] = {}
        for change in changes:
            change_type = change.get("type", "Changed")
            desc = change.get("description", "")
            if change_type not in grouped:
                grouped[change_type] = []
            grouped[change_type].append(desc)
        
        type_order = ["Added", "Changed", "Fixed", "Removed", "Security"]
        for change_type in type_order:
            if change_type in grouped:
                lines.append(f"### {change_type}")
                for desc in grouped[change_type]:
                    lines.append(f"- {desc}")
                lines.append("")
        
        return "\n".join(lines)

