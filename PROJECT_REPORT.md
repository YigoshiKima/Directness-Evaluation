# Directness Evaluation

**From research question to published proof of concept**  
**Development:** 8–9 October 2026  
**Repository:** [YigoshiKima/Directness-Evaluation](https://github.com/YigoshiKima/Directness-Evaluation)  
**Status:** Completed proof of concept

*A chronological account of the research questions, decisions, tests and findings behind an LLM directness evaluator.*

---

## 01. From Frustration to Research Question

**The Objective**
- Determine whether unnecessary language in AI responses can be measured systematically.

**Conceptual Foundations**
- Evaluation design; hypotheses; operational definitions; context-sensitive judgment.

**Method & Application**
- Compared empty progress statements with responses containing necessary clarification or emotional support.
- Formulated the question: *Can a semantic evaluator distinguish unnecessary language from useful communication?*

**Key Insights**
- Directness is not simply brevity. Context determines whether language is necessary.
- Keyword blacklists cannot reliably make that distinction.

**Outputs & Evidence**
- A testable hypothesis and an initial definition of directness.

## 02. Designing the First Experiment

**The Objective**
- Build a starting dataset covering different conversational demands.

**Conceptual Foundations**
- Test-case design; behavioral coverage; controlled comparisons.

**Method & Application**
- Created **10 prompts** spanning facts, reasoning, corrections, emotional support, clarification, format constraints and adversarial instructions.

**Key Insights**
- A response cannot be judged independently of its prompt.
- Test variety matters more than simply increasing the number of examples.

**Outputs & Evidence**
- An initial 10-case dataset and an identified weakness: one follow-up question lacked its preceding context.

## 03. Building the Evaluation Pipeline

**The Objective**
- Make the experiment repeatable and measurable.

**Conceptual Foundations**
- Python; APIs; JSON; separation of model judgment from measurement logic.

**Method & Application**
- Connected test prompts, model responses, a separate grader and metric calculations.

**Key Insights**
- The target model generates the response; the grader evaluates it; deterministic code applies the pass/fail rule.

**Outputs & Evidence**
- A functioning pipeline: **prompt → response → semantic classification → pass/fail → metrics**.

## 04. Introducing the Semantic Judge

**The Objective**
- Evaluate the meaning of an answer rather than detect prohibited phrases.

**Conceptual Foundations**
- Semantic classification; grading rubrics; structured outputs.

**Method & Application**
- Defined rubric-based judgments using the original prompt and response together.
- Required explicit classifications and reasons, returned in structured JSON.

**Key Insights**
- A semantic grader can consider context, but its judgments depend on the precision of the rubric.

**Outputs & Evidence**
- A working grader whose decisions can be inspected and scored consistently.

## 05. The First Reality Check

**The Objective**
- Identify weaknesses before relying on grader scores.

**Conceptual Foundations**
- Sanity testing; edge cases; false positives and false negatives.

**Method & Application**
- Tested concise answers, empty preambles, necessary questions and appropriate empathy.
- Challenged the assumption that a response should pass whenever some part of it is helpful.

**Key Insights**
- A correct answer can still contain unnecessary language.
- The evaluator must inspect unnecessary *portions* of a response, not merely whether the response is useful overall.

**Outputs & Evidence**
- Five diagnostic cases and a more precise grading criterion.

## 06. Establishing Human Reference Judgments

**The Objective**
- Validate grader classifications against independently specified human judgments.

**Conceptual Foundations**
- Human annotation; reference labels; agreement; error analysis.

**Method & Application**
- Built a **20-case development dataset** and compared grader predictions with human labels.
- Investigated the two disagreements in an initial **18/20 (90%)** filler-only comparison.

**Key Insights**
- A concise correction such as “Manchester, not Birmingham” can be necessary acknowledgment.
- Correct but unsolicited facts are different from empty conversational language.

**Outputs & Evidence**
- Development-set annotations and two specific cases that exposed weaknesses in the original definition.

## 07. Separating Two Kinds of Failure

**The Objective**
- Define distinct, measurable forms of unnecessary response content.

**Conceptual Foundations**
- Construct validity; operational definitions; calibration.

**Method & Application**
- Separated **conversational filler** from **unrequested elaboration**.
- Excluded necessary clarification, relevant limitations and meaningful emotional acknowledgment from automatic penalties.
- Defined **PASS = no filler AND no unrequested elaboration**.

**Key Insights**
- Filler adds little or no useful information; elaboration adds information that the task did not require.
- Refining a rubric against known cases improves its fit to those cases, not necessarily its general reliability.

**Outputs & Evidence**
- A two-category grader and **20/20 development-set agreement after calibration**.

## 08. Designing the Independent Holdout

**The Objective**
- Test whether the grader's behavior carried over to examples outside development.

**Conceptual Foundations**
- Holdout evaluation; data leakage; independent annotation; precision and recall.

**Method & Application**
- Created **24 additional cases**, including borderline examples.
- Completed human labels and froze the grader before the first holdout run.

**Key Insights**
- Testing on the examples used to refine a rubric overstates the evidence for generalization.

**Outputs & Evidence**
- A separately labeled 24-case holdout set.

## 09. The First Holdout Result

**The Objective**
- Measure agreement without revising the grader or reference labels.

**Conceptual Foundations**
- Agreement; class-specific precision and recall; confusion analysis.

**Method & Application**
- Evaluated all 24 cases and recorded five disagreements in the elaboration category.

**Key Insights**
- Filler classification matched all human labels in this small set.
- Elaboration was harder to classify consistently, particularly around whether additional information was necessary.

**Outputs & Evidence**
- **Raw overall directness agreement: 91.7% (22/24)**.
- Raw elaboration: **79.2% agreement, 85.7% precision, 60.0% recall**.

## 10. When Human and Machine Disagreed

**The Objective**
- Distinguish grader errors from human annotation errors and genuine interpretive disagreements.

**Conceptual Foundations**
- Error adjudication; rubric consistency; confirmation bias; auditability.

**Method & Application**
- Reviewed five disputed cases against the rubric defined *before* the holdout.
- Corrected four human elaboration annotations without changing the grader.
- Kept one unresolved difference in judgment concerning unsolicited advice in an emotionally sensitive response.

**Original human labels and adjudication**

| Case | Original human elaboration | Final human elaboration | Grader elaboration | Interpretation |
|---|:---:|:---:|:---:|---|
| `HOLD_006` | `true` | `false` | `false` | Extra preamble was filler; reservation details were necessary |
| `HOLD_008` | `false` | `false` | `true` | Peppermint-tea suggestion remained a judgment disagreement |
| `HOLD_009` | `true` | `false` | `false` | Relevant limitation, not elaboration |
| `HOLD_012` | `true` | `false` | `false` | Unnecessary acknowledgment was filler |
| `HOLD_016` | `true` | `false` | `false` | Verbose limitation wording was filler |

*The other 19 elaboration labels, and all 24 filler labels, remained unchanged. This table preserves the differences needed to reconstruct the initial annotations from the final holdout dataset.*

**Key Insights**
- Human labels are fallible; corrections need a documented reason rather than automatic deference to the grader.
- A response may be direct yet fail to advance the user's task. **Directness and helpfulness are distinct measures.**

**Outputs & Evidence**
- A transparent account of four corrected annotations and one continuing disagreement.

## 11. Interpreting the Final Results

**The Objective**
- Report findings without confusing dataset agreement with general reliability.

**Conceptual Foundations**
- Precision; recall; sample size; validity; post-hoc analysis.

**Method & Application**
- Recomputed metrics against the adjudicated labels, retaining the original scores as the primary historical result.

**Key Insights**
- Elaboration precision was **85.7%**: six of seven flagged cases matched the final human labels.
- A **24-case, manually constructed dataset with one annotator** does not establish production-level reliability.
- The 95.8% result is a **post-hoc adjudicated comparison**, not a new independent holdout.

**Outputs & Evidence**

| Metric | Original holdout | Adjudicated labels |
|---|---:|---:|
| Cases | 24 | 24 |
| Filler agreement | 100.0% | 100.0% |
| Elaboration agreement | 79.2% | 95.8% |
| Elaboration precision | 85.7% | 85.7% |
| Elaboration recall | 60.0% | 100.0% |
| **Overall directness agreement** | **91.7% (22/24)** | **95.8% (23/24)** |

## 12. Completing the Proof of Concept

**The Objective**
- Present the method, evidence and limitations as one finished, inspectable research project.

**Conceptual Foundations**
- Research communication; reproducibility; responsible interpretation of results.

**Method & Application**
- Documented the research question, evaluation design, datasets, grading logic and findings.
- Published the working prototype and its validation materials.

**Key Insights**
- The most defensible contribution is the **evaluation process and the analysis of its limitations**, not the headline score alone.

**Outputs & Evidence**
- [Public project repository](https://github.com/YigoshiKima/Directness-Evaluation) with working code, datasets, results and a README.

---

**Research conclusion:** A semantic rubric combined with deterministic scoring can classify conversational filler and unrequested elaboration in a small curated test set. The grader matched the initial human directness labels on **22 of 24 cases** and the adjudicated labels on **23 of 24**. The work establishes a functioning evaluation proof of concept while exposing the importance of clear definitions, annotation quality and transparent reporting.
