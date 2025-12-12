# syntaxmatrix/code_tools_registry.py
from typing import Dict, Any
from .agent_tools import CodeTool
from ..utils import (
    strip_python_dotenv, fix_predict_calls_records_arg, fix_values_sum_numeric_only_bug,
    fix_fstring_backslash_paths, ensure_os_import, fix_numeric_sum, ensure_os_import, 
    fix_numeric_sum, fix_concat_empty_list, fix_confusion_matrix_for_multilabel
)

def _wrap(fn):
    return lambda code, ctx: fn(code)

# 1) early sanitiser
EARLY_SANITIZERS = [ 
    CodeTool("strip_dotenv", "sanitize_early", _wrap(strip_python_dotenv), priority=0),
]

# 2) Domain and Plotting patches
DOMAIN_AND_PLOTTING_PATCHES = [
    
]

# 3) syntax/data fixers
SYNTAX_AND_REPAIR = [
    CodeTool("fix_predict_records", "syntax_fixes", _wrap(fix_predict_calls_records_arg), priority=10),
    CodeTool("fix_values_sum_bug", "syntax_fixes", _wrap(fix_values_sum_numeric_only_bug), priority=20),
    CodeTool("fix_fstring_paths", "syntax_fixes", _wrap(fix_fstring_backslash_paths), priority=30),
    CodeTool("ensure_os_import", "syntax_fixes", _wrap(ensure_os_import), priority=40),
    CodeTool("fix_numeric_sum", "syntax_fixes", _wrap(fix_numeric_sum), priority=50),
    CodeTool("fix_concat_empty_list", "syntax_fixes", _wrap(fix_concat_empty_list), priority=60),
    CodeTool("fix_cm_multilabel", "syntax_fixes", _wrap(fix_confusion_matrix_for_multilabel), priority=65),
]

# 4) final SANITIZERS catch-all
FINAL_SANITIZERS = [
    # CodeTool("repair_cell", "final_repair", _wrap(_smx_repair_python_cell), priority=999),
]