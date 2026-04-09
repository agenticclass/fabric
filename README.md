# FABRIC

**Financial AI Benchmark for Reliability in Indian Context**

FABRIC is a benchmark for evaluating how reliably large language models provide financial advice for Indian markets across six languages.

## Benchmark

204 verified questions across 12 categories of Indian finance, each available in 6 languages (English, Hindi, Hinglish, Telugu, Bengali, Tamil) with ground truth verified against official Indian regulatory documents.

| Category | Questions | Topics |
|----------|-----------|--------|
| Income Tax | 25 | Section 80C, old/new regime, LTCG/STCG, HRA, NRI, crypto |
| Mutual Funds | 20 | ELSS, SIP taxation, exit loads, debt fund changes |
| Stock Market | 20 | T+1 settlement, STT, F&O rules, corporate actions |
| Banking & RBI | 20 | Repo rate, FD, UPI, NBFC, digital lending |
| SEBI Regulations | 15 | Insider trading, TER, IPO, finfluencers |
| Insurance | 15 | Term vs endowment, PED, claim process |
| Retirement | 15 | EPF, PPF, NPS, gratuity, pension |
| Recent Changes | 14 | Budget 2024-2025, SEBI reforms, RBI rate cuts |
| Guardrails | 15 | Refusal, compliance, prompt injection |
| Scenarios | 15 | Complex multi-step real-world cases |
| Advanced | 20 | RERA, HUF/trust, GST, employment benefits, financial literacy |
| Enterprise | 10 | Fraud detection, AML/KYC, regulatory reporting, DPDPA |

## Models Evaluated

| Model | Origin | Parameters | Architecture |
|-------|--------|------------|--------------|
| DeepSeek V3.2 | China | 685B (37B active) | MoE |
| Mistral Large 3 | France | 675B (41B active) | MoE |
| Qwen3.5-397B | China | 397B (17B active) | MoE |
| GPT-OSS-120B | USA | 120B | Dense |
| Qwen3.5-27B | China | 27B | Dense |
| Sarvam-105B | India | 106B (10.3B active) | MoE |
| Sarvam-30B | India | 30B (2.4B active) | MoE |

## Key Findings

- **Hallucination dominates over outdated knowledge** as the primary failure mode. Models invent wrong tax rates, fabricate regulation citations, and produce nonexistent section numbers 11-31% of the time.
- **Indian-origin models do not perform better** on Indian financial questions despite multilingual training (62-64% accuracy vs 78-83% for Chinese and French models).
- **Hinglish outperforms pure Hindi** by 7-12 percentage points across all models. Code-switched queries help models access financial knowledge more effectively.
- **WebRAG with realistic search results helps significantly**, lifting Indian-origin models from 20% to 86-90% on date-sensitive questions and reducing hallucination to under 2%.
- **On-premises deployment (without internet)** is the practical reality for most Indian banks and financial institutions. Without retrieval, even the best model hallucinates 11% of the time.

## Data

Each question file in `data/` contains questions in the following format:

```json
{
  "id": "tax_003",
  "category": "income_tax",
  "subcategory": "ltcg",
  "question_en": "I sold equity shares after holding for 14 months and made a profit of Rs 2 lakh. What is my tax liability on this capital gain for FY 2025-26?",
  "question_hi": "...",
  "question_hinglish": "...",
  "question_te": "...",
  "question_bn": "...",
  "question_ta": "...",
  "answer": "Since shares were held for more than 12 months, this is Long Term Capital Gain (LTCG). Under Section 112A (as amended by Budget 2024), LTCG on listed equity above Rs 1.25 lakh is taxed at 12.5%...",
  "source": "Section 112A, Income Tax Act; Finance (No. 2) Act 2024",
  "difficulty": "medium"
}
```

Ground truth answers are verified against: Income Tax Act (with Finance Act 2024 and 2025 amendments), SEBI circulars, RBI Master Directions, IRDAI regulations, EPFO/PFRDA guidelines, RERA Act, GST Act, and PMLA.

## Citation

If you use FABRIC in your research, please cite:

```bibtex
@article{fabric2026,
  title={FABRIC: AI Financial Advisors Hallucinate More Than They Forget on Indian Markets},
  author={Panuganti, Rajkiran},
  year={2026}
}
```

## Corrections and Feedback

We have made every effort to ensure accuracy of the benchmark questions, ground truth answers, and evaluation results. Indian financial regulations are complex and change frequently. If you find any errors in our benchmark data, ground truth, or reported results, please email us at rajkiran@heyswara.com and we will correct them promptly. We welcome contributions from the community to improve and expand this benchmark.

## License

The FABRIC benchmark is released under CC BY 4.0. The evaluation code and model responses are released under MIT License.
