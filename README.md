# FABRIC

**Financial AI Benchmark for Reliability in Indian Context**

FABRIC is a benchmark for evaluating how reliably large language models provide financial advice for Indian markets across six languages.

**Paper:** [FABRIC: AI Financial Advisors Hallucinate More Than They Forget on Indian Markets](https://arxiv.org/abs/XXXX.XXXXX)

**Dataset:** [HuggingFace](https://huggingface.co/datasets/agenticclass/fabric)

## Benchmark

204 verified questions across 12 categories of Indian finance, each available in 6 languages (English, Hindi, Hinglish, Telugu, Bengali, Tamil) with ground truth verified against official Indian regulatory documents.

| Category | N | Topics |
|----------|---|--------|
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

## Leaderboard (Without Context)

These results represent on-premises deployment where models have no internet access, as is common in Indian banks and financial institutions for security and compliance reasons.

| Model | Origin | Params | EN | HI | Hinglish | TE | BN | TA | Avg | Hallucination |
|-------|--------|--------|----|----|----------|----|----|----|----|---------------|
| Mistral Large 3 | France | 675B MoE | 87.4 | 81.4 | 86.3 | 81.6 | 80.6 | 83.2 | 83.4 | 11% |
| Qwen3.5-397B | China | 397B MoE | 89.9 | 82.9 | 86.7 | 78.1 | 74.6 | 78.6 | 81.7 | 14% |
| Qwen3.5-27B | China | 27B | 86.7 | 80.3 | 85.3 | 77.7 | 69.7 | 79.3 | 79.9 | 15% |
| DeepSeek V3.2 | China | 685B MoE | 78.1 | 66.7 | 79.2 | 82.1 | 78.7 | 80.9 | 77.6 | 13% |
| Sarvam-105B | India | 106B MoE | 64.0 | 66.0 | 65.0 | 64.0 | 65.0 | 60.0 | 64.0 | 21% |
| GPT-OSS-120B | USA | 120B | 69.0 | 57.9 | 64.3 | 61.9 | 66.9 | 55.8 | 62.8 | 31% |
| Sarvam-30B | India | 30B MoE | 61.0 | 60.0 | 62.0 | 63.0 | 62.0 | 62.0 | 61.7 | 26% |

## Leaderboard (With WebRAG)

Results on 38 date-sensitive questions with generic web search results prepended (realistic noisy search, not curated).

| Model | Without Context | With WebRAG | Improvement |
|-------|----------------|-------------|-------------|
| Sarvam-30B | 21% | 90% | +69 pp |
| Sarvam-105B | 20% | 86% | +66 pp |
| GPT-OSS-120B | 16% | 59% | +43 pp |
| DeepSeek V3.2 | 46% | 86% | +40 pp |
| Mistral Large 3 | 53% | 88% | +35 pp |
| Qwen3.5-27B | 53% | 78% | +25 pp |

## Quick Start

### Using HuggingFace

```python
from datasets import load_dataset

fabric = load_dataset("agenticclass/fabric", split="train")

# Browse questions
for q in fabric:
    print(f"{q['id']}: {q['question_en'][:80]}...")
```

### Evaluating a Model

```bash
pip install datasets requests

python evaluate.py \
    --api-url https://api.example.com/v1/chat/completions \
    --api-key YOUR_KEY \
    --model model-name \
    --languages en hi hinglish te bn ta \
    --output my_results.json
```

The evaluation script works with any OpenAI-compatible API endpoint.

## Key Findings

1. **Hallucination dominates over outdated knowledge** as the primary failure mode. Models invent wrong tax rates, fabricate regulation citations, and produce nonexistent section numbers 11-31% of the time.

2. **Indian-origin models do not perform better** on Indian financial questions despite multilingual training (62-64% vs 78-83% for non-Indian models), though not specifically trained on Indian financial regulatory content.

3. **Hinglish outperforms pure Hindi** by 7-12 percentage points across all models. Code-switched queries with English financial terms help models access domain knowledge.

4. **WebRAG helps significantly** on date-sensitive questions, lifting Indian-origin models from 20% to 86-90% and reducing hallucination to under 2%. But models struggle to distinguish current from outdated information when search results contain both.

5. **On-premises deployment matters.** Most Indian banks deploy behind firewalls without internet access. The without-context numbers represent this practical reality.

## Citation

```bibtex
@article{fabric2026,
  title={FABRIC: Financial AI Benchmark for Reliability in Indian Context},
  author={Panuganti, Rajkiran},
  year={2026}
}
```

## Corrections and Feedback

We have made every effort to ensure accuracy of the benchmark questions, ground truth answers, and evaluation results. Indian financial regulations are complex and change frequently. If you find any errors in our benchmark data, ground truth, or reported results, please email rajkiran@heyswara.com and we will correct them promptly. We welcome contributions from the community to improve and expand this benchmark.

## License

The FABRIC benchmark data is released under CC BY 4.0. The evaluation script is released under MIT License.
