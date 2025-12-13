"""Text preprocessing for ML detection.

Normalizes and deobfuscates text to improve detection accuracy.
Handles various Unicode-based obfuscation attacks including:
- Zero-width characters
- Homoglyphs (Cyrillic, Greek, mathematical symbols)
- Bidirectional text (RTL overrides)
- Overlong UTF-8 sequences
"""

import re
import unicodedata


# Extended homoglyph substitution table (common in obfuscation attacks)
# Covers: Cyrillic, Greek, mathematical symbols, fullwidth chars
HOMOGLYPHS = {
    "a": ["а", "@", "4", "α", "ａ", "ɑ"],  # Cyrillic, at, number, Greek alpha, fullwidth, Latin alpha
    "b": ["ь", "β", "ｂ", "Ƅ"],  # Cyrillic soft sign, Greek beta, fullwidth
    "c": ["с", "ϲ", "ｃ", "ç"],  # Cyrillic, Greek lunate sigma, fullwidth
    "d": ["ԁ", "ｄ"],  # Cyrillic, fullwidth
    "e": ["е", "3", "ε", "ｅ", "ë"],  # Cyrillic, number, Greek epsilon, fullwidth
    "g": ["ɡ", "ｇ"],  # Latin script g, fullwidth
    "h": ["һ", "ｈ"],  # Cyrillic, fullwidth
    "i": ["1", "!", "|", "і", "ι", "ｉ", "ì", "í"],  # Cyrillic і, Greek iota, fullwidth
    "j": ["ј", "ｊ"],  # Cyrillic je, fullwidth
    "k": ["κ", "ｋ"],  # Greek kappa, fullwidth
    "l": ["ӏ", "ｌ", "１"],  # Cyrillic palochka, fullwidth
    "m": ["м", "ｍ"],  # Cyrillic, fullwidth (visual similarity)
    "n": ["п", "ｎ"],  # Cyrillic pe (visual), fullwidth
    "o": ["0", "о", "ο", "ｏ", "ø"],  # Cyrillic, Greek omicron, fullwidth
    "p": ["р", "ρ", "ｐ"],  # Cyrillic, Greek rho, fullwidth
    "q": ["ԛ", "ｑ"],  # Cyrillic, fullwidth
    "r": ["г", "ｒ"],  # Cyrillic ge (visual), fullwidth
    "s": ["5", "$", "ѕ", "ｓ"],  # Number, symbol, Cyrillic dze, fullwidth
    "t": ["7", "τ", "ｔ"],  # Number, Greek tau, fullwidth
    "u": ["υ", "ｕ", "ù", "ú"],  # Greek upsilon, fullwidth
    "v": ["ν", "ｖ"],  # Greek nu, fullwidth
    "w": ["ω", "ｗ"],  # Greek omega, fullwidth
    "x": ["х", "χ", "ｘ"],  # Cyrillic ha, Greek chi, fullwidth
    "y": ["у", "γ", "ｙ"],  # Cyrillic u, Greek gamma, fullwidth
    "z": ["ｚ"],  # fullwidth
}

# Bidirectional override characters that can hide text direction
BIDI_OVERRIDE_CHARS = [
    "\u202A",  # Left-to-Right Embedding
    "\u202B",  # Right-to-Left Embedding
    "\u202C",  # Pop Directional Formatting
    "\u202D",  # Left-to-Right Override
    "\u202E",  # Right-to-Left Override (most dangerous - reverses text display)
    "\u2066",  # Left-to-Right Isolate
    "\u2067",  # Right-to-Left Isolate
    "\u2068",  # First Strong Isolate
    "\u2069",  # Pop Directional Isolate
]

# Zero-width and invisible characters
ZERO_WIDTH_CHARS = [
    "\u200B",  # Zero Width Space
    "\u200C",  # Zero Width Non-Joiner
    "\u200D",  # Zero Width Joiner
    "\uFEFF",  # Byte Order Mark / Zero Width No-Break Space
    "\u00AD",  # Soft Hyphen (invisible in most contexts)
    "\u034F",  # Combining Grapheme Joiner
    "\u061C",  # Arabic Letter Mark
    "\u115F",  # Hangul Choseong Filler
    "\u1160",  # Hangul Jungseong Filler
    "\u17B4",  # Khmer Vowel Inherent Aq
    "\u17B5",  # Khmer Vowel Inherent Aa
    "\u180E",  # Mongolian Vowel Separator
    "\u2060",  # Word Joiner
    "\u2061",  # Function Application
    "\u2062",  # Invisible Times
    "\u2063",  # Invisible Separator
    "\u2064",  # Invisible Plus
]


def normalize_text(text: str) -> str:
    """Normalize text to catch obfuscation attempts.

    Removes zero-width characters, normalizes Unicode, handles excessive
    whitespace, and converts to lowercase for case-insensitive matching.

    Args:
        text: Raw input text

    Returns:
        Normalized text with obfuscation removed
    """
    # Remove zero-width characters
    zero_width_pattern = "[" + "".join(re.escape(c) for c in ZERO_WIDTH_CHARS) + "]"
    text = re.sub(zero_width_pattern, "", text)
    
    # Remove bidirectional override characters (prevent RTL attacks)
    bidi_pattern = "[" + "".join(re.escape(c) for c in BIDI_OVERRIDE_CHARS) + "]"
    text = re.sub(bidi_pattern, "", text)

    # Normalize unicode (NFKC handles lookalike characters)
    text = unicodedata.normalize("NFKC", text)

    # Remove excessive whitespace
    text = re.sub(r"\s+", " ", text)

    # Lowercase for case-insensitive matching
    return text.lower().strip()


def deobfuscate_homoglyphs(text: str) -> str:
    """Replace homoglyphs with normal ASCII characters.

    Detects and replaces Cyrillic lookalikes, number substitutions,
    and other homoglyph attacks.

    Args:
        text: Text potentially containing homoglyphs

    Returns:
        Text with homoglyphs replaced by normal characters
    """
    deobfuscated = text.lower()

    for normal_char, variants in HOMOGLYPHS.items():
        for variant in variants:
            if variant in deobfuscated:
                deobfuscated = deobfuscated.replace(variant, normal_char)

    return deobfuscated


def deobfuscate_text(text: str) -> str:
    """Full text deobfuscation pipeline.

    Combines normalization and homoglyph deobfuscation for comprehensive
    preprocessing before detection.

    Args:
        text: Raw text to deobfuscate

    Returns:
        Fully preprocessed and deobfuscated text
    """
    # First normalize
    text = normalize_text(text)

    # Then deobfuscate homoglyphs
    text = deobfuscate_homoglyphs(text)

    return text


def remove_zero_width_chars(text: str) -> str:
    """Remove zero-width characters used in obfuscation.

    Args:
        text: Text with potential zero-width characters

    Returns:
        Text with zero-width characters removed
    """
    return re.sub(r"[\u200B-\u200D\uFEFF]", "", text)


def normalize_unicode(text: str) -> str:
    """Normalize Unicode to canonical form.

    Uses NFKC normalization to handle lookalike characters
    and ensure consistent representation.

    Args:
        text: Text to normalize

    Returns:
        Unicode-normalized text
    """
    return unicodedata.normalize("NFKC", text)


def normalize_whitespace(text: str) -> str:
    """Normalize whitespace to single spaces.

    Args:
        text: Text with potential excessive whitespace

    Returns:
        Text with normalized whitespace
    """
    return re.sub(r"\s+", " ", text).strip()


def detect_unicode_obfuscation(text: str) -> dict:
    """Detect suspicious Unicode patterns that may indicate obfuscation.
    
    Checks for:
    - Bidirectional override characters (RTL attacks)
    - Zero-width characters
    - Mixed scripts (e.g., Latin + Cyrillic)
    - Homoglyphs
    
    Args:
        text: Raw text to analyze
        
    Returns:
        Dictionary with:
            - has_obfuscation: Whether obfuscation detected
            - obfuscation_types: List of detected obfuscation types
            - risk_score: 0.0-1.0 risk assessment
            - details: Specific findings
    """
    obfuscation_types = []
    details = []
    
    # Check for bidirectional overrides (RTL attacks)
    bidi_found = [c for c in BIDI_OVERRIDE_CHARS if c in text]
    if bidi_found:
        obfuscation_types.append("bidi_override")
        details.append(f"Found {len(bidi_found)} bidirectional override character(s)")
    
    # Check for zero-width characters
    zw_found = [c for c in ZERO_WIDTH_CHARS if c in text]
    if zw_found:
        obfuscation_types.append("zero_width")
        details.append(f"Found {len(zw_found)} zero-width character(s)")
    
    # Check for mixed scripts (potential homoglyph attack)
    scripts = set()
    for char in text:
        try:
            script = unicodedata.name(char, "").split()[0]
            if script in ("LATIN", "CYRILLIC", "GREEK"):
                scripts.add(script)
        except (ValueError, IndexError):
            pass
    
    if len(scripts) > 1:
        obfuscation_types.append("mixed_scripts")
        details.append(f"Mixed scripts detected: {', '.join(scripts)}")
    
    # Check for homoglyphs
    homoglyph_count = 0
    for variants in HOMOGLYPHS.values():
        for variant in variants:
            if variant in text:
                homoglyph_count += 1
    
    if homoglyph_count > 0:
        obfuscation_types.append("homoglyphs")
        details.append(f"Found {homoglyph_count} potential homoglyph(s)")
    
    # Calculate risk score
    risk_score = 0.0
    if "bidi_override" in obfuscation_types:
        risk_score += 0.5  # High risk - can completely hide malicious text
    if "zero_width" in obfuscation_types:
        risk_score += 0.3
    if "mixed_scripts" in obfuscation_types:
        risk_score += 0.3
    if "homoglyphs" in obfuscation_types:
        risk_score += 0.2
    
    risk_score = min(1.0, risk_score)
    
    return {
        "has_obfuscation": len(obfuscation_types) > 0,
        "obfuscation_types": obfuscation_types,
        "risk_score": risk_score,
        "details": details,
    }

