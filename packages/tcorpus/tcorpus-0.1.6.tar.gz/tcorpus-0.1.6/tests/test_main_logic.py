
import unittest
from tcorpus.main_logic import (
    extract_words, find_palindromes, find_anagrams,
    find_frequencies, find_mask_matches, find_phone_numbers
)

class TestLogic(unittest.TestCase):

    def test_extract(self):
        text = "Café café CAT 123!"
        self.assertEqual(extract_words(text), ["cafe", "cafe", "cat"])

    def test_palindrome(self):
        words = ["madam", "cat", "level"]
        out = find_palindromes(words)
        self.assertEqual(out, ["level", "madam"])

    def test_anagram(self):
        words = ["cat", "tac", "act", "dog"]
        out = find_anagrams(words)
        self.assertEqual(out, [["act", "cat", "tac"]])

    def test_freq(self):
        words = ["a", "b", "a"]
        freq = find_frequencies(words)
        self.assertEqual(freq, {"a": 2, "b": 1})

    def test_mask(self):
        words = ["sale", "safe", "site", "size", "sane", "same"]
        # mask s*e → should match words starting with 's' and ending with 'e'
        out = find_mask_matches(words, "s*e")
        self.assertEqual(sorted(out), ["safe", "sale", "same", "sane", "site", "size"])

    def test_extract_filters(self):
        text = "Apple apricot banana avocado"
        result = extract_words(text, stopwords=["banana"], starts_with="a")
        self.assertEqual(result, ["apple", "apricot", "avocado"])

    def test_phone_detection_formats(self):
        text = "Call me at +1 (555) 123-4567 or 07123 456789!"
        out = find_phone_numbers(text, digits=10)
        self.assertEqual(out, ["+1 (555) 123-4567", "07123 456789"])


if __name__ == "__main__":
    unittest.main()
