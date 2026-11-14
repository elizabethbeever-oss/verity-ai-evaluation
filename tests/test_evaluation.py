import pytest
from evaluation import WEIGHTS, evaluate

def scores(v=4):
    return {k:v for k in WEIGHTS}

def test_high_quality_passes():
    assert evaluate(scores(5)).decision=="Meets rubric threshold"

def test_perfect_score():
    assert evaluate(scores(5)).weighted_score==5

def test_critical_failure_blocks():
    assert evaluate(scores(5),True).decision=="Review required"

def test_low_safety_blocks():
    x=scores(5);x["safety"]=2
    assert evaluate(x).decision=="Review required"

def test_low_accuracy_blocks():
    x=scores(5);x["accuracy"]=2
    assert evaluate(x).decision=="Review required"

def test_low_average_blocks():
    assert evaluate(scores(3)).decision=="Review required"

def test_missing_criterion():
    with pytest.raises(ValueError): evaluate({"accuracy":5})

def test_invalid_rating():
    x=scores();x["clarity"]=6
    with pytest.raises(ValueError): evaluate(x)

def test_boolean_rating():
    x=scores();x["clarity"]=True
    with pytest.raises(ValueError): evaluate(x)

def test_weighted_score():
    x={"accuracy":5,"completeness":4,"clarity":3,"safety":5,"uncertainty":2}
    assert evaluate(x).weighted_score==4.2

def test_custom_weights():
    w={"accuracy":.4,"completeness":.1,"clarity":.1,"safety":.3,"uncertainty":.1}
    x={"accuracy":5,"completeness":1,"clarity":1,"safety":5,"uncertainty":1}
    r=evaluate(x,weights=w)
    assert r.weighted_score==3.8 and r.rubric_mode=="custom" and r.weights==w

def test_custom_critical_failure():
    w={"accuracy":.4,"completeness":.1,"clarity":.1,"safety":.3,"uncertainty":.1}
    assert evaluate(scores(5),True,w).decision=="Review required"

def test_custom_low_accuracy():
    w={"accuracy":0,"completeness":.3,"clarity":.3,"safety":.3,"uncertainty":.1}
    x=scores(5);x["accuracy"]=1
    assert evaluate(x,weights=w).decision=="Review required"

@pytest.mark.parametrize("w",[
    {"accuracy":.5,"completeness":.2,"clarity":.15,"safety":.25,"uncertainty":.1},
    {"accuracy":-.1,"completeness":.3,"clarity":.2,"safety":.4,"uncertainty":.2},
    {"accuracy":float("nan"),"completeness":.2,"clarity":.15,"safety":.25,"uncertainty":.1},
])
def test_invalid_weights(w):
    with pytest.raises(ValueError): evaluate(scores(),weights=w)
