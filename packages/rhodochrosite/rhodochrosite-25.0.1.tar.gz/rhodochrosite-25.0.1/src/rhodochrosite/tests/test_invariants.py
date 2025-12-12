from rhodochrosite.ruby import RubySymbol


def test_symbols_are_equal() -> None:
    sym1 = RubySymbol(value="abc")
    sym2 = RubySymbol(value="abc")
    sym3 = RubySymbol(value="def")

    assert sym1 == sym2
    assert sym2 != sym3
    assert sym1 != "abc"
    assert str(sym1) == "abc"

    assert hash(sym1) == hash(sym2)
    assert hash(sym2) != hash(sym3)
