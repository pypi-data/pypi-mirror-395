import typer
import sys
import os
import time
import json
import configparser
from typing import Optional, List, Dict, Tuple
from rich.progress import Progress
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from dotenv import load_dotenv  # [필수] python-dotenv 설치 필요

# Import internal modules
from .runner import TestRunner
from .reporter import TestReporter
from .source import DataSourceFactory

try:
    from vectorwave.batch.batch import get_batch_manager
    from vectorwave.database.db import get_cached_client
except ImportError:
    get_batch_manager = None
    get_cached_client = None

app = typer.Typer(help="Vectorboard: AI Native Testing Framework", rich_markup_mode="rich")
console = Console()

# ------------------------------------------------------------------------------
# 0. Helper: Find Project Root & Setup Env
# ------------------------------------------------------------------------------
def find_project_root() -> str:
    """Find the project root looking for vwtest.ini or pyproject.toml"""
    current_path = os.path.abspath(os.getcwd())
    while True:
        if os.path.exists(os.path.join(current_path, "vwtest.ini")):
            return current_path
        if os.path.exists(os.path.join(current_path, "pyproject.toml")):
            return current_path
        parent_path = os.path.dirname(current_path)
        if parent_path == current_path:
            break
        current_path = parent_path
    return os.getcwd()

def setup_env():
    """
    .env 파일이 없으면 기본 설정값으로 생성하고, 환경 변수를 로드합니다.
    """
    project_root = find_project_root()
    env_path = os.path.join(project_root, ".env")

    if not os.path.exists(env_path):
        console.print(Panel(f"[bold yellow]⚠️  No .env file found![/bold yellow]\nCreating default configuration at: [underline]{env_path}[/underline]", title="Auto Setup"))

        # 사용자가 제안한 기본 설정값 (HuggingFace 로컬 모드)
        default_content = """WEAVIATE_HOST=localhost
WEAVIATE_PORT=8080
WEAVIATE_GRPC_PORT=50051

# [Optional] OpenAI API Key (Leave empty if using HuggingFace)
OPENAI_API_KEY=

# Default Vectorizer: HuggingFace (Local, No Cost)
VECTORIZER="huggingface"
HF_MODEL_NAME="sentence-transformers/all-MiniLM-L6-v2"

CUSTOM_PROPERTIES_FILE_PATH=.weaviate_properties
RUN_ID=test-run-local-001
"""
        try:
            with open(env_path, "w", encoding="utf-8") as f:
                f.write(default_content)
            console.print("[bold green]✅ Default .env file created successfully![/bold green]")
        except Exception as e:
            console.print(f"[bold red]❌ Failed to create .env file: {e}[/bold red]")

    # 환경 변수 로드
    load_dotenv(env_path)

# 앱 시작 시 환경 변수 세팅 실행
setup_env()

# ------------------------------------------------------------------------------
# 1. Smart Path Setup
# ------------------------------------------------------------------------------
def setup_python_paths():
    project_root = find_project_root()

    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    src_path = os.path.join(project_root, "src")
    if os.path.exists(src_path) and src_path not in sys.path:
        sys.path.insert(0, src_path)

    ini_path = os.path.join(project_root, "vwtest.ini")
    if os.path.exists(ini_path):
        try:
            config = configparser.ConfigParser()
            config.read(ini_path, encoding='utf-8')
            if "vectorcheck" in config:
                paths_str = config.get("vectorcheck", "python_paths", fallback="")
                extra_paths = [p.strip() for p in paths_str.split(',') if p.strip()]
                for path in extra_paths:
                    abs_path = os.path.abspath(os.path.join(project_root, path))
                    if abs_path not in sys.path:
                        sys.path.insert(0, abs_path)
                        console.print(f"[dim]Added custom path from ini: {abs_path}[/dim]")
        except Exception:
            pass

setup_python_paths()

# ------------------------------------------------------------------------------
# 2. Function List Retrieval (Advanced Deduplication)
# ------------------------------------------------------------------------------
def get_all_registered_functions() -> List[str]:
    client = get_cached_client()
    if not client:
        return []

    try:
        funcs_col = client.collections.get("VectorWaveFunctions")
        response = funcs_col.query.fetch_objects(limit=1000)

        func_map: Dict[Tuple[str, str], List[str]] = {}

        for obj in response.objects:
            props = obj.properties
            mod = props.get("module_name")
            name = props.get("function_name")
            source_code = props.get("source_code", "")

            if mod and name and source_code and "replay=True" in source_code:
                key = (name, source_code)
                if key not in func_map:
                    func_map[key] = []
                func_map[key].append(mod)

        targets = []
        for (func_name, _), modules in func_map.items():
            if len(modules) == 1:
                targets.append(f"{modules[0]}.{func_name}")
                continue

            if "__main__" in modules and len(modules) > 1:
                modules.remove("__main__")

            modules.sort(key=lambda x: len(x), reverse=True)
            best_module = modules[0]
            targets.append(f"{best_module}.{func_name}")

        return sorted(targets)

    except Exception as e:
        typer.secho(f"⚠️ Error fetching functions list: {e}", fg=typer.colors.YELLOW)
        return []

def get_target_config(target_name: str, cli_semantic: bool, cli_threshold: Optional[float]):
    """
    vwtest.ini 파일에서 특정 함수에 대한 설정을 읽어옵니다.
    """
    project_root = find_project_root()
    ini_path = os.path.join(project_root, "vwtest.ini")

    config = configparser.ConfigParser()

    if os.path.exists(ini_path):
        try:
            config.read(ini_path, encoding='utf-8')
        except Exception:
            pass

    final_semantic = cli_semantic
    final_threshold = cli_threshold
    section = f"test:{target_name}"

    if config.has_section(section):
        if config.has_option(section, "strategy"):
            strategy = config.get(section, "strategy").lower()

            if strategy == "semantic":
                if not cli_semantic:
                    final_semantic = True
                final_threshold = None

            elif strategy == "similarity":
                final_semantic = False
                if final_threshold is None:
                    if config.has_option(section, "threshold"):
                        try:
                            final_threshold = config.getfloat(section, "threshold")
                        except ValueError:
                            final_threshold = 0.8
                    else:
                        final_threshold = 0.8

            elif strategy == "exact":
                final_semantic = False
                final_threshold = None

        if final_threshold is None and config.has_option(section, "threshold"):
            try:
                final_threshold = config.getfloat(section, "threshold")
            except ValueError:
                pass

    return final_semantic, final_threshold

# ------------------------------------------------------------------------------
# 3. CLI Commands
# ------------------------------------------------------------------------------
@app.command()
def test(
        target: Optional[str] = typer.Option(None, "--target", "-t", help="Specific target function. If omitted, runs ALL."),
        limit: int = typer.Option(10, "--limit", "-l", help="Number of test cases to run"),
        file: Optional[str] = typer.Option(None, "--file", "-f", help="Path to JSONL snapshot file"),
        golden_only: bool = typer.Option(False, "--golden-only", help="Run only verified Golden Data cases"),
        semantic: bool = typer.Option(False, "--semantic", "-s", help="Use LLM Judge"),
        threshold: Optional[float] = typer.Option(None, "--threshold", help="Use Vector Similarity check"),
):
    """
    [bold green]Run regression tests[/bold green]. Automatically reads config from vwtest.ini.
    """
    if target is None:
        target = "all"

    targets = []
    if target.lower() == "all":
        try:
            DataSourceFactory.get_source("db")
            targets = get_all_registered_functions()

            if not targets:
                console.print("[bold yellow]⚠️ No replay-enabled functions found.[/bold yellow]")
                raise typer.Exit(code=0)

            console.print(f"[bold cyan]🔍 Found {len(targets)} replay-enabled functions.[/bold cyan]\n")
        except Exception:
            typer.secho("❌ Failed to fetch function list from DB.", fg=typer.colors.RED)
            raise typer.Exit(code=1)
    else:
        targets = [target]

    source_type = "file" if file else "db"
    try:
        data_source = DataSourceFactory.get_source(source_type, path=file)
    except Exception as e:
        typer.secho(f"❌ Error initializing data source: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    total_stats = {"passed": 0, "failed": 0, "total": 0}
    failed_funcs = []

    try:
        for i, current_target in enumerate(targets):
            use_semantic, use_threshold = get_target_config(current_target, semantic, threshold)

            mode_str = "Exact Match"
            if use_semantic:
                mode_str = "[magenta]Semantic (LLM)[/magenta]"
            elif use_threshold is not None:
                mode_str = f"[blue]Similarity (>{use_threshold})[/blue]"

            console.print(Panel(f"[bold yellow]▶️ Running Test ({i+1}/{len(targets)}): {current_target}[/bold yellow]\n[dim]Mode: {mode_str}[/dim]", expand=False))

            try:
                runner = TestRunner(target_func_path=current_target, source=data_source)
                results = runner.run(
                    limit=limit,
                    golden_only=golden_only,
                    semantic_eval=use_semantic,
                    similarity_threshold=use_threshold
                )

                TestReporter.print_summary(current_target, results)

                if "error" not in results:
                    total_stats["passed"] += results.get("passed", 0)
                    total_stats["failed"] += results.get("failed", 0)
                    total_stats["total"] += results.get("total", 0)

                    if results.get("failed", 0) > 0:
                        failed_funcs.append(current_target)

            except Exception as e:
                typer.secho(f"⚠️ Error testing '{current_target}': {e}", fg=typer.colors.YELLOW)
                failed_funcs.append(current_target)

            print("\n")

        if len(targets) > 1:
            grid = Table.grid(expand=True)
            grid.add_column()
            grid.add_column(justify="right")
            grid.add_row("[bold]Grand Total Cases[/bold]", str(total_stats['total']))
            grid.add_row("[bold green]Total Passed[/bold green]", str(total_stats['passed']))
            grid.add_row("[bold red]Total Failed[/bold red]", str(total_stats['failed']))

            final_color = "red" if failed_funcs else "green"
            console.print(Panel(grid, title="[bold]🚀 Project-Wide Test Summary[/bold]", border_style=final_color))

            if failed_funcs:
                console.print("[bold red]❌ Functions with Failures:[/bold red]")
                for f in failed_funcs:
                    console.print(f"  - {f}")
                raise typer.Exit(code=1)

    finally:
        if get_batch_manager:
            try:
                bm = get_batch_manager()
                print()
                with Progress() as progress:
                    task = progress.add_task("[cyan]⏳ Flushing logs to Weaviate (Batch Wait)...", total=100)
                    for _ in range(100):
                        time.sleep(0.05)
                        progress.update(task, advance=1)
                bm.shutdown()
                typer.secho("✅ All logs flushed successfully!", fg=typer.colors.GREEN)
            except Exception:
                pass

@app.command()
def export(
        target: Optional[str] = typer.Option(None, "--target", "-t", help="Specific target function. If omitted, exports ALL."),
        output: str = typer.Option(..., "--output", "-o", help="Output JSONL file path"),
        limit: int = typer.Option(100, "--limit", "-l", help="Max records to export PER FUNCTION")
):
    if target is None:
        target = "all"

    try:
        source = DataSourceFactory.get_source("db")
    except Exception as e:
        typer.secho(f"❌ Error initializing DB: {e}", fg=typer.colors.RED)
        raise typer.Exit(code=1)

    targets = []
    if target.lower() == "all":
        targets = get_all_registered_functions()
        console.print(f"📦 Exporting logs for [bold]{len(targets)} functions[/bold] (replay enabled) to '{output}'...")
    else:
        targets = [target]
        console.print(f"📦 Exporting logs for '{target}'...")

    if not targets:
        typer.secho("❌ No functions found to export.", fg=typer.colors.RED)
        return

    total_exported = 0

    output_dir = os.path.dirname(output)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(output, "w", encoding="utf-8") as f:
        with Progress() as progress:
            main_task = progress.add_task("[green]Exporting...", total=len(targets))

            for func_name in targets:
                try:
                    logs = source.fetch_data(func_name, limit=limit)
                    if logs:
                        for log in logs:
                            f.write(json.dumps(log, ensure_ascii=False) + "\n")
                        total_exported += len(logs)
                except Exception as e:
                    pass

                progress.update(main_task, advance=1)

    if total_exported > 0:
        typer.secho(f"\n✅ Export Complete! Total {total_exported} records saved.", fg=typer.colors.GREEN)
    else:
        typer.secho("\n⚠️ No logs found matching criteria.", fg=typer.colors.YELLOW)

if __name__ == "__main__":
    app()