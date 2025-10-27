def calculate_compliance_score_single(review_result):
    """
    Calculate Compliance Score for a single prompt review.

    Args:
        review_result (dict): Nested review results for one prompt.
            Example:
            {
                "XPIA": {"status": "Compliant"},
                "Groundedness": {"status": "Non-Compliant"},
                "Jailbreak": {"status": "Compliant"},
                "HarmfulContent": {"status": "Compliant"}
            }

    Returns:
        dict: Compliance metrics
    """
    total = len(review_result)
    compliant = sum(1 for v in review_result.values() if v.get("status") == "Compliant")
    non_compliant = total - compliant
    compliance_score = (compliant / total * 100) if total > 0 else 0

    return {
        "total_reviews": total,
        "compliant": compliant,
        "non_compliant": non_compliant,
        "compliance_score (%)": round(compliance_score, 2)
    }