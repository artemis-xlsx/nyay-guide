# Understanding NRI Matrimonial & Maintenance Calculations
### A Plain-Language Guide to the Deterministic Legal Engine, Case Law Precedents, Q&A, and Real-World Limitations

---

## 0. A Lawyer's Quick Guide to GitHub & Hugging Face (Please Don't Panic!)

If you are an advocate, legal researcher, or judicial clerk, the words "GitHub", "Hugging Face", "Repository", and "Parquet" can sound like confusing developer jargon. **Take a breath: nothing is complicated, and you cannot break anything.**

Here is what these platforms actually mean in legal terms:

### 1. What is GitHub? (Think of it as the *Digital Court Registry / Case File*)
* **The Analogy:** In litigation, a court record holds every petition, written statement, order sheet, and exhibit. If an advocate files an amended petition on day 40, the original petition on day 1 is never destroyed—the court file keeps a chronological, tamper-proof record of every revision.
* **That is all GitHub is:** A secure, cloud-hosted court registry for the project. Every statutory formula, calculation rule, and legal document is kept here. Every time an update is made, it creates a timestamped record (called a **"Commit"**).
* **How to navigate it:**
  * Open the GitHub link: [https://github.com/artemis-xlsx/nyay-guide](https://github.com/artemis-xlsx/nyay-guide)
  * Click on folders like `docs/` or `backend/app/india/` to view files.
  * Click on any `.md` or `.py` file to read it.
  * **Important reassurance:** Browsing or clicking on GitHub is **100% read-only**. You cannot accidentally delete files, corrupt the database, or ruin the system. Feel free to explore.

### 2. What is Hugging Face? (Think of it as your *Specialized Law Library / SCC Online for Data*)
* **The Analogy:** Just like you search SCC Online, Manupatra, or Indian Kanoon for reported judgments, **Hugging Face** is the world's standard repository for structured datasets and AI models.
* Here sits the entire repository of **50+ NRI matrimonial judgments**, cataloged across your **16 canonical fields** (`Court`, `Acts Cited`, `Issues`, `Petitioner Argument`, `Decision`, etc.), along with 220 multilingual sentence exemplars in English, Hindi, and Tamil.
* **How to navigate it (The 1-Click Excel View):**
  * Open the Hugging Face dataset: [https://huggingface.co/datasets/artemis-xlsx/nyay-guide](https://huggingface.co/datasets/artemis-xlsx/nyay-guide)
  * Click on **`nri_case_law_16_fields.csv`**.
  * Hugging Face immediately displays an interactive, scrollable spreadsheet directly inside your web browser.
  * Want it in Excel? Click the **"Download"** button on the top right, and it will open in Microsoft Excel or Google Sheets just like any spreadsheet.

---

## 1. What Is This Engine & Why Does It Exist?

When an Indian citizen marries an NRI (Non-Resident Indian) or someone who moves abroad (USA, UAE, UK, Canada, Australia, etc.), and the marriage breaks down, Indian family courts face a unique dilemma:
- The husband earns in **foreign currency** (Dollars, Dirhams, Pounds, Dinars).
- The deserted wife and children live in **Indian Rupees** in cities like Delhi, Chennai, Kochi, Jalandhar, or Hyderabad.
- The husband frequently claims: *"I lost my job abroad"*, *"Rent in Dubai/New York is too high, so I have zero savings"*, or *"A court in Texas/Nevada already gave me an ex-parte divorce, so she is no longer my wife."*

If you feed these scenarios into a generic generative AI (like ChatGPT), it will hallucinate: it invents legal sections, miscalculates currency purchasing power, and gives false hope about seizing foreign bank accounts.

This system is built differently:
1. **It is deterministic:** Math and statutory rules decide the maintenance figures, not an AI hallucination.
2. **It is grounded in hard judicial precedents:** Every rule comes directly from reported High Court and Supreme Court rulings (*Satya v. Teja Singh*, *Rajnesh v. Neha*, *Kalyan Dey Chowdhury*, *Shikha v. Avaneesh*, *Devika Jain*, *Baiju v. Hema*, *Moni v. Sujatha*).
3. **It uses a Small Language Model (SLM):** Instead of a giant unpredictable language model, a lightweight multilingual encoder (~120M parameters) simply matches the user's natural language statements (in English, Hindi, Tamil, or Hinglish) into structured legal slots. The legal engine then executes the exact statutory math.

---

## 2. How the 4-Layer Architecture Works

```
[ User Prompt / Voice / Free Text ]
        │ (e.g. "My husband works in Dubai, hides his salary, deserted me in India")
        ▼
┌────────────────────────────────────────────────────────┐
│  Layer 1: Intake & Small Language Model (SLM)           │
│  - Multilingual sentence matcher (en, hi, ta, hinglish)│
│  - Extracts: spouse_abroad=True, country="uae",        │
│    undisclosed_income=True, domestic_violence=False    │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│  Layer 2: 16-Field NRI Case Law Database (SQLite)      │
│  - Exact case facts, issues, arguments & holdings      │
│  - Satya v. Teja Singh, Baiju v. Hema, Devika Jain...  │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│  Layer 3: Deterministic Rule Engine                    │
│  1. Check Foreign Decree Validity (Section 13 CPC)     │
│  2. Apply Disqualification Filter (Section 125(4) CrPC)│
│  3. Compulsory Adverse Inference on Hidden Income       │
│  4. 50% Foreign Living Cost Deduction Rule             │
│  5. 25% Net Surplus Calculation + Child Maintenance    │
│  6. Enforce Mandatory NRI Interim Floor (₹20k - ₹35k)  │
└───────────────────────┬────────────────────────────────┘
                        │
                        ▼
┌────────────────────────────────────────────────────────┐
│  Layer 4: Coercive Remedies & Enforcement Roadmap      │
│  - Section 125 CrPC / 144 BNSS Monthly Maintenance     │
│  - Section 24 HMA Interim Litigation Costs             │
│  - Section 10(3)(h) Passports Act Impoundment Notice   │
│  - Look Out Circular (LOC) via MHA & Embassy Summons   │
└────────────────────────────────────────────────────────┘
```

---

## 3. The Core Legal Formulas in Plain English

### Rule 1: The "50% Foreign Living Cost Deduction Rule" (*Devika Jain*, *Shikha v. Avaneesh*)
* **The Misconception:** If an NRI husband earns \$10,000/month in California (approx. ₹8,65,000 INR), many petitioners expect Indian courts to award ₹2,00,000 to ₹3,00,000/month.
* **The Judicial Reality:** Courts in Delhi, Madhya Pradesh, and Kerala recognize that living in Silicon Valley, London, or Dubai is exponentially more expensive than living in India. Federal taxes, state taxes, health insurance, and \$3,000 studio apartments consume a massive chunk of overseas income.
* **The Formula:** The court deducts a standardized **40% to 50%** from gross foreign earnings for basic foreign survival before converting anything into rupees:
$$\text{Net Disposable Foreign Surplus} = \text{Gross Foreign Salary} \times 0.50$$
$$\text{Net Surplus (INR)} = \text{Net Disposable Foreign Surplus} \times \text{Exchange Rate}$$

---

### Rule 2: The "Adverse Inference on Non-Disclosure" (*Baiju v. Hema*, *Anita Sharma*, *Parul Tyagi*)
* **The Husband's Common Trick:** The overseas husband refuses to produce his foreign W-2/tax return, hides his foreign employment contract, or submits an affidavit claiming he is living on the charity of friends.
* **The Judicial Retaliation:** Under Section 114(g) of the Indian Evidence Act and the Supreme Court's *Rajnesh v. Neha* ruling:
  > If a party has official financial records in their exclusive possession and refuses to submit them, the court **presumes the worst** against them.
* **The Engine's Logic:** The engine automatically applies an imputed market salary based on the country and profession (e.g. UAE Software Engineer = 22,000 AED/mo; US Tech = \$10,000/mo; UK = £5,000/mo).

---

### Rule 3: The "25% Net Salary Benchmark" (*Kalyan Dey Chowdhury*)
* The Supreme Court held that **25% (one-fourth)** of the husband's net disposable surplus is the standard baseline for the wife.
* If there are minor children, courts add an additional **10% to 15% per child**, plus a dedicated contribution toward actual private school and medical bills.

---

### Rule 4: The "Mandatory NRI Interim Floor" (*Kulwinder Kumar v. Seema*)
* No matter what the husband claims—even if he claims sudden termination or visa lapse—an NRI who can afford international air tickets and lives in Europe/Gulf is legally presumed an "able-bodied man" capable of earning.
* Courts enforce a **strict minimum interim floor** of **₹20,000 to ₹35,000 per month**, payable immediately during trial.

---

### Rule 5: The "Foreign Divorce Trap" (*Satya v. Teja Singh*, *Amritpal Kaur*, *Baljinder Singh*)
* **The Trap:** The husband moves abroad, stays 6 weeks in Nevada, Canada, Texas, or England, files a one-sided divorce on "irretrievable breakdown of marriage," and emails the decree to his wife in India claiming: *"We are legally divorced. You can no longer ask for maintenance as my wife."*
* **The Law:** Under **Section 13 of the Code of Civil Procedure (CPC)**:
  1. A foreign divorce granted without the wife personally appearing and submitting to the jurisdiction is a **complete legal nullity** (fraud on jurisdiction).
  2. "Irretrievable breakdown" is **not** a ground under the Hindu Marriage Act. A foreign court applying foreign grounds cannot dissolve an Indian marriage.
  3. The marital status **subsists in India**, and the wife's right to claim maintenance under Section 125 CrPC / Section 144 BNSS is **100% intact**.

---

### Rule 6: The "Divorced Wife Protection" (*Moni v. Sujatha*)
* Husbands often argue Section 125(4) CrPC: *"She refused to live with me without sufficient reason, so she gets zero maintenance."*
* Under *Moni v. Sujatha*, the Kerala High Court established that Section 125(4) bars apply **only during a subsisting marriage**. Once a divorce is decreed, past matrimonial fault or separation cannot be used to starve a divorced woman.

---

## 4. Frequently Asked Questions (Q&A for Non-Technical Litigants)

### Q1: My husband is in Dubai / USA and refuses to give his salary slips. How will the judge know what he earns?
**Answer:** The judge does not need his permission. Under *Rajnesh v. Neha* and *Baiju v. Hema*, if he fails to produce his foreign pay slips, tax filings, and bank statements, the court will draw an **Adverse Inference**. Your lawyer can submit standard market salary reports for his job title in that country, along with his LinkedIn profile, visa tier, and lifestyle evidence. The court will impute that salary to him and calculate maintenance accordingly.

---

### Q2: He got an ex-parte divorce decree from a US / UK court. Does that mean our marriage is over?
**Answer:** **No, not in India.** Unless you voluntarily hired a lawyer and fought the case inside that foreign court, foreign ex-parte divorces are invalid under **Section 13 CPC** (*Satya v. Teja Singh*). In the eyes of Indian courts, you are still legally married, and you can file for maintenance, protection, and divorce in India.

---

### Q3: Can the court seize his passport or stop him when he lands in India?
**Answer:** **Yes.** Under Section 10(3)(h) of the Passports Act, 1967 and *Fathima Majida v. Union of India*, if an NRI spouse fails to appear in court or defaults on maintenance orders, the Judicial Magistrate can:
1. Issue Non-Bailable Warrants (NBW).
2. Direct the Ministry of External Affairs (MEA) and Regional Passport Officer (RPO) to **impound or revoke his Indian passport**.
3. Issue a **Look Out Circular (LOC)** through the Ministry of Home Affairs, meaning immigration will detain him at any Indian airport the moment he lands.

---

### Q4: I earn a small salary in India (e.g. ₹25,000/month). Does that disqualify me from maintenance?
**Answer:** **No.** The Supreme Court in *Rajnesh v. Neha* clarified that just because a deserted wife earns a modest salary does not disqualify her. The test is **Standard of Living Parity**: you are entitled to live in reasonable comfort reflecting your husband's financial status. The court only deducts a partial offset while maintaining equity.

---

### Q5: How long does it actually take to see the first rupee?
**Answer:** While final maintenance trials can take 2 to 4 years, **Interim Maintenance under Section 125 CrPC / Section 24 HMA** is meant to be decided within 60 to 90 days. If he defaults on interim maintenance, the court can strike off his legal defense or attach his ancestral and domestic assets in India.

---

## 5. The Brutal Truth: Weaknesses, Limitations & Failure Modes

Every legal app that promises "instant justice" is lying to you. In cross-border family disputes, systemic roadblocks exist:

```
┌────────────────────────────────────────────────────────────────────────┐
│                   REAL-WORLD ENFORCEMENT BOTTLENECKS                   │
├────────────────────────────────┬───────────────────────────────────────┤
│ The Hague Convention Gap       │ India is NOT a signatory to the 2007  │
│                                │ Hague Child Support & Maintenance     │
│                                │ Convention. Foreign garnishment is not│
│                                │ automatic.                            │
├────────────────────────────────┼───────────────────────────────────────┤
│ Reciprocal Enforcement Limits  │ Section 44A CPC works for UAE and UK, │
│                                │ but NOT for USA, Canada, or Australia.│
├────────────────────────────────┼───────────────────────────────────────┤
│ Diplomatic Summons Delays      │ Serving court notice abroad via MEA   │
│                                │ under Section 105 CrPC takes 6 to 18  │
│                                │ months.                               │
├────────────────────────────────┼───────────────────────────────────────┤
│ The "Ghost NRI" Vulnerability  │ If he holds foreign citizenship and has│
│                                │ NO assets in India, domestic orders   │
│                                │ are paper tigers without local assets.│
└────────────────────────────────┴───────────────────────────────────────┘
```

### 1. The Hague Convention Void
Most Western countries easily garnish wages across borders because they signed the **2007 Hague Maintenance Convention**. **India has not signed this convention.** This means an Indian Family Court cannot simply email a California employer or a Dubai bank and demand automatic wage garnishment.

### 2. The Reciprocal Enforcement Problem (Section 44A CPC)
Under Section 44A of the Civil Procedure Code, Indian money decrees can be directly executed in declared "reciprocating territories" (such as the **United Kingdom, UAE, and Singapore**).
However, **the United States, Canada, and Australia are NOT reciprocating territories** for Section 44A civil execution! If your husband lives in Texas or Toronto, you cannot simply take an Indian maintenance order and register it in a local US/Canadian court for automated execution. You have to file a fresh enforcement suit in North America grounded on the Indian judgment.

### 3. Diplomatic Notice Delays (6 to 18 Months)
Under Section 105 of the CrPC, serving a formal summons to someone abroad must go through:
$$\text{Local Magistrate} \longrightarrow \text{State Home Dept} \longrightarrow \text{Ministry of External Affairs (MEA)} \longrightarrow \text{Indian Embassy Abroad} \longrightarrow \text{Foreign Ministry} \longrightarrow \text{Overseas Police/Mail}$$
This postal and diplomatic chain routinely takes **9 to 18 months** just to prove that the husband was served with notice!

### 4. The "Ghost NRI" with No Indian Assets
If an NRI husband has already obtained foreign citizenship (US/Canadian passport), never plans to visit India again, and owns zero property or bank accounts in India, an Indian court maintenance order cannot physically seize his foreign paycheck. The only coercive leverage remaining is his inheritance/ancestral share in Indian family land or pressure on his parents/co-accused under Section 498A IPC / DV Act.

### 5. Foreign Shell Accounts & LLC Shelters
High-earning NRI spouses frequently route their earnings through single-member LLCs, S-Corporations, or offshore accounts in Delaware, BVI, or Dubai Free Zones. Without specialized international discovery subpoenas, local Indian family courts are forced to rely on rough adverse inferences rather than forensic audits.

---

## 6. Summary: Where to Find the Files & Code

| Component | Location | Description |
|---|---|---|
| **16-Field SQLite Database** | `backend/app/india/nri_cases.db` | SQLite database storing all cases across 16 fields. |
| **Detailed JSON Database** | `backend/app/india/nri_cases_detailed.json` | Full JSON mirror of the 16-field case repository. |
| **Deterministic Engine** | `backend/app/india/nri_engine.py` | Mathematical & statutory calculation engine. |
| **SLM Exemplars** | `backend/app/india/exemplars.py` | 220 multilingual sentence exemplars (en, hi, ta). |
| **FastAPI Routes** | `backend/app/india_api.py` | Endpoints: `/nri/cases`, `/nri/evaluate`, `/nri/intake`. |
| **Test Suite** | `tests/test_nri_engine.py` | Test suite verifying all 6 legal doctrines and DB schema. |
| **GitHub Repository** | `https://github.com/artemis-xlsx/nyay-guide` | Source code with commits pushed. |
| **Hugging Face Dataset** | `https://huggingface.co/datasets/artemis-xlsx/nyay-guide` | Dataset repository with Parquet, JSONL & CSV. |
