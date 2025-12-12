from __future__ import annotations

import re

# OSC (Operating System Command) sequences such as hyperlinks: ESC ] ... ( ESC \ or BEL )
OSC_SEQUENCE_RE = re.compile(r"\x1B\][0-?]*.*?(?:\x1B\\|\x07)")
