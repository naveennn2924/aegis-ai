import sys
from pathlib import Path

# Add project root to Python path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

import json
from orchestration.workflow import run_workflow


def run_regression_tests():
    with open("evaluation/golden_dataset.json", "r") as f:
        tests = json.load(f)

    failures = []

    for test in tests:
        user_input = test["input"]
        expected_intent = test["expected_intent"]
        min_quality = test["min_quality_score"]

        print(f"\n🔍 Testing input: '{user_input}'")

        result = run_workflow({"message": user_input})
        system_result = result["result"]

        actual_intent = system_result.get("intent")
        review = system_result.get("review", {})
        quality_score = review.get("quality_score", 0.0)

        # ---- Intent check ----
        if isinstance(expected_intent, list):
            if actual_intent not in expected_intent:
                failures.append(
                    f"Intent mismatch for '{user_input}' "
                    f"(expected one of {expected_intent}, got '{actual_intent}')"
                )
        else:
            if actual_intent != expected_intent:
                failures.append(
                    f"Intent mismatch for '{user_input}' "
                    f"(expected '{expected_intent}', got '{actual_intent}')"
                )

        # ---- Quality score check ----
        if quality_score < min_quality:
            failures.append(
                f"Quality regression for '{user_input}' "
                f"(score {quality_score} < min {min_quality})"
            )

        print(f"   Intent: {actual_intent}")
        print(f"   Quality score: {quality_score}")

    print("\n" + "=" * 50)

    if failures:
        print("❌ REGRESSION DETECTED")
        for failure in failures:
            print("-", failure)
    else:
        print("✅ All regression tests passed")


if __name__ == "__main__":
    run_regression_tests()
