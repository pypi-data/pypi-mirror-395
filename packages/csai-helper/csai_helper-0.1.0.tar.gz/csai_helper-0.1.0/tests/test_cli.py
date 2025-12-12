from ai_helper.cli import main


def test_cli_ask(capsys):
    main(["ask", "hello there"])
    out = capsys.readouterr().out.strip()
    assert out.startswith("[local]")
    assert "hello there" in out


def test_cli_summarize(capsys):
    main(["summarize", "one two three four five", "--max-words", "3"])
    out = capsys.readouterr().out.strip()
    assert len(out.split()) <= 4  # includes prefix
