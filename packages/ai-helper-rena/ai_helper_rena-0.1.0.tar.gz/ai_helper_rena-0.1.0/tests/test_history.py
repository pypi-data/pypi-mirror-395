from GPT_Helper.history import ConversationHistory

def test_history_add():
    h = ConversationHistory(max_items=2)
    h.add("a", "1")
    h.add("b", "2")
    assert len(h.all()) == 2

    h.add("c", "3")
    assert len(h.all()) == 2
    assert h.all()[-1]["prompt"] == "c"
