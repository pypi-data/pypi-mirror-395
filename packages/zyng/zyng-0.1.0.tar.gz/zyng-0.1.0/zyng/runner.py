from __future__ import annotations

import sys
from pathlib import Path
import re
from typing import List, Optional

from .core import ZyngRuntime, Show, Let, Statement


# --- 1. 行 → Statement の簡易パーサ（v0.0.x 相当） --------------------------


# show "Hello world" :::now
SHOW_RE = re.compile(
    r'^show\s+"(?P<content>.*?)"(?:\s+:::(?P<time>.+))?\s*$'
)

# let user = "Alice"
LET_RE = re.compile(
    r'^let\s+(?P<name>[a-zA-Z_][a-zA-Z0-9_]*)\s*=\s*"(?P<value>.*?)"\s*$'
)


def parse_line_to_statement(line: str) -> Optional[Statement]:
    """
    1 行の Zyng コードを Statement に変換する簡易パーサ。

    現時点では v0.0.x 相当の「雑パース」：
      - show "..." :::now / :::yest / :::tomo / :::at:"..."
      - let name = "value"
    だけをサポートする。

    Known limitation:
      - 文字列中に " や ::: が出てきた場合の扱いはまだ不完全。
        v0.1 で Lexer を導入して改善する予定。
    """
    stripped = line.strip()
    if not stripped:
        return None

    # show 文
    m = SHOW_RE.match(stripped)
    if m:
        content = m.group("content")
        time_raw = m.group("time")
        time = time_raw.strip() if time_raw else None
        return Show(content=content, time=time)

    # let 文
    m = LET_RE.match(stripped)
    if m:
        name = m.group("name")
        value = m.group("value")
        return Let(name=name, value=value)

    # それ以外の行は、現時点では無視
    return None


# --- 2. Markdown から ```zyng ブロックを抜き出す ---------------------------


def iter_zyng_lines(path: Path):
    """
    Markdown ファイルから ```zyng ～ ``` の間の行だけを順に返すジェネレータ。
    インデントや前後のテキストはそのまま無視する。
    """
    in_block = False

    with path.open(encoding="utf-8") as f:
        for raw in f:
            line = raw.rstrip("\n")
            stripped = line.lstrip()

            if not in_block:
                # ブロック開始判定: ```zyng で始まる行
                if stripped.startswith("```zyng"):
                    in_block = True
                continue

            # in_block == True のとき
            if stripped.startswith("```"):
                # ブロック終了
                in_block = False
                continue

            # Zyng コード行として返す
            yield line


# --- 3. エントリポイント -----------------------------------------------------


def main(argv: Optional[list[str]] = None) -> None:
    if argv is None:
        argv = sys.argv[1:]

    if not argv:
        print("Usage: python -m zyng.runner <markdown-file>", file=sys.stderr)
        raise SystemExit(1)

    path = Path(argv[0])
    if not path.exists():
        print(f"File not found: {path}", file=sys.stderr)
        raise SystemExit(1)

    runtime = ZyngRuntime()
    statements: List[Statement] = []

    # 1. Markdown から zyng 行を抜く
    for line in iter_zyng_lines(path):
        stmt = parse_line_to_statement(line)
        if stmt is not None:
            statements.append(stmt)

    # 2. AST を Context 上で実行
    for stmt in statements:
        runtime.execute(stmt)


if __name__ == "__main__":
    main()
