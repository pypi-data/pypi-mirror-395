# src/vectorcheck/runner.py
from typing import Dict, Any, Optional
import logging

# [FIX 1] 탐색 함수 직접 임포트
from .loader import find_module_for_function, get_search_paths
import sys

try:
    from vectorwave.utils.replayer import VectorWaveReplayer
    from vectorwave.utils.replayer_semantic import SemanticReplayer
except ImportError:
    VectorWaveReplayer = None
    SemanticReplayer = None

class TestRunner:
    def __init__(self, target_func_path: str, source=None):
        self.original_path = target_func_path

        self.target_func_path = self._resolve_real_path(target_func_path)

        self._register_search_paths()

        if not VectorWaveReplayer:
            raise RuntimeError("VectorWave library not found.")

    def _register_search_paths(self):
        """
        Add project paths that loader found to sys.path
        """
        search_paths = get_search_paths()
        for path in search_paths:
            if path not in sys.path:
                sys.path.insert(0, path)

    def _resolve_real_path(self, func_path: str) -> str:
        if "." not in func_path:
            return func_path

        module_name, func_name = func_path.rsplit(".", 1)

        if module_name == "__main__":
            print(f"[Runner] 🔍 Resolving path for local execution: {func_path}")
            real_module = find_module_for_function(func_name)

            if real_module:
                new_path = f"{real_module}.{func_name}"
                print(f"[Runner] ✅ Path remapped: {func_path} -> {new_path}")
                return new_path
            else:
                print(f"[Runner] ⚠️ Could not find source file for {func_path}. Execution may fail.")

        return func_path

    def run(self, limit: int, golden_only: bool = False, semantic_eval: bool = False, similarity_threshold: Optional[float] = None) -> Dict[str, Any]:

        logging.getLogger("vectorwave").setLevel(logging.WARNING)

        if golden_only:
            print("⚠️ Warning: 'golden-only' filter is not fully supported in this version of VectorWave Core."
                  " Running with priority fetch.")

        if semantic_eval:
            return self._run_llm_judge(limit)
        elif similarity_threshold is not None:
            return self._run_vector_similarity(limit, similarity_threshold)
        else:
            return self._run_exact_match(limit)

    def _run_exact_match(self, limit: int) -> Dict[str, Any]:
        print(f"🚀 Running [Exact Match] Replay...")
        replayer = VectorWaveReplayer()

        return replayer.replay(
            function_full_name=self.target_func_path,
            limit=limit
        )

    def _run_vector_similarity(self, limit: int, threshold: float) -> Dict[str, Any]:
        if not SemanticReplayer:
            raise RuntimeError("SemanticReplayer needed for vector check.")

        print(f"🚀 Running [Vector Similarity] Replay (Threshold: {threshold})...")
        replayer = SemanticReplayer()

        return replayer.replay(
            function_full_name=self.target_func_path,
            limit=limit,
            semantic_eval=False,
            similarity_threshold=threshold
        )

    def _run_llm_judge(self, limit: int) -> Dict[str, Any]:
        if not SemanticReplayer:
            raise RuntimeError("SemanticReplayer needed for LLM judge.")

        print(f"🚀 Running [LLM Judge] Replay (AI Evaluation)...")
        replayer = SemanticReplayer()

        return replayer.replay(
            function_full_name=self.target_func_path,
            limit=limit,
            semantic_eval=True,
            similarity_threshold=None
        )