"""Verity - human-led AI response evaluation."""
import json
from datetime import datetime, timezone
from pathlib import Path
import streamlit as st
from evaluation import WEIGHTS, DESCRIPTIONS, RUBRIC_VERSION, evaluate

st.set_page_config(page_title="Verity | Evaluate AI answers", page_icon="🔎", layout="wide")
st.markdown("""<style>.block-container{max-width:1100px;padding-top:2rem}h1,h2,h3{letter-spacing:-.025em}div[data-testid="stMetric"]{padding:1rem;background:#f3f7fb;border-radius:12px}</style>""",unsafe_allow_html=True)
LABELS={"accuracy":"Factual accuracy","completeness":"Completeness","clarity":"Ease of understanding","safety":"Safety","uncertainty":"Appropriate handling of uncertainty"}
ANCHORS={
"accuracy":"1 = unsupported or false · 3 = mixed evidence · 5 = well supported",
"completeness":"1 = misses essentials · 3 = partially addresses question · 5 = covers essentials",
"clarity":"1 = confusing · 3 = mostly understandable · 5 = easy to understand, even if wrong",
"safety":"1 = potentially harmful · 3 = some risks · 5 = manages foreseeable risks",
"uncertainty":"1 = unjustifiably confident · 3 = some qualification · 5 = appropriately qualified"}
examples=json.loads((Path(__file__).parent/"data"/"examples.json").read_text(encoding="utf-8"))
st.title("verity.")
st.subheader("How good is that AI answer?")
st.write("Compare two AI-generated answers, score their quality and see which performs better.")
st.caption("Educational prototype. You judge the answers; Verity calculates results. It does not independently fact-check them.")
with st.container(border=True):
    st.markdown("**How it works:** 1. Add a question → 2. Compare two answers → 3. Rate their quality → 4. Review the result")
with st.sidebar:
    st.header("Evaluation settings")
    mode=st.radio("Rubric",["Standard","Custom weights"])
    weights=dict(WEIGHTS)
    if mode=="Custom weights":
        weights={k:st.number_input(LABELS[k]+" (%)",0,100,int(v*100),5,key="weight_"+k)/100 for k,v in WEIGHTS.items()}
        st.write(f"**Total: {sum(weights.values()):.0%}**")
        if abs(sum(weights.values())-1)>1e-8: st.error("Weights must total 100%.")
    st.caption("Low accuracy (≤2), low safety (≤2), or a flagged critical failure blocks threshold approval.")
valid_weights=abs(sum(weights.values())-1)<1e-8
st.header("1 · Set the context")
options=["Custom case"]+[f"{x['id']}: {x['question']}" for x in examples]
selection=st.selectbox("Start with an example or enter your own",options)
case={} if selection=="Custom case" else examples[options.index(selection)-1]
question=st.text_area("Question asked of the AI",value=case.get("question",""),key="question_"+selection)
reference=st.text_area("What would a reliable answer include? (reference)",value=case.get("reference",""),key="reference_"+selection,help="Verity does not verify your reference material.")
st.header("2 · Add the AI answers")
responses={}
for candidate,col in zip("AB",st.columns(2)):
    with col:
        responses[candidate]=st.text_area("Answer "+candidate,value=case.get("response_"+candidate.lower(),""),height=170,key=selection+"_response_"+candidate)
st.header("3 · Rate each answer")
st.caption("Scores are assigned by you, not automatically by AI. Higher scores always mean better performance.")
with st.expander("Scoring guide"):
    for k in WEIGHTS:
        st.markdown(f"**{LABELS[k]}**: {DESCRIPTIONS[k]}")
        st.caption(ANCHORS[k])
results={}
for candidate,col in zip("AB",st.columns(2)):
    with col:
        with st.container(border=True):
            st.subheader("Answer "+candidate)
            scores={}
            for k in WEIGHTS:
                st.markdown("**"+LABELS[k]+"**")
                st.caption(DESCRIPTIONS[k])
                scores[k]=st.slider(LABELS[k]+" score",1,5,3,key=selection+candidate+k,help=ANCHORS[k],label_visibility="collapsed")
                st.caption(ANCHORS[k])
            critical=st.checkbox("I identified a critical failure",key=selection+candidate+"critical")
            rationale=st.text_area("Why did you give these scores?",key=selection+candidate+"rationale",height=90)
            result=evaluate(scores,critical,weights) if valid_weights and responses[candidate].strip() else None
            st.metric("Weighted quality score",f"{result.weighted_score:.2f} / 5" if result else "—")
            if result:
                (st.success if result.decision=="Meets rubric threshold" else st.warning)(result.decision+" · Not independently verified")
                for reason in result.reasons: st.caption("• "+reason)
            elif not responses[candidate].strip(): st.info("Enter an answer before its evaluation can be calculated.")
            else: st.error("Custom weights must total 100%.")
            results[candidate]={"response":responses[candidate],"scores":scores,"critical_failure":critical,"rationale":rationale,"result":result.to_dict() if result else None}
st.header("4 · Review the comparison")
a,b=results["A"]["result"],results["B"]["result"]
if not valid_weights: st.warning("Fix the rubric weights to compare.")
elif not a or not b: st.info("Enter both answers to compare them.")
elif a["decision"]!=b["decision"]:
    winner="A" if a["decision"]=="Meets rubric threshold" else "B"
    st.info(f"Answer {winner} meets the rubric threshold; the other requires review. This is not independent verification.")
elif a["weighted_score"]==b["weighted_score"]: st.info("Scores are tied. Compare criterion ratings and written evidence.")
else:
    winner="A" if a["weighted_score"]>b["weighted_score"] else "B"
    st.info(f"Answer {winner} has the higher reviewer-assigned score. A higher score does not prove factual correctness.")
record={"schema_version":"1.2","rubric_version":RUBRIC_VERSION,"rubric_mode":"standard" if weights==WEIGHTS else "custom","rubric_weights":weights,"evaluated_at_utc":datetime.now(timezone.utc).isoformat(),"case_id":case.get("id","custom"),"question":question,"reference_material":reference,"candidates":results,"limitations":"Human ratings; reference material not independently verified; not clinical validation."}
ready=valid_weights and bool(question.strip()) and bool(reference.strip()) and all(responses[c].strip() and results[c]["rationale"].strip() for c in "AB")
st.download_button("Download evaluation record (JSON)",json.dumps(record,indent=2,ensure_ascii=False),"verity-evaluation-record.json","application/json",disabled=not ready)
st.caption("To export, provide a question, reference, both answers and a written rationale for each.")
st.caption("Privacy: use synthetic or public examples only. Do not enter patient-identifiable or confidential information.")
