from info_llm_observe.exceptions import estimate_tokens, estimate_cost

def test_estimate_tokens_and_cost():
    t = estimate_tokens("hello world")
    assert t >= 1
    c = estimate_cost(t)
    assert c >= 0
