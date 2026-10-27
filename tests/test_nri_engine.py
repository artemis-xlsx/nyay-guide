import sqlite3, json
from app.india.nri_engine import NRIFacts, evaluate_nri_case

def test_satya_v_teja_singh_foreign_decree_nullity():
    f = NRIFacts(spouse_abroad=True, foreign_decree_obtained=True, decree_submitted_to=False)
    r = evaluate_nri_case(f)
    assert r["foreign_decree_valid_in_india"] is False
    assert any("Satya v. Teja Singh" in p["precedent"] for p in r["judicial_precedents"])

def test_baiju_v_hema_adverse_inference():
    f = NRIFacts(spouse_abroad=True, spouse_country="uae", undisclosed_income=True, lifestyle_tier="tech/managerial")
    r = evaluate_nri_case(f)
    assert r["adverse_inference_applied"] is True
    assert r["imputed_or_disclosed_gross_foreign_salary"] == 22000 # AED
    assert any("Baiju v. Hema" in p["precedent"] for p in r["judicial_precedents"])

def test_devika_jain_50_pct_deduction():
    f = NRIFacts(spouse_abroad=True, spouse_country="usa", stated_monthly_income=10000, undisclosed_income=False)
    r = evaluate_nri_case(f)
    assert r["net_disposable_foreign_surplus_monthly"] == 5000.0 # 50% deduction
    assert any("Devika Jain" in p["precedent"] for p in r["judicial_precedents"])

def test_moni_v_sujatha_divorced_wife():
    f = NRIFacts(divorce_status="decreed", past_marital_fault_alleged=True)
    r = evaluate_nri_case(f)
    assert r["disqualified"] is False
    assert any("Moni v. Sujatha" in p["precedent"] for p in r["judicial_precedents"])

def test_kulwinder_kumar_minimum_floor():
    f = NRIFacts(spouse_abroad=True, spouse_country="other", stated_monthly_income=500, undisclosed_income=False, children_count=0)
    r = evaluate_nri_case(f)
    assert r["calculated_monthly_maintenance_inr"] >= 20000
    assert r["interim_floor_enforced"] is True
    assert any("Kulwinder Kumar" in p["precedent"] for p in r["judicial_precedents"])

def test_nri_cases_db_16_fields():
    conn = sqlite3.connect("backend/app/india/nri_cases.db")
    cur = conn.cursor()
    cur.execute("PRAGMA table_info(nri_case_law)")
    columns = [row[1] for row in cur.fetchall()]
    conn.close()
    
    expected_fields = [
        "court", "case_title", "case_number", "judgment_date", "judges",
        "acts_cited", "sections_cited", "legal_topics", "outcome",
        "fact_petitioner", "fact_respondent", "issues", "petitioner_argument",
        "respondent_argument", "factors_considered", "decision"
    ]
    for field in expected_fields:
        assert field in columns, f"Missing field: {field}"

if __name__ == "__main__":
    test_satya_v_teja_singh_foreign_decree_nullity()
    test_baiju_v_hema_adverse_inference()
    test_devika_jain_50_pct_deduction()
    test_moni_v_sujatha_divorced_wife()
    test_kulwinder_kumar_minimum_floor()
    test_nri_cases_db_16_fields()
    print("All NRI engine and 16-field DB tests passed successfully!")
