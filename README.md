# Directness Eval

**A proof-of-concept framework for evaluating the directness of AI-generated responses.**

## 1. Research Question

Can an LLM-based grader reliably identify unnecessary conversational language and unrequested elaboration in AI responses?

The project investigates whether response directness can be evaluated using semantic criteria rather than simple keyword matching.

## 2. What Is Being Measured?

The evaluator identifies two independent failure categories:

**Unnecessary conversational filler:** Language that contributes no meaningful information and can be removed without compromising the response.

Examples include empty progress statements, redundant acknowledgements, and unnecessary preambles.

**Unrequested elaboration:** Substantive information that may be accurate or relevant but was not requested and is unnecessary to answer the user's question.

A response passes only when neither failure is detected.

Importantly, the rubric allows necessary clarification, relevant limitations, and contextually appropriate emotional acknowledgement.

## 3. Methodology

The evaluation pipeline follows:

**Test case → AI response → semantic grader → structured classification → deterministic pass/fail → metrics**

The project uses:

- An initial set of 10 prompts across different interaction categories.
- A 20-case development dataset to refine the grading rubric.
- A separate 24-case holdout dataset for evaluation after the rubric was frozen.
- Human annotations for both failure categories.
- Structured JSON output from an LLM-based grader.
- Python code to calculate agreement, precision, and recall.

The grader identifies semantic properties. Python applies the final pass/fail rule.

## 4. Results

| Metric | Adjudicated holdout |
|---|---:|
| Test cases | 24 |
| Filler agreement | 100.0% |
| Filler precision | 100.0% |
| Filler recall | 100.0% |
| Elaboration agreement | 95.8% |
| Elaboration precision | 85.7% |
| Elaboration recall | 100.0% |
| Overall directness agreement | **95.8%** |

The original holdout evaluation produced **91.7% overall agreement**.

After examining disagreements, four human annotation errors were corrected against the existing rubric. Both the original and adjudicated results are reported for transparency.

One disagreement remained: whether an additional suggestion about peppermint tea was unnecessary elaboration in a response to exam anxiety.

## 5. Key Findings

- Semantic classification successfully distinguished conversational filler from substantive information in this small test set.
- Distinguishing unnecessary elaboration from useful contextual information proved more difficult.
- Human labels are themselves subject to ambiguity and error.
- A response can be direct without being helpful or adequately completing the user's task.
- Precise operational definitions are essential for meaningful evaluation.

## 6. Limitations

This is a small proof of concept, not a validated production benchmark.

- Only 24 holdout cases were evaluated.
- Examples were manually constructed rather than sampled from representative real-world model traffic.
- Human annotations were supplied by one annotator.
- The LLM grader may vary between runs.
- The post-hoc adjudicated result must be distinguished from the original holdout score.
- High agreement on this dataset does not establish general reliability across models, tasks, or domains.

## 7. Running the Project

Requirements:

- Python 3
- OpenAI Python SDK
- An OpenAI API key configured as the `OPENAI_API_KEY` environment variable

Install the SDK:

`py -m pip install openai`

Run the initial evaluation:

`py src/run_eval.py`

Run holdout validation:

`py src/validate_holdout.py`

API calls incur usage charges.

## 8. Conclusion

This project demonstrates an end-to-end AI evaluation workflow: defining measurable behavior, designing datasets, building a semantic grader, validating against human judgments, calculating metrics, and analyzing disagreements.

The main outcome is a functioning evaluation proof of concept and an improved understanding of the methodological challenges involved in measuring LLM behavior.