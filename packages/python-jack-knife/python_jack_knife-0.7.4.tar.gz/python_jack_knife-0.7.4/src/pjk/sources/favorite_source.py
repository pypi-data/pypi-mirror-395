from pjk.usage import Usage, ParsedToken
from pjk.components import Source
from pathlib import Path
from typing import Dict

MACRO_FILE = '~/.pjk/macros.txt'

def read_macros(file_name: str = MACRO_FILE) -> Dict[str, str]:
    out: Dict[str, str] = {}
    path = Path(file_name).expanduser()
    with path.open(encoding="utf-8") as f:
        for raw in f:
            line = raw.split("#", 1)[0].strip()
            if not line or ":" not in line:
                continue
            key, val = line.split(":", 1)
            out[key.strip()] = val.strip()
    return out

class MacroSource(Source):
    @classmethod
    def usage(cls):
        u = Usage(
            name='macros',
            desc=f"Source to list the macro expressions stored in {MACRO_FILE}.\n"
                  "A specific macro is referenced using 'm:<instance>, e.g. pjk m:hw -",
            component_class=cls
    	)
        return u

    def __init__(self, ptok: ParsedToken, usage: Usage):
        pass

    # only the instance=+ case comes here.  See parser
    def __iter__(self):
        macros = read_macros()
        for k, v in macros.items():
            yield {k: v}

    def deep_copy(self):
        return None

    def close(self):
        pass
