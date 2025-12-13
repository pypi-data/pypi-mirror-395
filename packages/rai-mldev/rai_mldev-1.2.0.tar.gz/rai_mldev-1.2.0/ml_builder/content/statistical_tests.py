"""
Statistical test explanations content for ML Builder.

Contains test explanations and interpretation guides for various
statistical tests used in feature analysis.
"""

from typing import Dict

# Base explanations for different test types
TEST_EXPLANATIONS = {
    "chi2": {
        "test": """
            **Chi-square Test (For Category vs Category)**
            - Helps understand if two categorical variables are related
            - Example: Is there a connection between color preference and gender?
            - Like asking if the patterns we see are real or just by chance
        """,
        "chi2": """
            **Chi-square Value:**
            - Measures how different the actual patterns are from what we'd expect by chance
            - Like measuring the gap between what we see and what we'd expect if there was no relationship
            - Bigger number = bigger difference from random chance
            - Example: If we see Chi² = 0, the pattern is exactly what we'd expect by chance
            - Example: If we see Chi² = 10, there's a bigger gap from random chance
        """
    },
    "t_test": {
        "test": """
            **Independent T-test (For Yes/No vs Numbers)**
            - Compares averages between two groups
            - Example: Do people who exercise regularly weigh different from those who don't?
            - Helps decide if the difference between groups is real
        """,
        "statistic": """
            **T Statistic:**
            - Think of it as the strength of the difference we found
            - Bigger number = stronger evidence of a real difference
            - Small number = difference might be just random chance
            - Values above 2 or below -2 usually suggest important differences
            - The sign (+ or -) shows which group has the higher average
        """
    },
    "anova": {
        "test": """
            **ANOVA (For Multiple Groups vs Numbers)**
            - Like T-test but for more than two groups
            - Example: Do people from different cities have different income levels?
            - Helps spot differences across multiple groups
        """,
        "statistic": """
            **F Statistic:**
            - Used in ANOVA tests (comparing multiple groups)
            - Like T-statistic but for more than two groups
            - Bigger number = stronger evidence of differences between groups
            - Small number = groups are probably similar
            - Can never be negative (always 0 or positive)
        """
    },
    "pearson": {
        "test": """
            **Pearson Correlation (For Number vs Number)**
            - Shows if two numbers move together
            - Ranges from -1 (opposite movement) to +1 (same movement)
            - Example: As height increases, does weight tend to increase too?
        """,
        "statistic": """
            **Correlation Coefficient:**
            - Shows strength and direction of relationship
            - +1: Perfect positive relationship (both increase together)
            - -1: Perfect negative relationship (one up, other down)
            - 0: No relationship
            - Example: 0.7 is a strong positive relationship
            - Example: -0.3 is a moderate negative relationship
        """
    }
}

# Common explanations for values that appear in multiple tests
COMMON_EXPLANATIONS = {
    "p_value": """
        **P Value (Probability Value):**
        - The chance that what we see is just random luck
        - Less than 0.05 (5%) = We're pretty confident it's a real pattern
        - More than 0.05 = Could just be random chance
        - Think of it like a weather forecast: 5% chance of being wrong
    """,
    "dof": """
        **Degrees of Freedom:**
        - Technical value that helps calculate probability
        - Larger values mean more data points were used
        - Helps determine how reliable the results are
        - Higher is generally better (more data = more reliable)
    """,
    "effect_size": """
        **Effect Size:**
        - Shows how big the difference or relationship is
        - Like measuring the size of a wave, not just if there is a wave
        - Small effect: Tiny but maybe still important (around 0.2)
        - Medium effect: Notable difference (around 0.5)
        - Large effect: Big, obvious difference (0.8 or larger)
    """
}

# Map test names to standardized keys
TEST_NAME_MAP = {
    "independent t-test": "t_test",
    "independent t test": "t_test",
    "t-test": "t_test",
    "t test": "t_test",
    "pearson": "pearson",
    "pearson correlation": "pearson",
    "pearsonr": "pearson",
    "correlation": "pearson",
    "chi2": "chi2",
    "chi-square": "chi2",
    "chi square": "chi2",
    "chi-square test": "chi2",
    "chi square test": "chi2",
    "chi-square test of independence": "chi2",
    "chi square test of independence": "chi2",
    "chisquare": "chi2",
    "chi": "chi2",
    "anova": "anova",
    "one-way anova": "anova",
    "one way anova": "anova",
    "f-test": "anova",
    "f test": "anova"
}

def get_statistical_explanation(test_type: str, values: Dict[str, float]) -> Dict[str, str]:
    """Get explanation for specific statistical test and its values."""

    # Clean up test type string
    test_type = test_type.lower().strip().replace("_", " ")

    # Map test names to standardized keys
    mapped_test_type = TEST_NAME_MAP.get(test_type, test_type)

    # Build explanation based on test type and available values
    explanation = {
        "method": TEST_EXPLANATIONS.get(mapped_test_type, {}).get("test", "Test explanation not available"),
        "interpretation": ""
    }

    interpretations = []

    # Add test-specific statistic explanation if available
    if "statistic" in values or "chi2" in values:
        stat_key = "chi2" if mapped_test_type == "chi2" else "statistic"
        if mapped_test_type in TEST_EXPLANATIONS:
            stat_explanation = TEST_EXPLANATIONS[mapped_test_type].get(stat_key, "")
            interpretations.append(stat_explanation)

    # Add common value explanations if present in values
    for key in values:
        if key in COMMON_EXPLANATIONS:
            common_explanation = COMMON_EXPLANATIONS[key]
            interpretations.append(common_explanation)

    explanation["interpretation"] = "\n\n".join([interp for interp in interpretations if interp])

    return explanation