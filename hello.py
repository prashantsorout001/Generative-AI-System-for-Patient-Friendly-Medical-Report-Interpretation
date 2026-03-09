# Generative AI System for Patient-Friendly Medical Report Interpretation

def interpret_report(report_text):
    """
    Convert complex medical report text into simple patient-friendly explanation.
    (Prototype version)
    """

    explanations = {
        "hypertension": "Your blood pressure is higher than normal.",
        "diabetes": "Your blood sugar levels are elevated.",
        "anemia": "Your body may not have enough healthy red blood cells.",
        "cholesterol": "Your cholesterol levels may be higher than recommended."
    }

    result = []

    for term in explanations:
        if term in report_text.lower():
            result.append(explanations[term])

    if not result:
        return "The report does not contain common conditions. Please consult a doctor for detailed explanation."

    return "\n".join(result)


def main():
    print("=== Patient Friendly Medical Report Interpreter ===")

    report = input("Enter medical report text: ")

    explanation = interpret_report(report)

    print("\nPatient-Friendly Explanation:")
    print(explanation)


if __name__ == "__main__":
    main()