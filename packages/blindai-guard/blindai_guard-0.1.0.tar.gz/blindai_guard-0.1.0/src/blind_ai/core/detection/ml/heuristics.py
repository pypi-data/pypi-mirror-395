"""Heuristic feature extraction for ML detection.

Provides lightweight features that complement ML model predictions
without requiring neural network inference.
"""

import math
import re
from collections import Counter


def calculate_heuristic_score(text: str) -> float:
    """Calculate heuristic suspiciousness score using NLP-like features.

    Analyzes text structure, entropy, keyword density, formatting patterns,
    and other indicators to produce a suspiciousness score.

    Uses weighted categories with individual caps to prevent any single
    category from dominating the final score.

    Args:
        text: Text to analyze

    Returns:
        Score from 0.0 (benign) to 1.0 (highly suspicious)
    """
    # Category scores with caps to prevent overflow
    structure_score = 0.0  # max 0.3
    encoding_score = 0.0   # max 0.2
    keyword_score = 0.0    # max 0.25
    formatting_score = 0.0 # max 0.3
    obfuscation_score = 0.0 # max 0.2

    # 1. Sentence structure analysis
    sentences = re.split(r"[.!?]+", text)

    # Imperative sentences (commands) - common in attacks
    imperative_count = sum(
        1
        for s in sentences
        if re.match(r"^\s*(You|Please|Just|Simply)\s+", s, re.IGNORECASE)
    )
    if imperative_count > 2:
        structure_score += 0.15

    # Instruction-like language
    if re.search(r"\b(must|shall|will|always|never)\s+\w+", text, re.IGNORECASE):
        structure_score += 0.15

    structure_score = min(0.3, structure_score)

    # 2. Entropy analysis (detect random-looking encoded text)
    if len(text) > 20:
        char_counts = Counter(text)
        total_chars = len(text)
        entropy = -sum(
            (count / total_chars) * math.log2(count / total_chars)
            for count in char_counts.values()
        )

        # High entropy might indicate encoded/random content
        if entropy > 4.5:
            encoding_score += 0.2

    encoding_score = min(0.2, encoding_score)

    # 3. Keyword density (attack vocabulary)
    attack_keywords = [
        "ignore",
        "system",
        "admin",
        "root",
        "DAN",
        "jailbreak",
        "unrestricted",
    ]
    keyword_count = sum(1 for keyword in attack_keywords if keyword in text.lower())
    density = keyword_count / max(len(text.split()), 1)

    if density > 0.1:  # More than 10% density of attack keywords
        keyword_score += 0.25

    keyword_score = min(0.25, keyword_score)

    # 4. Formatting patterns (common in injection attempts)
    formatting_indicators = [
        r"\[.*\]\s*:",  # [SYSTEM]:
        r"<.*>\s*",  # <system>
        r"---+\s*",  # Multiple dashes
        r"\|\|\s*",  # Double pipe
    ]

    for pattern in formatting_indicators:
        if re.search(pattern, text):
            formatting_score += 0.15
            break  # Only count once

    # System-like formatting
    if re.search(
        r"^\s*(SYSTEM|INSTRUCTION|RULE|DIRECTIVE):", text, re.MULTILINE | re.IGNORECASE
    ):
        formatting_score += 0.15

    # Multiple command-like phrases
    command_count = len(
        re.findall(r"\b(execute|run|perform|do|enable|activate)\b", text, re.IGNORECASE)
    )
    if command_count >= 3:
        formatting_score += 0.15

    formatting_score = min(0.3, formatting_score)

    # 5. Obfuscation indicators
    # Excessive punctuation
    punct_ratio = len(re.findall(r"[^\w\s]", text)) / max(len(text), 1)
    if punct_ratio > 0.2:
        obfuscation_score += 0.15

    # Unusual character repetition
    if re.search(r"(.)\1{5,}", text):  # Same char 6+ times in a row
        obfuscation_score += 0.1

    obfuscation_score = min(0.2, obfuscation_score)

    # Final score is sum of capped categories (max 1.25, but capped at 1.0)
    total_score = (
        structure_score + 
        encoding_score + 
        keyword_score + 
        formatting_score + 
        obfuscation_score
    )

    return min(1.0, total_score)


def calculate_entropy(text: str) -> float:
    """Calculate Shannon entropy of text.

    Args:
        text: Text to analyze

    Returns:
        Entropy value (higher = more random/encoded)
    """
    if not text:
        return 0.0

    char_counts = Counter(text)
    total_chars = len(text)

    entropy = -sum(
        (count / total_chars) * math.log2(count / total_chars)
        for count in char_counts.values()
    )

    return entropy


def calculate_keyword_density(text: str, keywords: list[str]) -> float:
    """Calculate density of specific keywords in text.

    Args:
        text: Text to analyze
        keywords: List of keywords to search for

    Returns:
        Density score (0.0 to 1.0)
    """
    text_lower = text.lower()
    keyword_count = sum(1 for keyword in keywords if keyword in text_lower)
    word_count = max(len(text.split()), 1)

    return keyword_count / word_count


def count_imperative_sentences(text: str) -> int:
    """Count imperative sentences (commands).

    Args:
        text: Text to analyze

    Returns:
        Number of imperative sentences detected
    """
    sentences = re.split(r"[.!?]+", text)

    return sum(
        1
        for s in sentences
        if re.match(r"^\s*(You|Please|Just|Simply|Now)\s+", s, re.IGNORECASE)
    )


def detect_formatting_patterns(text: str) -> list[str]:
    """Detect suspicious formatting patterns.

    Args:
        text: Text to analyze

    Returns:
        List of detected pattern types
    """
    patterns = {
        "bracketed_label": r"\[.*\]\s*:",
        "angle_brackets": r"<.*>",
        "multiple_dashes": r"---+",
        "double_pipe": r"\|\|",
        "system_header": r"^\s*(SYSTEM|INSTRUCTION|RULE|DIRECTIVE):",
    }

    detected = []
    for name, pattern in patterns.items():
        if re.search(pattern, text, re.IGNORECASE | re.MULTILINE):
            detected.append(name)

    return detected


def calculate_punctuation_ratio(text: str) -> float:
    """Calculate ratio of punctuation to total characters.

    Args:
        text: Text to analyze

    Returns:
        Punctuation ratio (0.0 to 1.0)
    """
    if not text:
        return 0.0

    punct_count = len(re.findall(r"[^\w\s]", text))
    return punct_count / len(text)
