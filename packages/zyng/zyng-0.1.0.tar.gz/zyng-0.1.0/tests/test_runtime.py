from zyng.core import ZyngRuntime, ZyngContext, Show, Let


def test_let_and_show_with_time_now(capsys):
    ctx = ZyngContext()
    runtime = ZyngRuntime(ctx)

    runtime.execute(Let(name="user", value="Alice"))
    runtime.execute(Show(content="Hello, {user}!", time="now"))

    captured = capsys.readouterr()
    assert "[now] Hello, Alice!" in captured.out
    # ログにも残っていることを軽く確認
    assert "[now] Hello, Alice!" in ctx.logs
