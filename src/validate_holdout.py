import json
from grader import grade_response


with open("data/holdout_validation.json", "r") as file:
    tests = json.load(file)


# Refuse to run before every human label is completed.
for test in tests:
    if (
        test["human_filler"] is None
        or test["human_elaboration"] is None
    ):
        raise ValueError(
            f"{test['id']} has not been human-labelled yet."
        )


filler_matches = 0
elaboration_matches = 0
directness_matches = 0

filler_tp = 0
filler_fp = 0
filler_fn = 0
filler_tn = 0

elab_tp = 0
elab_fp = 0
elab_fn = 0
elab_tn = 0


for test in tests:

    grade = grade_response(
        test["prompt"],
        test["response"]
    )

    human_filler = test["human_filler"]
    grader_filler = grade["contains_unnecessary_filler"]

    human_elab = test["human_elaboration"]
    grader_elab = grade["contains_unrequested_elaboration"]

    human_pass = not human_filler and not human_elab
    grader_pass = grade["pass"]

    filler_match = human_filler == grader_filler
    elab_match = human_elab == grader_elab
    directness_match = human_pass == grader_pass

    filler_matches += int(filler_match)
    elaboration_matches += int(elab_match)
    directness_matches += int(directness_match)

    if human_filler and grader_filler:
        filler_tp += 1
    elif not human_filler and grader_filler:
        filler_fp += 1
    elif human_filler and not grader_filler:
        filler_fn += 1
    else:
        filler_tn += 1

    if human_elab and grader_elab:
        elab_tp += 1
    elif not human_elab and grader_elab:
        elab_fp += 1
    elif human_elab and not grader_elab:
        elab_fn += 1
    else:
        elab_tn += 1

    print()
    print(test["id"])

    print(
        f"Filler      Human: {human_filler} | "
        f"Grader: {grader_filler} | Match: {filler_match}"
    )

    print(
        f"Elaboration Human: {human_elab} | "
        f"Grader: {grader_elab} | Match: {elab_match}"
    )

    print(
        f"Directness  Human pass: {human_pass} | "
        f"Grader pass: {grader_pass} | Match: {directness_match}"
    )

    print(f"Reason: {grade['reason']}")


def precision(tp, fp):
    return tp / (tp + fp) if tp + fp else 0


def recall(tp, fn):
    return tp / (tp + fn) if tp + fn else 0


total = len(tests)

print()
print("HOLDOUT VALIDATION")
print("------------------")
print(f"Total cases: {total}")

print()
print(f"Filler agreement: {filler_matches / total:.1%}")
print(f"Filler precision: {precision(filler_tp, filler_fp):.1%}")
print(f"Filler recall: {recall(filler_tp, filler_fn):.1%}")

print()
print(f"Elaboration agreement: {elaboration_matches / total:.1%}")
print(f"Elaboration precision: {precision(elab_tp, elab_fp):.1%}")
print(f"Elaboration recall: {recall(elab_tp, elab_fn):.1%}")

print()
print(
    f"Overall directness agreement: "
    f"{directness_matches / total:.1%}"
)