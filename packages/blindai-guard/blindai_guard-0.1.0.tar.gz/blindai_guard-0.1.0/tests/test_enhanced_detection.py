#!/usr/bin/env python3
"""
Test Phase 2 Implementation
Verify checksum validation, context windows, and confidence scoring
"""

from blind_ai.core.detection.enhanced_detector import EnhancedPatternDetector, EnhancedDetectionResult
from blind_ai.core.detection.patterns import ALL_PII_PATTERNS

def test_checksum_validation():
    """Test checksum validation for various patterns"""
    print("🧪 Testing Checksum Validation...")
    print()
    
    from blind_ai.core.detection.patterns.validators import (
        luhn_check,
        validate_pesel,
        validate_portuguese_nif,
        validate_south_africa_id,
        validate_israeli_id,
        validate_routing_number
    )
    
    tests = [
        ("Luhn (Credit Card)", luhn_check, "4532123456789010", True),
        ("Luhn (Invalid)", luhn_check, "1234567890123456", False),
        ("Polish PESEL", validate_pesel, "44051401359", True),
        ("Portuguese NIF", validate_portuguese_nif, "123456789", True),
        ("South Africa ID", validate_south_africa_id, "9001015009087", True),
        ("Israeli ID", validate_israeli_id, "123456782", True),
        ("US Routing", validate_routing_number, "021000021", True),
        ("US Routing (Invalid)", validate_routing_number, "123456789", False),
    ]
    
    passed = 0
    for name, func, value, expected in tests:
        result = func(value)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {name}: {value} → {result} (expected {expected})")
        if result == expected:
            passed += 1
    
    print()
    print(f"  Passed: {passed}/{len(tests)}")
    print()
    return passed == len(tests)


def test_context_windows():
    """Test context window matching"""
    print("🧪 Testing Context Windows...")
    print()
    
    from blind_ai.core.detection.patterns.validators import validate_pattern_with_context
    
    tests = [
        ("SSN with context", "Please enter your SSN: 123-45-6789", 24, 35, ["ssn", "social"], True),
        ("SSN without context", "Random number: 123-45-6789", 15, 26, ["ssn", "social"], False),
        ("Credit card with context", "Card number: 4532-1234-5678-9010", 13, 32, ["card", "credit"], True),
        ("No keywords required", "Any text here", 0, 5, [], True),
    ]
    
    passed = 0
    for name, text, start, end, keywords, expected in tests:
        result = validate_pattern_with_context(text, start, end, keywords, 50)
        status = "✅" if result == expected else "❌"
        print(f"  {status} {name}: {result} (expected {expected})")
        if result == expected:
            passed += 1
    
    print()
    print(f"  Passed: {passed}/{len(tests)}")
    print()
    return passed == len(tests)


def test_confidence_scoring():
    """Test confidence scoring"""
    print("🧪 Testing Confidence Scoring...")
    print()
    
    detector = EnhancedPatternDetector(context_window_size=50)
    
    # Find SSN pattern
    ssn_pattern = next((p for p in ALL_PII_PATTERNS if p.name == "ssn"), None)
    if not ssn_pattern:
        print("  ❌ SSN pattern not found")
        return False
    
    tests = [
        ("SSN with context + valid", "Please enter your SSN: 123-45-6789", 0.7, 1.0),
        ("SSN without context", "Random: 123-45-6789", 0.4, 0.7),
    ]
    
    passed = 0
    for name, text, min_conf, max_conf in tests:
        results = detector.detect_with_confidence(text, ssn_pattern, "pii")
        if results:
            confidence = results[0].confidence
            in_range = min_conf <= confidence <= max_conf
            status = "✅" if in_range else "❌"
            print(f"  {status} {name}: confidence={confidence:.2f} (expected {min_conf}-{max_conf})")
            if in_range:
                passed += 1
        else:
            print(f"  ❌ {name}: No match found")
    
    print()
    print(f"  Passed: {passed}/{len(tests)}")
    print()
    return passed == len(tests)


def test_enhanced_detection():
    """Test full enhanced detection pipeline"""
    print("🧪 Testing Enhanced Detection Pipeline...")
    print()
    
    detector = EnhancedPatternDetector()
    
    # Test text with multiple PII types
    text = """
    Customer Information:
    - SSN: 123-45-6789
    - Credit Card: 4532-1234-5678-9010
    - Email: customer@example.com
    - Random number: 987-65-4321
    """
    
    all_results = []
    for pattern in ALL_PII_PATTERNS[:10]:  # Test first 10 patterns
        results = detector.detect_with_confidence(text, pattern, "pii")
        all_results.extend(results)
    
    print(f"  Found {len(all_results)} matches")
    print()
    
    for result in all_results:
        print(f"  📍 {result.pattern_name}:")
        print(f"     Text: {result.matched_text}")
        print(f"     Confidence: {result.confidence:.2f}")
        print(f"     Validation: {'✅' if result.validation_passed else '❌'}")
        print(f"     Context: {'✅' if result.context_matched else '❌'}")
        print()
    
    return len(all_results) > 0


def main():
    print("=" * 60)
    print("🧪 PHASE 2 TESTING")
    print("=" * 60)
    print()
    
    results = []
    
    # Test 1: Checksum validation
    results.append(("Checksum Validation", test_checksum_validation()))
    
    # Test 2: Context windows
    results.append(("Context Windows", test_context_windows()))
    
    # Test 3: Confidence scoring
    results.append(("Confidence Scoring", test_confidence_scoring()))
    
    # Test 4: Enhanced detection
    results.append(("Enhanced Detection", test_enhanced_detection()))
    
    print("=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    print()
    
    for name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"  {status}: {name}")
    
    print()
    total_passed = sum(1 for _, passed in results if passed)
    print(f"  Total: {total_passed}/{len(results)} tests passed")
    print()
    
    if total_passed == len(results):
        print("🎉 ALL TESTS PASSED!")
    else:
        print("⚠️  Some tests failed")
    
    return total_passed == len(results)


if __name__ == "__main__":
    success = main()
    exit(0 if success else 1)
