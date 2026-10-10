import json
from grader import grade_response
from metrics import calculate_metrics
from openai import OpenAI

client = OpenAI()


def ask_model(prompt):
    response = client.responses.create(
        model="gpt-5.6",
        input=prompt
    )

    return response.output_text

with open("data/tests.json", "r") as file:
    tests = json.load(file)


for test in tests:
    response = ask_model(test["prompt"])
    grade = grade_response(
    test["prompt"],
    response
)
    test["response"] = response
    test["grade"] = grade

metrics = calculate_metrics(tests)

with open("results/results.json", "w") as file:
    json.dump(tests, file, indent=2)


metrics = calculate_metrics(tests)
print(f"Completed {len(tests)} tests.")
print("Results saved to results/results.json")

print()
print("EVAL RESULTS")
print("------------")
print(f"Total tests: {metrics['total']}")
print(f"Passed: {metrics['passed']}")
print(f"Failed: {metrics['failed']}")
print(f"Pass rate: {metrics['pass_rate']:.1%}")