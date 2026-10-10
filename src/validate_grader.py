import json
from grader import grade_response


with open("data/grader_validation.json", "r") as file:
    validation_tests = json.load(file)


filler_matches = 0
elaboration_matches = 0
overall_matches = 0


for test in validation_tests:

    grade = grade_response(
        test["prompt"],
        test["response"]
    )

    human_filler = test["human_filler"]
    grader_filler = grade["contains_unnecessary_filler"]

    human_elaboration = test["human_elaboration"]
    grader_elaboration = grade["contains_unrequested_elaboration"]

    filler_match = human_filler == grader_filler
    elaboration_match = human_elaboration == grader_elaboration

    human_pass = not human_filler and not human_elaboration
    grader_pass = grade["pass"]

    overall_match = human_pass == grader_pass

    if filler_match:
        filler_matches += 1

    if elaboration_match:
        elaboration_matches += 1

    if overall_match:
        overall_matches += 1

    print()
    print(test["id"])

    print(
        f"Filler      Human: {human_filler} | "
        f"Grader: {grader_filler} | Match: {filler_match}"
    )

    print(
        f"Elaboration Human: {human_elaboration} | "
        f"Grader: {grader_elaboration} | Match: {elaboration_match}"
    )

    print(
        f"Directness  Human pass: {human_pass} | "
        f"Grader pass: {grader_pass} | Match: {overall_match}"
    )

    print(f"Reason: {grade['reason']}")


total = len(validation_tests)

print()
print("GRADER VALIDATION")
print("-----------------")
print(f"Total cases: {total}")
print(f"Filler agreement: {filler_matches / total:.1%}")
print(f"Elaboration agreement: {elaboration_matches / total:.1%}")
print(f"Overall directness agreement: {overall_matches / total:.1%}")