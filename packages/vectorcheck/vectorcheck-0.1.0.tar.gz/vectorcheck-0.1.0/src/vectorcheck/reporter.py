from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from typing import Dict, Any

console = Console()

class TestReporter:
    @staticmethod
    def print_summary(target: str, results: Dict[str, Any]):
        console.print()
        console.print(Panel(f"[bold cyan]🔍 Testing Target:[/bold cyan] {target}", expand=False))

        if "error" in results:
            console.print(Panel(f"[bold red]❌ Execution Failed[/bold red]\n\n{results['error']}", border_style="red"))
            return

        # Summary Table
        grid = Table.grid(expand=True)
        grid.add_column()
        grid.add_column(justify="right")
        grid.add_row(f"[bold]Total Cases[/bold]", str(results['total']))
        grid.add_row(f"[bold green]✅ Passed[/bold green]", str(results['passed']))
        grid.add_row(f"[bold red]❌ Failed[/bold red]", str(results['failed']))

        console.print(Panel(grid, title="Summary", border_style="green" if results['failed'] == 0 else "red"))

        # Failure Detail
        if results['failures']:
            table = Table(title="❌ Failure Details", show_lines=True)
            table.add_column("UUID", style="dim", no_wrap=True)
            table.add_column("Type", justify="center")
            table.add_column("Expected", style="green")
            table.add_column("Actual", style="red")

            for fail in results['failures']:
                mark = "🌟 GOLDEN" if fail.get('is_golden') else "Log"
                uuid = fail.get('uuid')

                if 'error' in fail:
                    table.add_row(uuid, mark, "-", f"[bold]Error:[/bold] {fail['error']}")
                else:
                    table.add_row(
                        uuid,
                        mark,
                        str(fail['expected'])[:50],
                        str(fail['actual'])[:50]
                    )

            console.print(table)