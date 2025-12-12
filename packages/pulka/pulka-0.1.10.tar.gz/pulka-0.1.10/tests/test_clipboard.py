from pulka.clipboard import copy_to_clipboard


class StubBackend:
    def __init__(self, *, supported: bool = True, succeeds: bool = True):
        self.supported = supported
        self.succeeds = succeeds
        self.calls: list[str] = []
        self.name = "stub"

    def is_supported(self) -> bool:
        return self.supported

    def copy(self, text: str) -> bool:
        self.calls.append(text)
        return self.succeeds


def test_copy_to_clipboard_uses_first_successful_backend():
    failing = StubBackend(succeeds=False)
    success = StubBackend()

    result = copy_to_clipboard("hello", backends=[failing, success])

    assert result is True
    assert failing.calls == ["hello"]
    assert success.calls == ["hello"]


def test_copy_to_clipboard_returns_false_when_all_backends_fail():
    unsupported = StubBackend(supported=False)
    failing = StubBackend(succeeds=False)

    result = copy_to_clipboard("hello", backends=[unsupported, failing])

    assert result is False
    assert unsupported.calls == []
    assert failing.calls == ["hello"]
