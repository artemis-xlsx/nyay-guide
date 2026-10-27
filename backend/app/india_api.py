import logging
from typing import Any, Literal, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from .india import Facts, advise, CATALOGUE
from .india.intake import extract
from .india import slm
from .india.agent import step, forget

router = APIRouter(prefix="/api/india", tags=["india-family-law"])

Law = Literal["hindu", "muslim", "christian", "parsi", "special_marriage"]
Place = Optional[str]


class FactsIn(BaseModel):
    law: Law = Field(description="hindu (incl. Sikh, Jain, Buddhist) | muslim | christian | parsi | special_marriage")
    claimant: Literal["wife", "husband", "child", "parent"] = "wife"
    needs: list[Literal["divorce", "maintenance", "protection"]] = []
    mutual_consent: bool = False
    ground: Optional[str] = Field(default=None, max_length=80)
    marriage_years: Optional[float] = Field(default=None, ge=0, le=100)
    separated_months: Optional[float] = Field(default=None, ge=0, le=1200)
    marriage_place: Optional[str] = Field(default=None, max_length=80)
    last_cohabitation_place: Optional[str] = Field(default=None, max_length=80)
    petitioner_residence: Optional[str] = Field(default=None, max_length=80)
    respondent_residence: Optional[str] = Field(default=None, max_length=80)
    respondent_abroad: bool = False
    claimant_can_self_maintain: bool = False
    respondent_has_means: bool = True
    claimant_living_in_adultery: bool = False
    claimant_refuses_cohabitation_without_cause: bool = False
    separated_by_mutual_consent: bool = False
    domestic_violence: bool = False
    child_minor: bool = True
    child_disabled: bool = False
    divorce_status: Optional[Literal["none", "pending", "decreed", "filed"]] = Field(
        default=None, description="none | pending | decreed | filed (filed = pending or decreed, unknown which)")
    divorce_pending_or_decreed: bool = Field(default=False, description="legacy; prefer divorce_status")


@router.post("/advise")
def advise_route(body: FactsIn):
    try:
        return advise(Facts(**body.model_dump()))
    except ValueError as e:
        raise HTTPException(422, str(e))


@router.get("/catalogue")
def catalogue():
    return CATALOGUE


class IntakeIn(BaseModel):
    text: str = Field(max_length=4000)


@router.post("/intake")
def intake(body: IntakeIn):
    return slm.augment(body.text, extract(body.text))


class AnswerIn(BaseModel):
    slot: str = Field(max_length=40)
    value: Any = None


class AgentIn(BaseModel):
    session_id: Optional[str] = Field(default=None, max_length=64)
    text: Optional[str] = Field(default=None, max_length=4000)
    answer: Optional[AnswerIn] = None
    lang: Optional[str] = Field(default=None, pattern="^(en|hi|ta)$")
    snapshot: Optional[dict] = None     # sent back by the browser so a restarted server can rebuild the session


@router.post("/agent")
def agent(body: AgentIn):
    try:
        return step(body.session_id, body.text, body.answer.model_dump() if body.answer else None, lang=body.lang, snap=body.snapshot)
    except ValueError as e:
        a = body.answer
        logging.getLogger("uvicorn.error").warning("agent 422: %s (slot=%s)", e, a.slot if a else None)   # never logs the person's text or answers
        raise HTTPException(422, str(e))


@router.delete("/session/{session_id}", status_code=204)
def delete_session(session_id: str):
    """Forget a session and everything typed into it."""
    forget(session_id)


# ---- NRI Matrimonial & Maintenance Engine Endpoints ----
import sqlite3, json
from pathlib import Path
from .india.nri_engine import NRIFacts, evaluate_nri_case


class NRIFactsInput(BaseModel):
    claimant: Literal["wife", "child", "parent", "husband"] = "wife"
    marriage_law: Literal["hindu", "muslim", "christian", "parsi", "special_marriage"] = "hindu"
    spouse_abroad: bool = True
    spouse_country: Literal["usa", "uae", "uk", "canada", "australia", "qatar", "singapore", "other"] = "uae"
    stated_monthly_income: Optional[float] = None
    currency: Optional[str] = None
    undisclosed_income: bool = False
    lifestyle_tier: Literal["tech/managerial", "medical/doctor", "executive/business", "entry/clerical", "manual/labour", "unknown"] = "tech/managerial"
    custom_imputed_salary: Optional[float] = None
    foreign_living_cost_deduction_pct: Optional[float] = None
    spousal_maintenance_pct: float = 0.25
    child_maintenance_pct_per_child: float = 0.10
    wife_monthly_income: float = 0.0
    children_count: int = 0
    children_education_monthly: float = 0.0
    foreign_decree_obtained: bool = False
    decree_submitted_to: bool = False
    domestic_violence: bool = False
    abandoned_in_india: bool = True
    divorce_status: Literal["none", "pending", "decreed"] = "none"
    past_marital_fault_alleged: bool = False
    case_filing_date_post_july_2024: bool = True


@router.get("/nri/cases")
def get_nri_cases(query: Optional[str] = None, court: Optional[str] = None):
    """Query structured NRI case law database with 16 core fields + verification/audit metadata."""
    db_path = Path(__file__).resolve().parent / "india" / "nri_cases.db"
    if not db_path.exists():
        raise HTTPException(404, "NRI cases database not found")
    conn = sqlite3.connect(db_path)
    cur = conn.cursor()
    sql = """
    SELECT id, court, case_title, case_number, judgment_date, judges,
           acts_cited, sections_cited, legal_topics, outcome,
           fact_petitioner, fact_respondent, issues, petitioner_argument,
           respondent_argument, factors_considered, decision,
           verification_status, exact_holding, negative_limitations,
           calculator_dependency, primary_source_link, reviewed_by_and_date
    FROM nri_case_law WHERE 1=1
    """
    params = []
    if court:
        sql += " AND court LIKE ?"
        params.append(f"%{court}%")
    if query:
        sql += " AND (case_title LIKE ? OR legal_topics LIKE ? OR issues LIKE ? OR decision LIKE ? OR exact_holding LIKE ?)"
        params.extend([f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%", f"%{query}%"])
    cur.execute(sql, params)
    rows = cur.fetchall()
    conn.close()

    results = []
    keys = [
        "id", "Court", "Case Title", "Case Number", "Judgment Date", "Judges",
        "Acts Cited", "Sections Cited", "Legal Topics", "Outcome",
        "Fact/Petitioner", "Fact/Respondent", "Issues", "Petitioner Argument",
        "Respondent Argument", "Factors to be Considered", "Decision",
        "Verification Status", "Exact Holding", "Negative Limitations",
        "Calculator Dependency", "Primary Source Link", "Reviewed By & Date"
    ]
    for row in rows:
        d = dict(zip(keys, row))
        try: d["Acts Cited"] = json.loads(d["Acts Cited"])
        except: pass
        try: d["Sections Cited"] = json.loads(d["Sections Cited"])
        except: pass
        try: d["Legal Topics"] = json.loads(d["Legal Topics"])
        except: pass
        results.append(d)
    return {"total": len(results), "cases": results}


@router.post("/nri/evaluate")
def evaluate_nri_route(body: NRIFactsInput):
    """Deterministic NRI maintenance & jurisdiction evaluation."""
    facts = NRIFacts(**body.model_dump())
    return evaluate_nri_case(facts)


class NRIIntakeInput(BaseModel):
    text: str = Field(max_length=4000)
    country: Optional[str] = "uae"
    stated_monthly_income: Optional[float] = None
    children_count: int = 0


@router.post("/nri/intake")
def nri_intake_route(body: NRIIntakeInput):
    """Natural language text intake using SLM + lexicon, flowing into deterministic NRI inference."""
    intake_res = slm.augment(body.text, extract(body.text))
    facts_dict = intake_res.get("facts", {})
    tent = intake_res.get("tentative", {})

    text_lower = body.text.lower()
    detected_country = body.country or "other"
    if any(k in text_lower for k in ["dubai", "uae", "abu dhabi", "sharjah", "दुबई"]):
        detected_country = "uae"
    elif any(k in text_lower for k in ["america", "usa", "california", "texas", "न्यूयॉर्क", "अमेरिका"]):
        detected_country = "usa"
    elif any(k in text_lower for k in ["uk", "london", "england", "birmingham", "लंदन"]):
        detected_country = "uk"
    elif any(k in text_lower for k in ["canada", "toronto", "ontario", "vancouver", "कनाडा"]):
        detected_country = "canada"
    elif any(k in text_lower for k in ["australia", "sydney", "melbourne"]):
        detected_country = "australia"
    elif any(k in text_lower for k in ["qatar", "doha", "कतर"]):
        detected_country = "qatar"
    elif "singapore" in text_lower:
        detected_country = "singapore"

    undisclosed = False
    if any(k in text_lower for k in ["hide", "hides", "conceal", "refuse", "won't show", "chupa", "nahi bata"]):
        undisclosed = True
    if "undisclosed_income" in tent:
        undisclosed = True

    foreign_decree = False
    if any(k in text_lower for k in ["foreign decree", "foreign court", "ex parte divorce", "divorced abroad", "nevada", "texas court", "विदेश से तलाक"]):
        foreign_decree = True
    if "foreign_decree_obtained" in tent:
        foreign_decree = True

    facts = NRIFacts(
        spouse_abroad=facts_dict.get("respondent_abroad", True),
        spouse_country=detected_country,
        stated_monthly_income=body.stated_monthly_income,
        undisclosed_income=undisclosed,
        domestic_violence=facts_dict.get("domestic_violence", False),
        foreign_decree_obtained=foreign_decree,
        children_count=body.children_count,
        divorce_status=facts_dict.get("divorce_status", "none")
    )
    eval_result = evaluate_nri_case(facts)
    return {
        "extracted_intake": intake_res,
        "mapped_facts": facts.__dict__,
        "evaluation": eval_result
    }

