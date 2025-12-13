"""
Simple importer for `.pyowo` and `.pyowopp` files.

Usage: place this file on PYTHONPATH (same dir as `pythowopp.py`) or import it from your program.
Then `import foo` will search for `foo.pyowo` or `foo.pyowopp` on sys.path and execute it with the pythowopp interpreter.
Top-level variables (numbers, strings, lists, and functions) are exposed as Python attributes.
"""
import importlib.abc
import importlib.util
import sys
import os
import types

import pythowopp as pythowo


class PyowoLoader(importlib.abc.Loader):
    def __init__(self, path):
        self.path = path

    def create_module(self, spec):
        return None

    def exec_module(self, module):
        with open(self.path, "r", encoding="utf-8") as f:
            src = f.read()

        # run the .pyowo source in a fresh symbol table that inherits builtins
        st = pythowo.SymbolTable(parent=pythowo.global_symbol_table)
        _, error = pythowo.run(self.path, src, symbol_table=st)
        # treat empty files as valid no-ops (pyowo parser may report syntax errors on empty files)
        if error:
            if src.strip() == "":
                # leave symbol table empty
                pass
            else:
                raise ImportError(f"error importing {self.path}: {error.as_string()}")

        def to_python(val):
            if val is None:
                return None
            if isinstance(val, pythowo.Number):
                return val.value
            if isinstance(val, pythowo.String):
                return val.value
            if isinstance(val, pythowo.List):
                return [to_python(e) for e in val.elements]
            if isinstance(val, pythowo.BaseFunction):
                def fn(*args):
                    # convert python args -> pythowo Values (limited support)
                    vals = []
                    for a in args:
                        if isinstance(a, (int, float)):
                            vals.append(pythowo.Number(a))
                        elif isinstance(a, str):
                            vals.append(pythowo.String(a))
                        elif isinstance(a, list):
                            # assume list of primitives
                            elems = []
                            for x in a:
                                if isinstance(x, (int, float)):
                                    elems.append(pythowo.Number(x))
                                elif isinstance(x, str):
                                    elems.append(pythowo.String(x))
                                else:
                                    raise TypeError("Unsupported list element type for .pyowo call")
                            vals.append(pythowo.List(elems))
                        else:
                            raise TypeError("Unsupported arg type for .pyowo call")
                    res = val.execute(vals)
                    if res.error:
                        raise RuntimeError(res.error.as_string())
                    return to_python(res.value)
                return fn
            # fallback: return None for unsupported types
            return None

        # export the top-level symbols from the symbol table as module attributes
        for name, value in st.symbols.items():
            try:
                setattr(module, name, to_python(value))
            except Exception:
                # skip values we cannot convert
                setattr(module, name, None)

        module.__file__ = self.path
        module.__loader__ = self


EXTS = [".pyowo", ".pyowopp"]


class PyowoFinder(importlib.abc.MetaPathFinder):
    def find_spec(self, fullname, path, target=None):
        name = fullname.rpartition(".")[-1]
        search_paths = path or sys.path
        for entry in search_paths:
            # if name already has a supported extension, try it directly
            for ext in EXTS:
                if name.endswith(ext):
                    candidate = os.path.join(entry, name)
                    if os.path.isfile(candidate):
                        loader = PyowoLoader(candidate)
                        spec = importlib.util.spec_from_loader(fullname, loader)
                        spec.origin = candidate
                        return spec

            # otherwise try with each supported extension
            for ext in EXTS:
                candidate = os.path.join(entry, name + ext)
                if os.path.isfile(candidate):
                    loader = PyowoLoader(candidate)
                    spec = importlib.util.spec_from_loader(fullname, loader)
                    spec.origin = candidate
                    return spec
        return None


# register importer at front of meta_path if not already present
_finder = PyowoFinder()
if not any(isinstance(f, PyowoFinder) for f in sys.meta_path):
    sys.meta_path.insert(0, _finder)
