import importlib
import sys
import os
import ast
import configparser
from typing import Callable, Optional, List


def find_project_root() -> str:
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


def get_search_paths() -> List[str]:
    project_root = find_project_root()
    paths = [project_root, os.getcwd()]

    src_path = os.path.join(project_root, "src")
    if os.path.exists(src_path):
        paths.append(src_path)

    ini_path = os.path.join(project_root, "vwtest.ini")

    if os.path.exists(ini_path):
        try:
            config = configparser.ConfigParser()
            config.read(ini_path, encoding='utf-8')

            if config.has_option("vectorcheck", "python_paths"):
                paths_str = config.get("vectorcheck", "python_paths")
                for p in paths_str.split(','):
                    if p.strip():
                        abs_p = os.path.abspath(os.path.join(project_root, p.strip()))
                        paths.append(abs_p)
        except Exception as e:
            print(f"[⚠️ Warning] Failed to read vwtest.ini: {e}")

    unique_paths = list(set(paths))
    return unique_paths


def find_module_for_function(target_func_name: str) -> Optional[str]:
    """
    Insect the entire project and find the module_path for the function.
    """
    search_paths = get_search_paths()
    print(f"[🔍 Auto-Discovery] Searching for function '{target_func_name}' in project...")

    for search_root in search_paths:
        if not os.path.exists(search_root):
            continue

        for root, dirs, files in os.walk(search_root):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d != '__pycache__' and 'venv' not in d]

            for file in files:
                if not file.endswith(".py"):
                    continue

                file_path = os.path.join(root, file)

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                        content = f.read()
                        if f"def {target_func_name}" not in content:
                            continue

                        tree = ast.parse(content)
                        for node in ast.walk(tree):
                            if isinstance(node, ast.FunctionDef) and node.name == target_func_name:
                                try:
                                    rel_path = os.path.relpath(file_path, search_root)
                                except ValueError:
                                    rel_path = os.path.relpath(file_path, os.getcwd())

                                module_name = rel_path.replace(os.path.sep, ".").rstrip(".py")

                                if module_name.startswith("src."):
                                    module_name = module_name[4:]

                                if module_name.endswith(".__init__"):
                                    module_name = module_name[:-9]

                                print(f"[✅ Found] Function '{target_func_name}' found in '{module_name}'")
                                return module_name
                except Exception:
                    continue

    print(f"[❌ Not Found] Could not find function '{target_func_name}' in search paths.")
    return None


class FunctionLoader:
    @staticmethod
    def load_function(func_path: str) -> Callable:
        try:
            search_paths = get_search_paths()
            for path in search_paths:
                if path not in sys.path:
                    sys.path.insert(0, path)

            if '.' in func_path:
                module_name, func_name = func_path.rsplit('.', 1)
            else:
                raise ValueError(f"Invalid function path format: {func_path}")

            if module_name == "__main__":
                discovered = find_module_for_function(func_name)
                if discovered:
                    module_name = discovered
                else:
                    raise ImportError(
                        f"Could not automatically find module for '{func_name}'. Please regenerate data using 'python -m ...'.")

            module = importlib.import_module(module_name)
            func = getattr(module, func_name)
            return func

        except Exception as e:
            raise RuntimeError(f"Failed to load function '{func_path}': {e}")
