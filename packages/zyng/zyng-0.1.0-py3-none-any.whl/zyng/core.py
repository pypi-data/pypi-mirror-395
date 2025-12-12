from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import re


# --- 1. Context (メモリ/状態) -------------------------------------------------


class ZyngContext:
    """
    Zyng 実行時の状態（変数・ログなど）を保持するコンテキスト。

    v0.1 以降で let/read/use などの拡張にもそのまま使える前提で設計しておく。
    """

    def __init__(self) -> None:
        # 変数テーブル（将来 Expr を入れることも想定して Any にしておく）
        self.variables: Dict[str, Any] = {}
        # 実行ログ（デバッグ用）。本番では別のシンクに流すかもしれない。
        self.logs: List[str] = []

    def set_var(self, name: str, value: Any) -> None:
        self.variables[name] = value

    def get_var(self, name: str) -> Any:
        """
        v0.0.x では未定義変数は None を返す。

        将来的には KeyError を投げるモード／デフォルト値を返すモードなどを検討する。
        """
        return self.variables.get(name)

    def log(self, message: str) -> None:
        self.logs.append(message)


# --- 2. AST (命令の定義) ------------------------------------------------------


@dataclass
class Statement:
    """
    すべての Zyng 文の基底クラス。
    いまは具象クラスとして Show / Let だけを持つ。
    """
    pass


@dataclass
class Show(Statement):
    """
    メッセージを出力する文。

    content: 出力する本文（{var} 埋め込みを含む生文字列）
    time: "now" / "yest" / "tomo" / 'at:"2025-12-03T21:00:00+09:00"' など
    meta: その他のメタ情報（role/kind/use などを将来的に入れる余地）
    """
    content: str
    time: Optional[str] = None
    meta: Dict[str, str] = field(default_factory=dict)


@dataclass
class Let(Statement):
    """
    変数に値を束縛する文。

    v0.1 では value を「ただの文字列」として扱う。
    将来、式（Expr: Literal / Var / Concat ...）として拡張する余地を残しておく。
    """
    name: str
    value: str  # TODO(v>0.1): Expr 型に拡張する


# 将来的に Use / Write などを足すとしたら、ここに dataclass を追加していく。


# --- 3. Runtime（実行機構） ---------------------------------------------------


class ZyngRuntime:
    """
    AST（Statement）のリストを Context 上で実行する Runtime。

    ここでは「行即時実行」ではなく
        1. 行をパースして Statement を作る
        2. Statement を Context 付きで execute する
    という二段構成を前提に設計している。
    """

    def __init__(self, context: Optional[ZyngContext] = None) -> None:
        self.context = context or ZyngContext()

    # --- パブリック API -------------------------------------------------------

    def execute(self, stmt: Statement) -> None:
        """
        単一の Statement を Context 上で実行する。
        """
        if isinstance(stmt, Show):
            self._exec_show(stmt)
        elif isinstance(stmt, Let):
            self._exec_let(stmt)
        else:
            # 未対応の Statement は将来ここでエラー or 無視を決める
            raise TypeError(f"Unsupported statement type: {type(stmt).__name__}")

    # --- 各 Statement ごとの実行ロジック -------------------------------------

    def _exec_show(self, stmt: Show) -> None:
        # 1. 変数埋め込みを解決
        resolved = self._resolve_vars(stmt.content)

        # 2. time メタからプレフィックスを決める
        prefix = self._format_time_prefix(stmt.time)

        # 3. 出力（いまは stdout + log に書くだけ）
        message = f"{prefix}{resolved}"
        print(message)
        self.context.log(message)

    def _exec_let(self, stmt: Let) -> None:
        # v0.1 では単純に文字列をそのまま束縛
        # 将来、value が Expr になったときに評価ロジックをここに書く。
        value = self._resolve_vars(stmt.value)
        self.context.set_var(stmt.name, value)

    # --- 補助メソッド --------------------------------------------------------

    def _resolve_vars(self, text: str) -> str:
        """
        プレーンな文字列中の {var_name} を Context.variables から展開する。

        - 未定義変数はそのまま {var_name} を残す（v0.0.x の方針）。
        - ルールは「英字+数字+アンダースコアから始まる識別子」だけを対象にする。
        """
        pattern = re.compile(r"{([a-zA-Z_][a-zA-Z0-9_]*)}")

        def replacer(match: re.Match[str]) -> str:
            name = match.group(1)
            value = self.context.get_var(name)
            if value is None:
                # 未定義の場合はそのまま残す
                return match.group(0)
            return str(value)

        return pattern.sub(replacer, text)

    @staticmethod
    def _format_time_prefix(time_meta: Optional[str]) -> str:
        """
        time メタから `[now] ` のようなプレフィックス文字列を生成する。
        time_meta は "now" / "yest" / "tomo" / 'at:"...ISO8601..."' 等を想定。
        """
        if time_meta is None:
            return ""

        # 代表的なショートカット
        if time_meta in ("now", "yest", "tomo"):
            return f"[{time_meta}] "

        # at:"2025-12-03T21:00:00+09:00" のような raw 表現はそのまま包む
        return f"[{time_meta}] "


# --- 4. 簡易テスト（Lexer/Parser 未実装でも Runtime を試せるように） -------


if __name__ == "__main__":
    runtime = ZyngRuntime()

    mock_ast_list: List[Statement] = [
        Let(name="user", value="Alice"),
        Show(content="Hello, {user}!", time="now"),
        Let(name="weather", value="Sunny"),
        Show(content="It is {weather} today."),
        Show(content="Exact time example", time='at:"2025-12-03T21:00:00+09:00"'),
    ]

    print("--- Running Core Skeleton ---")
    for stmt in mock_ast_list:
        runtime.execute(stmt)
    print("--- Done ---")
