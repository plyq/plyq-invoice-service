import app.main as am


def test_main() -> None:
    assert am.main() == "Hello world!"
