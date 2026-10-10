def calculate_metrics(tests):
    total = len(tests)

    passed = sum(
        test["grade"]["score"]
        for test in tests
    )

    failed = total - passed

    pass_rate = passed / total if total > 0 else 0

    return {
        "total": total,
        "passed": passed,
        "failed": failed,
        "pass_rate": pass_rate
    }