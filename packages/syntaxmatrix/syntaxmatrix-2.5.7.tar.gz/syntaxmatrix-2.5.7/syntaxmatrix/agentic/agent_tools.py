# syntaxmatrix/agent_tools.py
from dataclasses import dataclass
from typing import Callable, Optional, Dict, Any, List, Literal

Phase = Literal["sanitize_early", "domain_patches", "syntax_fixes", "final_repair"]

@dataclass
class CodeTool:
    name: str
    phase: Phase
    fn: Callable[[str, Dict[str, Any]], str]
    when: Optional[Callable[[str, Dict[str, Any]], bool]] = None
    priority: int = 100  # lower runs earlier within the phase

class ToolRunner:
    def __init__(self, tools: List[CodeTool]):
        # stable order: phase → priority → name
        self.tools = sorted(tools, key=lambda t: (t.phase, t.priority, t.name))

    def run(self, code: str, ctx: Dict[str, Any]) -> str:
        for t in self.tools:
            if t.when is None or t.when(code, ctx):
                code = t.fn(code, ctx)
        return code
