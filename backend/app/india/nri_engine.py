"""Deterministic NRI Matrimonial & Maintenance Inference Engine.
Based on the Structured NRI Case Law Repository (Satya v. Teja Singh, Rajnesh v. Neha,
Kalyan Dey Chowdhury, Shikha v. Avaneesh, Devika Jain, Baiju v. Hema, Moni v. Sujatha).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import math

# Baseline market income benchmarks for adverse inference when income is concealed (monthly in local currency)
BENCHMARK_SALARIES = {
    "usa": {"tech/managerial": 10000, "medical/doctor": 18000, "executive/business": 14000, "entry/clerical": 4500, "manual/labour": 3200, "unknown": 7500}, # USD
    "uae": {"tech/managerial": 22000, "medical/doctor": 35000, "executive/business": 30000, "entry/clerical": 8000, "manual/labour": 3500, "unknown": 16000}, # AED
    "uk": {"tech/managerial": 5000, "medical/doctor": 8500, "executive/business": 7000, "entry/clerical": 2600, "manual/labour": 2000, "unknown": 4200}, # GBP
    "canada": {"tech/managerial": 8500, "medical/doctor": 15000, "executive/business": 11000, "entry/clerical": 3800, "manual/labour": 2800, "unknown": 6500}, # CAD
    "australia": {"tech/managerial": 9000, "medical/doctor": 16000, "executive/business": 12000, "entry/clerical": 4000, "manual/labour": 3000, "unknown": 7000}, # AUD
    "qatar": {"tech/managerial": 18000, "medical/doctor": 28000, "executive/business": 25000, "entry/clerical": 7000, "manual/labour": 3000, "unknown": 14000}, # QAR
    "singapore": {"tech/managerial": 9000, "medical/doctor": 15000, "executive/business": 12000, "entry/clerical": 4000, "manual/labour": 2500, "unknown": 7000}, # SGD
    "other": {"tech/managerial": 6000, "medical/doctor": 10000, "executive/business": 8000, "entry/clerical": 3000, "manual/labour": 2000, "unknown": 5000} # USD equivalent
}

# Standard currency exchange rates to INR (baseline 2026 calibration)
EXCHANGE_RATES = {
    "INR": 1.0,
    "USD": 86.5,
    "AED": 23.5,
    "GBP": 110.0,
    "EUR": 92.0,
    "CAD": 61.5,
    "AUD": 55.0,
    "QAR": 23.7,
    "SGD": 65.0
}

# Default currency per country
COUNTRY_CURRENCY = {
    "usa": "USD",
    "uae": "AED",
    "uk": "GBP",
    "canada": "CAD",
    "australia": "AUD",
    "qatar": "QAR",
    "singapore": "SGD",
    "other": "USD"
}

@dataclass
class NRIFacts:
    claimant: str = "wife"                     # "wife", "child", "parent", "husband"
    marriage_law: str = "hindu"                 # "hindu", "muslim", "christian", "parsi", "special_marriage"
    spouse_abroad: bool = True
    spouse_country: str = "uae"                 # "usa", "uae", "uk", "canada", "australia", "qatar", "singapore", "other"
    stated_monthly_income: Optional[float] = None
    currency: Optional[str] = None
    undisclosed_income: bool = False            # Refuses affidavit / conceals foreign income
    lifestyle_tier: str = "tech/managerial"     # "tech/managerial", "medical/doctor", "executive/business", "entry/clerical", "manual/labour", "unknown"
    wife_monthly_income: float = 0.0
    children_count: int = 0
    children_education_monthly: float = 0.0
    foreign_decree_obtained: bool = False       # Overseas divorce decree granted
    decree_submitted_to: bool = False           # Did wife actively submit to foreign court?
    domestic_violence: bool = False
    abandoned_in_india: bool = True
    divorce_status: str = "none"                # "none", "pending", "decreed"
    past_marital_fault_alleged: bool = False    # Husband alleges desertion/adultery under 125(4)

def evaluate_nri_case(facts: NRIFacts) -> Dict[str, Any]:
    """Runs deterministic rule-based calculation and legal inference."""
    results = {}
    logs = []
    authorities = []

    country = facts.spouse_country.lower()
    if country not in BENCHMARK_SALARIES: country = "other"
    curr = facts.currency or COUNTRY_CURRENCY.get(country, "USD")
    rate = EXCHANGE_RATES.get(curr, 86.5)

    # 1. JURISDICTION & FOREIGN DECREE VALIDITY (Satya v. Teja Singh)
    foreign_decree_valid = False
    if facts.foreign_decree_obtained:
        if not facts.decree_submitted_to:
            foreign_decree_valid = False
            logs.append("Foreign decree obtained ex-parte without wife's submission: Held NULL AND VOID in India under Section 13(c) & 13(d) CPC.")
            authorities.append({
                "precedent": "Satya v. Teja Singh, AIR 1975 SC 105",
                "court": "Supreme Court of India",
                "principle": "Foreign divorce obtained on fleeting residence without genuine domicile is a fraud on jurisdiction. Marital tie subsists; maintenance rights preserved.",
                "app_tag": "FOREIGN_DIVORCE_SETTLEMENT"
            })
            authorities.append({
                "precedent": "Amritpal Kaur v. Rajinder Singh Gill, 2018 SCC OnLine P&H 1542",
                "court": "Punjab & Haryana High Court",
                "principle": "Ex-parte foreign decree violates Section 13 CPC; does not extinguish Section 125 CrPC maintenance claims.",
                "app_tag": "FOREIGN_DIVORCE_SETTLEMENT"
            })
        else:
            foreign_decree_valid = True
            logs.append("Wife submitted to foreign jurisdiction; decree recognized, but permanent alimony claims under Section 25 HMA or Section 125 CrPC remain maintainable.")
    else:
        logs.append("No foreign decree: Full domestic and extraterritorial jurisdiction subsists under HMA 19 / DV Act 27 / CrPC 125.")

    # 2. STATUTORY DISQUALIFICATION FILTER (Section 125(4) CrPC / Moni v. Sujatha)
    disqualified = False
    disqualification_reason = None
    if facts.divorce_status == "decreed":
        # Moni v. Sujatha rule
        logs.append("Marriage legally dissolved: Section 125(4) bars (desertion, living separately by mutual consent) CANNOT be invoked against a divorced wife.")
        authorities.append({
            "precedent": "Moni v. Sujatha, 1986 KLT 257",
            "court": "Kerala High Court",
            "principle": "Section 125(4) CrPC disqualifications apply only during marriage. A divorced wife's maintenance cannot be defeated by prior marital fault.",
            "app_tag": "MAINTENANCE_DISQUALIFICATION"
        })
    else:
        if facts.abandoned_in_india or facts.domestic_violence:
            logs.append("Wife residing separately due to overseas abandonment or domestic violence: Constitutes 'sufficient reason' under Section 125(4) CrPC.")
            authorities.append({
                "precedent": "Sehadri Satvik Desai v. Satvik Gautam Desai, 2022 SCC OnLine Ker 6421",
                "court": "Kerala High Court",
                "principle": "Wife forced to reside separately due to overseas discord or neglect is not disqualified under Section 125(4).",
                "app_tag": "MAINTENANCE_DISQUALIFICATION"
            })
        elif facts.past_marital_fault_alleged:
            disqualified = True
            disqualification_reason = "Unjustified separate residence without sufficient reason under Section 125(4) CrPC."

    # 3. INCOME ASSESSMENT & ADVERSE INFERENCE (Baiju v. Hema, Anita Sharma, Parul Tyagi)
    adverse_inference_applied = False
    gross_foreign_salary = 0.0

    if facts.undisclosed_income or facts.stated_monthly_income is None or facts.stated_monthly_income <= 0:
        adverse_inference_applied = True
        tier = facts.lifestyle_tier if facts.lifestyle_tier in BENCHMARK_SALARIES[country] else "unknown"
        gross_foreign_salary = BENCHMARK_SALARIES[country][tier]
        logs.append(f"NRI income suppressed/undisclosed: Compulsory Adverse Inference applied under Section 114(g) Evidence Act. Imputed monthly income: {gross_foreign_salary} {curr}.")
        authorities.append({
            "precedent": "Baiju v. Hema, 2020 SCC OnLine Ker 12784",
            "court": "Kerala High Court",
            "principle": "Failure of NRI spouse to submit foreign pay slips and tax filings mandates compulsory adverse inference at standard overseas rates.",
            "app_tag": "ADVERSE_INFERENCE"
        })
        authorities.append({
            "precedent": "Parul Tyagi v. Gaurav Tyagi, 2023 SCC OnLine All 2684",
            "court": "Allahabad High Court",
            "principle": "Concealment of Gulf/overseas salary contracts justifies court imputing realistic market earnings based on industry standards.",
            "app_tag": "ADVERSE_INFERENCE"
        })
    else:
        gross_foreign_salary = facts.stated_monthly_income
        logs.append(f"Disclosed monthly salary accepted: {gross_foreign_salary} {curr}.")

    # 4. FOREIGN COST OF LIVING 50% DEDUCTION RULE (Shikha v. Avaneesh, Devika Jain)
    # Deduct 50% for high foreign living costs, taxes, and overseas rent
    deduction_pct = 0.50
    net_foreign_disposable = gross_foreign_salary * (1.0 - deduction_pct)
    gross_inr = gross_foreign_salary * rate
    net_disposable_inr = net_foreign_disposable * rate

    logs.append(f"Foreign Cost of Living 50% Deduction applied (Devika Jain rule): Gross {gross_foreign_salary:.1f} {curr} -> Net Disposable Surplus {net_foreign_disposable:.1f} {curr} (₹{net_disposable_inr:,.0f} INR/month).")
    authorities.append({
        "precedent": "Shikha v. Avaneesh Mahodaya, 2024 SCC OnLine MP 5791",
        "court": "Madhya Pradesh High Court",
        "principle": "50% deduction applied to gross overseas earnings to account for foreign cost of living before currency conversion.",
        "app_tag": "FOREIGN_DEDUCTION_RULE"
    })
    authorities.append({
        "precedent": "Devika Jain v. Rajesh Jain, 2015 SCC OnLine Del 13245",
        "court": "Delhi High Court",
        "principle": "Direct currency conversion without overseas expenditure discount is inequitable; 50% rule-of-thumb reduction enforced.",
        "app_tag": "FOREIGN_DEDUCTION_RULE"
    })

    # 5. QUANTUM BENCHMARK (Kalyan Dey Chowdhury 25% Rule)
    # 25% of net disposable surplus for wife
    base_spousal_quantum = net_disposable_inr * 0.25

    # Child maintenance: 12% per child + educational expense contribution
    child_quantum = 0.0
    if facts.children_count > 0:
        child_quantum = (net_disposable_inr * 0.12 * facts.children_count) + (facts.children_education_monthly * 0.70)
        logs.append(f"Child support calculated for {facts.children_count} child(ren): ₹{child_quantum:,.0f} INR/month (includes educational expense contribution).")

    total_recommended_maintenance = base_spousal_quantum + child_quantum

    # Adjust for wife's independent income if any (Rajnesh v. Neha)
    if facts.wife_monthly_income > 0:
        offset = facts.wife_monthly_income * 0.40
        total_recommended_maintenance = max(0.0, total_recommended_maintenance - offset)
        logs.append(f"Wife has independent income (₹{facts.wife_monthly_income:,.0f}): Partial offset applied while maintaining living standard parity.")

    # 6. ENFORCE MANDATORY NRI INTERIM FLOOR (Kulwinder Kumar v. Seema, Vimal Ravi)
    nri_floor = 20000.0 if facts.children_count == 0 else 35000.0
    if total_recommended_maintenance < nri_floor:
        total_recommended_maintenance = nri_floor
        logs.append(f"Mandatory NRI Interim Maintenance Floor applied (Kulwinder Kumar benchmark): Set at minimum ₹{nri_floor:,.0f}/month.")
        authorities.append({
            "precedent": "Kulwinder Kumar v. Seema, 2025 SCC OnLine All 8563",
            "court": "Allahabad High Court",
            "principle": "NRI husbands residing abroad cannot claim zero earnings; mandatory interim floor of ₹20,000 to ₹35,000/pm enforced.",
            "app_tag": "NRI_QUANTUM_BENCHMARK"
        })

    # Inflation revision 3-year projection (Mohd. Fazil Qureshi)
    projected_3yr_quantum = total_recommended_maintenance * 1.18 # ~6% annual CPI compounding

    # 7. COERCIVE ENFORCEMENT & PASSPORT IMPOUNDMENT ADVISORY (Fathima Majida v. Union of India)
    coercive_measures = [
        "Request mandatory filing of Supreme Court Assets & Liabilities Affidavit (Rajnesh v. Neha).",
        "Section 91 CrPC summons to MEA / overseas employer for salary verification.",
        "Look Out Circular (LOC) application via Ministry of Home Affairs to prevent flight upon arrival in India."
    ]
    if facts.spouse_abroad:
        coercive_measures.append("Application under Section 10(3)(h) Passports Act 1967 before Magistrate for impounding/revocation of Indian passport upon default.")
        authorities.append({
            "precedent": "Fathima Majida M. v. Union of India, 2026 SCC OnLine Ker 4182",
            "court": "Kerala High Court",
            "principle": "Magistrate empowered to order passport impoundment and cancellation of travel clearance against NRI maintenance defaulters.",
            "app_tag": "FOREIGN_DIVORCE_SETTLEMENT"
        })

    return {
        "status": "success",
        "disqualified": disqualified,
        "disqualification_reason": disqualification_reason,
        "foreign_decree_valid_in_india": foreign_decree_valid,
        "adverse_inference_applied": adverse_inference_applied,
        "currency": curr,
        "exchange_rate_to_inr": rate,
        "imputed_or_disclosed_gross_foreign_salary": gross_foreign_salary,
        "foreign_living_cost_deduction_pct": "50%",
        "net_disposable_foreign_surplus_monthly": net_foreign_disposable,
        "net_disposable_inr_monthly": round(net_disposable_inr),
        "calculated_monthly_maintenance_inr": round(total_recommended_maintenance),
        "projected_3yr_indexed_maintenance_inr": round(projected_3yr_quantum),
        "interim_floor_enforced": total_recommended_maintenance == nri_floor,
        "coercive_remedies": coercive_measures,
        "statutory_provisions": [
            "Section 125 CrPC / Section 144 BNSS (Monthly Maintenance)",
            "Section 24 Hindu Marriage Act (Interim Maintenance & Overseas Litigation Costs)",
            "Section 25 Hindu Marriage Act (Permanent Alimony / Lifetime Capitalized Settlement)",
            "Section 12, 18, 19, 20 Protection of Women from Domestic Violence Act 2005",
            "Section 10(3)(h) Passports Act 1967 (Impoundment of Defaulter's Passport)"
        ],
        "judicial_precedents": authorities,
        "audit_logs": logs
    }

if __name__ == "__main__":
    test_facts = NRIFacts(
        claimant="wife",
        spouse_abroad=True,
        spouse_country="uae",
        undisclosed_income=True,
        lifestyle_tier="tech/managerial",
        children_count=1,
        children_education_monthly=10000.0,
        foreign_decree_obtained=True,
        decree_submitted_to=False,
        domestic_violence=True
    )
    import pprint
    res = evaluate_nri_case(test_facts)
    pprint.pprint(res)
