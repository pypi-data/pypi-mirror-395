# veriskgo/cli_instrument.py

import os
import ast

INSTRUMENT_IMPORT = "from veriskgo import track_function"


def _lazy_import_astor():
    """
    Lazy import astor only when required.
    Prevents ModuleNotFoundError when user doesn't run `instrument`.
    """
    try:
        import astor
        return astor
    except ImportError:
        print("\n❌ Missing optional dependency: 'astor'\n")
        print("The `instrument` command requires the `astor` package.")
        print("Install it manually:\n")
        print("    pip install astor\n")
        return None


class Instrumentor(ast.NodeTransformer):
    def __init__(self, skip_private=True, exclude=None):
        self.skip_private = skip_private
        self.exclude = exclude or []

    def _process_function(self, node):
        # Exclusion logic
        if node.name in self.exclude:
            return node

        # Private filter
        if self.skip_private and node.name.startswith("_"):
            return node

        # Already decorated?
        already = any(
            (isinstance(dec, ast.Call) and getattr(dec.func, "id", "") == "track_function") or
            (isinstance(dec, ast.Name) and dec.id == "track_function")
            for dec in node.decorator_list
        )

        if not already:
            decorator = ast.Call(
                func=ast.Name(id="track_function", ctx=ast.Load()),
                args=[],
                keywords=[]
            )
            node.decorator_list.insert(0, decorator)

        return node

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        return self._process_function(node)

    def visit_AsyncFunctionDef(self, node):
        self.generic_visit(node)
        return self._process_function(node)


def ensure_import_exists(code: str) -> str:
    """Insert track_function import if missing."""
    if INSTRUMENT_IMPORT in code:
        return code

    lines = code.split("\n")
    insert_pos = 0

    while insert_pos < len(lines) and (
        lines[insert_pos].startswith("#!") or
        "coding" in lines[insert_pos]
    ):
        insert_pos += 1

    lines.insert(insert_pos, INSTRUMENT_IMPORT)
    return "\n".join(lines)


def instrument_file(path: str, skip_private=True, exclude=None, dry_run=False):
    # Lazy-load astor only **inside** this function
    astor = _lazy_import_astor()
    if astor is None:
        return  # error already printed

    try:
        with open(path, "r", encoding="utf-8") as f:
            original = f.read()
    except Exception as e:
        print(f"❌ Cannot read {path}: {e}")
        return

    try:
        tree = ast.parse(original)
    except SyntaxError:
        print(f"❌ Skipping {path} (syntax error)")
        return

    transformer = Instrumentor(skip_private=skip_private, exclude=exclude)
    modified_tree = transformer.visit(tree)
    ast.fix_missing_locations(modified_tree)

    modified_code = astor.to_source(modified_tree)
    modified_code = ensure_import_exists(modified_code)

    if modified_code == original:
        print(f"✓ {path} (no changes needed)")
        return

    if dry_run:
        print(f"DRY RUN → Would update: {path}")
        return

    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(modified_code)
        print(f"✔ Instrumented: {path}")
    except Exception as e:
        print(f"❌ Failed to write {path}: {e}")


def instrument_directory(root=".", skip_private=True, exclude=None, dry_run=False):
    """Instrument all .py files recursively."""
    for base, dirs, files in os.walk(root):
        dirs[:] = [
            d for d in dirs
            if d not in (".venv", "venv", "__pycache__", "site-packages")
        ]

        for file in files:
            if file.endswith(".py"):
                full = os.path.join(base, file)
                instrument_file(full, skip_private, exclude, dry_run)


def instrument_project(path=".", skip_private=True, exclude=None, dry_run=False):
    """Entry point — determines file vs directory."""
    if not os.path.exists(path):
        print(f"❌ Path not found: {path}")
        return

    if os.path.isfile(path):
        instrument_file(path, skip_private, exclude, dry_run)
    else:
        instrument_directory(path, skip_private, exclude, dry_run)

    print("[veriskgo] Instrumentation complete.")
