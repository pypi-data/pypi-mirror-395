"""Import validation for detecting hallucinated packages."""

from __future__ import annotations

import importlib.util
import sys
from typing import Optional, Set


# Standard library modules (Python 3.9+)
STDLIB_MODULES: Set[str] = set(sys.stdlib_module_names) if hasattr(sys, 'stdlib_module_names') else {
    'abc', 'argparse', 'ast', 'asyncio', 'base64', 'collections', 'configparser',
    'contextlib', 'copy', 'csv', 'dataclasses', 'datetime', 'decimal', 'difflib',
    'email', 'enum', 'functools', 'glob', 'hashlib', 'html', 'http', 'importlib',
    'inspect', 'io', 'itertools', 'json', 'logging', 'math', 'multiprocessing',
    'operator', 'os', 'pathlib', 'pickle', 'platform', 'pprint', 're', 'shutil',
    'signal', 'socket', 'sqlite3', 'string', 'subprocess', 'sys', 'tempfile',
    'textwrap', 'threading', 'time', 'traceback', 'types', 'typing', 'unittest',
    'urllib', 'uuid', 'warnings', 'weakref', 'xml', 'zipfile',
}


def module_exists(module_name: str) -> bool:
    """Check if a module/package exists in the Python environment."""
    # Check stdlib first (fast path)
    base = module_name.split('.')[0]
    if base in STDLIB_MODULES:
        return True
    
    try:
        spec = importlib.util.find_spec(module_name)
        return spec is not None
    except (ModuleNotFoundError, ValueError, ImportError, AttributeError):
        return False


def validate_import(module_name: str, name: Optional[str] = None) -> Optional[str]:
    """
    Validate that an import is correct.
    
    Returns an error message if the import is invalid, None otherwise.
    """
    # Check known hallucinations first
    if name:
        hallucination_msg = check_known_hallucination(module_name, name)
        if hallucination_msg:
            return hallucination_msg
    
    # Check if base module exists
    base_module = module_name.split('.')[0]
    if not module_exists(base_module):
        return f"Module '{module_name}' does not exist"
    
    return None


# Common hallucinated imports (known bad patterns from AI)
# Format: (module, name) -> error message (None means valid)
KNOWN_HALLUCINATIONS = {
    # === FastAPI / Starlette confusion ===
    ('requests', 'JSONResponse'): "JSONResponse is from starlette.responses or fastapi.responses, not requests",
    ('requests', 'Response'): None,  # Valid - requests has Response
    ('flask', 'Query'): "Query is from fastapi, not flask",
    ('flask', 'Depends'): "Depends is from fastapi, not flask",
    ('flask', 'HTTPException'): None,  # Valid - flask.exceptions.HTTPException exists
    ('django', 'FastAPI'): "FastAPI is its own package, not part of django",
    ('django', 'APIRouter'): "APIRouter is from fastapi, not django",
    
    # === typing module confusion ===
    ('typing', 'Required'): "Required is from typing_extensions (Python <3.11)",
    ('typing', 'NotRequired'): "NotRequired is from typing_extensions (Python <3.11)",
    ('typing', 'Self'): "Self is from typing_extensions (Python <3.11)",
    ('typing', 'TypeGuard'): "TypeGuard is in typing (3.10+) or typing_extensions",
    ('typing', 'ParamSpec'): None,  # Valid in 3.10+
    
    # === dataclasses confusion ===
    ('collections', 'dataclass'): "dataclass is from dataclasses, not collections",
    ('typing', 'dataclass'): "dataclass is from dataclasses, not typing",
    ('attrs', 'dataclass'): "dataclass is from dataclasses; attrs uses @attr.s or @define",
    
    # === pydantic confusion ===
    ('dataclasses', 'BaseModel'): "BaseModel is from pydantic, not dataclasses",
    ('typing', 'BaseModel'): "BaseModel is from pydantic, not typing",
    ('dataclasses', 'Field'): None,  # Valid - dataclasses has field()
    
    # === async confusion ===
    ('asyncio', 'aiohttp'): "aiohttp is its own package, not part of asyncio",
    ('asyncio', 'httpx'): "httpx is its own package, not part of asyncio",
    ('async', 'await'): "async/await are keywords, not importable",
    
    # === os/pathlib confusion ===
    ('os', 'makedirectory'): "Use os.makedirs() not os.makedirectory()",
    ('os', 'makedir'): "Use os.mkdir() or os.makedirs(), not os.makedir()",
    ('os.path', 'Path'): "Path is from pathlib, not os.path",
    ('pathlib', 'mkdirs'): "Use Path.mkdir(parents=True), not mkdirs()",
    
    # === json confusion ===
    ('json', 'JSONEncoder'): None,  # Valid
    ('json', 'parse'): "Use json.loads() not json.parse() (JavaScript pattern)",
    ('json', 'stringify'): "Use json.dumps() not json.stringify() (JavaScript pattern)",
    
    # === common non-existent packages ===
    ('utils', None): "Generic 'utils' is not a standard package - likely meant local module",
    ('helpers', None): "Generic 'helpers' is not a standard package - likely meant local module",
    ('common', None): "Generic 'common' is not a standard package - likely meant local module",
    
    # === pytest confusion ===
    ('unittest', 'fixture'): "fixture is from pytest, not unittest",
    ('unittest', 'mark'): "mark is from pytest, not unittest",
    ('pytest', 'TestCase'): "TestCase is from unittest, not pytest",
    
    # === requests/urllib confusion ===  
    ('urllib', 'get'): "Use urllib.request.urlopen() or requests.get(), not urllib.get()",
    ('urllib', 'post'): "Use urllib.request.urlopen() or requests.post(), not urllib.post()",
    ('http', 'get'): "Use http.client or requests for HTTP requests",
    
    # === logging confusion ===
    ('logging', 'log'): None,  # Valid - logging.log() exists
    ('logger', None): "'logger' is not a module - use 'logging'",
    
    # === SQLAlchemy confusion ===
    ('sqlalchemy', 'Model'): "Model is from flask_sqlalchemy, SQLAlchemy uses declarative_base()",
    ('sqlalchemy', 'db'): "db is typically a Flask-SQLAlchemy instance, not from sqlalchemy",
}


def check_known_hallucination(module: str, name: Optional[str]) -> Optional[str]:
    """Check if this is a known hallucinated import pattern."""
    # Check exact match
    result = KNOWN_HALLUCINATIONS.get((module, name))
    if result is not None:
        return result
    
    # Check module-only patterns (name=None in dict)
    module_only = KNOWN_HALLUCINATIONS.get((module, None))
    if module_only is not None:
        return module_only
    
    return None


def is_likely_hallucinated_package(module_name: str) -> Optional[str]:
    """
    Check if a module name looks like a hallucinated package.
    
    Returns error message if likely hallucinated, None otherwise.
    """
    base = module_name.split('.')[0]
    
    # Check if it exists
    if module_exists(module_name):
        return None
    
    # Common AI hallucination patterns
    hallucinated_patterns = {
        'utils': "Module 'utils' does not exist - did you mean a local module?",
        'helpers': "Module 'helpers' does not exist - did you mean a local module?",
        'common': "Module 'common' does not exist - did you mean a local module?",
        'config': "Module 'config' does not exist - did you mean a local module?",
        'constants': "Module 'constants' does not exist - did you mean a local module?",
        'models': "Module 'models' does not exist - did you mean a local module?",
        'schemas': "Module 'schemas' does not exist - did you mean a local module?",
        'services': "Module 'services' does not exist - did you mean a local module?",
    }
    
    if base in hallucinated_patterns:
        return hallucinated_patterns[base]
    
    return f"Module '{module_name}' does not exist - possible hallucination"


# Common hallucinated method calls
# Format: method_name -> (correct_method, context_hint)
HALLUCINATED_METHODS = {
    # String methods
    'titlecase': ('title', "str.title()"),
    'uppercase': ('upper', "str.upper()"),
    'lowercase': ('lower', "str.lower()"),
    'trimStart': ('lstrip', "str.lstrip() - JavaScript pattern"),
    'trimEnd': ('rstrip', "str.rstrip() - JavaScript pattern"),
    'trim': ('strip', "str.strip() - JavaScript pattern"),
    'charAt': ('[]', "Use indexing s[i] not s.charAt(i) - JavaScript pattern"),
    'indexOf': ('find', "str.find() or 'in' operator - JavaScript pattern"),
    'lastIndexOf': ('rfind', "str.rfind() - JavaScript pattern"),
    'substring': ('[]', "Use slicing s[start:end] - JavaScript pattern"),
    'substr': ('[]', "Use slicing s[start:start+length] - JavaScript pattern"),
    'includes': ('in', "Use 'in' operator - JavaScript pattern"),
    'repeat': ('*', "Use s * n for repetition - JavaScript pattern"),
    'padStart': ('rjust', "str.rjust() or str.zfill() - JavaScript pattern"),
    'padEnd': ('ljust', "str.ljust() - JavaScript pattern"),
    'toUpperCase': ('upper', "str.upper() - JavaScript pattern"),
    'toLowerCase': ('lower', "str.lower() - JavaScript pattern"),
    'toString': ('str', "Use str() builtin - JavaScript pattern"),
    
    # List/Array methods
    'push': ('append', "list.append() - JavaScript pattern"),
    'unshift': ('insert', "list.insert(0, x) - JavaScript pattern"),
    'shift': ('pop', "list.pop(0) - JavaScript pattern"),
    'splice': ('[]', "Use slicing/del for splice - JavaScript pattern"),
    'slice': ('[]', "Use slicing list[start:end] - JavaScript pattern"),
    'concat': ('+', "Use + or extend() - JavaScript pattern"),
    'forEach': ('for', "Use for loop - JavaScript pattern"),
    'map': ('list comprehension', "Use [f(x) for x in list] or map()"),
    'filter': ('list comprehension', "Use [x for x in list if cond] or filter()"),
    'reduce': ('functools.reduce', "Use functools.reduce()"),
    'find': ('next', "Use next(x for x in list if cond) or list comprehension"),
    'findIndex': ('next', "Use next(i for i,x in enumerate(list) if cond)"),
    'some': ('any', "Use any(cond for x in list)"),
    'every': ('all', "Use all(cond for x in list)"),
    'flat': ('itertools.chain', "Use itertools.chain.from_iterable()"),
    'flatMap': ('itertools.chain', "Use chain.from_iterable(f(x) for x in list)"),
    'length': ('len', "Use len(list) not list.length - JavaScript pattern"),
    'size': ('len', "Use len(obj) not obj.size()"),
    
    # Dict methods
    'hasOwnProperty': ('in', "Use 'key in dict' - JavaScript pattern"),
    'keys': (None, None),  # Valid in Python
    'values': (None, None),  # Valid in Python
    'entries': ('items', "dict.items() - JavaScript pattern"),
    'assign': ('update', "dict.update() or {**d1, **d2} - JavaScript pattern"),
    'freeze': (None, "Python dicts are mutable; use types.MappingProxyType"),
    
    # Type checking
    'typeof': ('type', "Use type() or isinstance() - JavaScript pattern"),
    'instanceof': ('isinstance', "Use isinstance() - JavaScript pattern"),
    
    # Other common mistakes
    'len': (None, None),  # Valid - but common mistake is .len() instead of len()
    'print': (None, None),  # Valid
    'sorted': (None, None),  # Valid
    'reversed': (None, None),  # Valid
}


def check_hallucinated_method(method_name: str) -> Optional[str]:
    """
    Check if a method name is a known hallucination.
    
    Returns error message with correction if hallucinated, None otherwise.
    """
    if method_name not in HALLUCINATED_METHODS:
        return None
    
    correct, hint = HALLUCINATED_METHODS[method_name]
    if correct is None:
        return None  # Method is valid
    
    return f"'{method_name}' is not a Python method. {hint}"
