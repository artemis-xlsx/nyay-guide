import sqlite3, json
from app.india.nri_engine import NRIFacts, evaluate_nri_case

def test_satya_v_teja_singh_foreign_decree_nullity():
    f = NRIFacts(spouse_abroad=True, foreign_decree_obtained=True, decree_submitted_to=False)
    r = evaluate_nri_case(f)
    assert r["private_international_law"]["status_in_india"] == "NULL AND VOID ab initio"
    assert any("Satya v. Teja Singh" in p["precedent"] for p in r["authorities_and_holdings"])
    assert any("Y. Narasimha Rao" in p["precedent"] for p in r["authorities_and_holdings"])

def test_baiju_v_hema_adverse_inference():
    f = NRIFacts(spouse_abroad=True, spouse_country="uae", undisclosed_income=True, lifestyle_tier="tech/managerial")
    r = evaluate_nri_case(f)
    assert r["income_and_deductions"]["adverse_inference_applied"] is True
    assert r["income_and_deductions"]["gross_foreign_monthly_salary"] == 20000.0 # AED calibrated benchmark
    assert any("Baiju v. Hema" in p["precedent"] for p in r["authorities_and_holdings"])

def test_configurable_deductions_and_statutory_transition():
    # Test post-July 2024 filing with user-configured 40% deduction
    f = NRIFacts(
        spouse_abroad=True,
        spouse_country="usa",
        stated_monthly_income=10000,
        foreign_living_cost_deduction_pct=0.40,
        spousal_maintenance_pct=0.25,
        case_filing_date_post_july_2024=True
    )
    r = evaluate_nri_case(f)
    assert r["income_and_deductions"]["foreign_living_cost_deduction_pct"] == "40.0%"
    assert r["income_and_deductions"]["net_disposable_foreign_surplus_monthly"] == 6000.0
    assert "Section 144" in r["procedural_framework"]["governing_maintenance_code"]
    assert "BNSS" in r["procedural_framework"]["governing_maintenance_code"]
    assert "Section 119(g)" in r["procedural_framework"]["governing_evidence_code"]
    assert any("Devika Jain" in p["precedent"] for p in r["authorities_and_holdings"])

def test_cpc_section_44a_and_passports_act_suresh_nanda():
    f = NRIFacts(spouse_abroad=True, spouse_country="usa")
    r = evaluate_nri_case(f)
    roadmap = r["cross_border_enforcement_roadmap"]
    # USA is non-reciprocating territory under 44A CPC
    assert roadmap["section_44a_cpc"]["status"] == "NOT AVAILABLE (Non-Reciprocating Territory)"
    # Suresh Nanda precedent on passport impoundment limits
    assert "Suresh Nanda" in roadmap["passport_impoundment"]["judicial_power"]
    assert "10(3)(h)" in roadmap["passport_impoundment"]["statutory_provision"]

def test_nri_cases_db_16_fields_and_audit_fields():
    conn = sqlite3.connect("backend/app/india/nri_cases.db")
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(nri_case_law)")
    columns = [row[1] for row in cur.fetchall()]
    
    # Check count
    cur.execute("SELECT COUNT(*) FROM nri_case_law")
    count = cur.fetchone()[0]
    conn.close()
    
    assert count >= 120, f"Expected at least 120 curated cases, got {count}"
    
    expected_fields = [
        "court", "case_title", "case_number", "judgment_date", "judges",
        "acts_cited", "sections_cited", "legal_topics", "outcome",
        "fact_petitioner", "fact_respondent", "issues", "petitioner_argument",
        "respondent_argument", "factors_considered", "decision",
        "verification_status", "exact_holding", "negative_limitations",
        "calculator_dependency", "primary_source_link", "reviewed_by_and_date"
    ]
    for field in expected_fields:
        assert field in columns, f"Missing field: {field}"

if __name__ == "__main__":
    test_satya_v_teja_singh_foreign_decree_nullity()
    test_baiju_v_hema_adverse_inference()
    test_configurable_deductions_and_statutory_transition()
    test_cpc_section_44a_and_passports_act_suresh_nanda()
    test_nri_cases_db_16_fields_and_audit_fields()
    print("All updated NRI engine and 22-field DB tests passed successfully!")
