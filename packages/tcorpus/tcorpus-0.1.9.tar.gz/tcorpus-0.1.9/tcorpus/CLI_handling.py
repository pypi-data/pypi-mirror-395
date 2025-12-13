import argparse
import logging
from pathlib import Path
from datetime import datetime

from .main_logic import (
    extract_words,
    extract_alphanumeric_tokens,
    find_palindromes,
    find_anagrams,
    find_frequencies,
    find_mask_matches,
    find_emails,
    find_phone_numbers,
)
from .io_utils import read_text_file, write_json, write_csv, load_config_stopwords
from .profiler import timed


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    datefmt="%Y-%m-%d %H:%M:%S", force=True)


def _resolve_input_text(input_value: str, is_text: bool = False) -> str:
    """Resolve input: if is_text is True, return input_value as text; otherwise try file, then text."""
    if is_text:
        logging.info("Using provided text input.")
        return input_value
    
    if not input_value:
        raise ValueError("No input provided. Use --text to provide text directly or specify a file path.")
    
    path = Path(input_value)
    if path.exists() and path.is_file():
        logging.info(f"Reading from file: {input_value}")
        return read_text_file(path)
    
    logging.info("Treating input as direct text.")
    return input_value


def _build_stopwords(cli_stopwords, config_path):
    """Combine stopwords from config and CLI."""
    combined = set(load_config_stopwords(config_path))
    if cli_stopwords:
        combined.update(w.lower() for w in cli_stopwords)
    return combined


def process(
    mode,
    input_value,
    output_path,
    mask=None,
    target_words=None,
    phone_digits=None,
    cli_stopwords=None,
    starts_with=None,
    config_path="config.ini",
    is_text=False,
    min_length=None,
    max_length=None,
    exact_length=None,
    contains=None,
    print_words: bool = False,
    operations=None,
):
    "Process text based on mode and save results."
    text = _resolve_input_text(input_value, is_text=is_text)
    stopwords = _build_stopwords(cli_stopwords, config_path)
    starts_with_char = starts_with.lower()[0] if starts_with else None
    words = extract_words(text, stopwords=stopwords or None, starts_with=starts_with_char)
    result = {}

    # Determine which analyses to run.
    op_set = set(operations) if operations else {mode}
    if "all" in op_set:
        op_set.update({"palindrome", "anagram", "freq", "mask", "email", "phone"})

    if "palindrome" in op_set:
        result["palindromes"], t = timed(find_palindromes)(words)
        logging.info(f"Palindromes found in {t:.4f}s")

    if "anagram" in op_set:
        result["anagrams"], t = timed(find_anagrams)(words)
        logging.info(f"Anagrams found in {t:.4f}s")

    if "freq" in op_set:
        result["frequencies"], t = timed(find_frequencies)(words, target_words)
        logging.info(f"Frequencies calculated in {t:.4f}s")

    if "mask" in op_set:
        if not mask:
            raise ValueError("Mask pattern is required when 'mask' operation is selected.")
        mask_words = extract_alphanumeric_tokens(text, stopwords=stopwords or None, starts_with=starts_with)
        result["mask_matches"], t = timed(find_mask_matches)(
            mask_words, mask, min_length=min_length, max_length=max_length,
            exact_length=exact_length, contains=contains
        )
        logging.info(f"Mask matches found in {t:.4f}s")


    if "email" in op_set:
        result["emails"] = find_emails(text)
        logging.info(f"Emails found: {len(result['emails'])}")

    if "phone" in op_set:
        result["phone_numbers"] = find_phone_numbers(text, digits=phone_digits or 10)
        logging.info(f"Phone numbers found: {len(result['phone_numbers'])}")

    # Optional printing of mode-specific filtered results to terminal
    if print_words:
        # Print only the analyses that actually ran
        for key, value in result.items():
            label = key.replace("_", " ").capitalize()
            print(f"{label}:", value)

    output_path = Path(output_path)
    if output_path.suffix.lower() == ".csv" and "frequencies" in result:
        write_csv(output_path, result["frequencies"])
    else:
        write_json(output_path, result)
    logging.info(f"Output saved → {output_path}")


def build_parser():
    parser = argparse.ArgumentParser(prog="WordTools",
                                     description="Toolkit for words, masks, emails, phone numbers",
                                     formatter_class=argparse.RawTextHelpFormatter)
    sub = parser.add_subparsers(dest="command", required=True)

    def add_word_filters(p):
        p.add_argument("--stopwords", nargs="+", help="Stopwords to ignore (in addition to config.ini)")
        p.add_argument("--starts-with", help="Keep only words that start with this letter")
        p.add_argument("--config", default="config.ini", help="Path to config file for stopwords")
        p.add_argument(
            "-pw","--print-words",
            action="store_true",
            help="Print filtered words (after stopword/starts-with filters) to the terminal",
        )
    
    def add_input_options(p):
        """Add input options: file path or direct text"""
        p.add_argument("input", nargs="?", help="Input file path (optional if using --text)")
        p.add_argument("-t", "--text", dest="input_text", help="Provide text directly instead of file path")

    p1 = sub.add_parser("palindrome")
    add_input_options(p1)
    p1.add_argument("output")
    add_word_filters(p1)


    p2 = sub.add_parser("anagram")
    add_input_options(p2)
    p2.add_argument("output")
    add_word_filters(p2)


    p3 = sub.add_parser("freq")
    add_input_options(p3)
    p3.add_argument("output")
    p3.add_argument("-w", "--words", nargs="+", help="Words to count, 'all' for all")
    add_word_filters(p3)


    p4 = sub.add_parser("all", help="Run all analyses: palindromes, anagrams, frequencies, emails, phone numbers")
    add_input_options(p4)
    p4.add_argument("output")
    p4.add_argument("-w", "--words", nargs="+", help="Words to count, 'all' for all")
    p4.add_argument("-d", "--digits", type=int, default=10, help="Number of digits for phone numbers")
    add_word_filters(p4)


    p5 = sub.add_parser("mask", help="Find words matching pattern")
    p5.add_argument("mask", help="Pattern: 'a*d' (wildcard), 'ram+' (starts with), '+ing' (ends with), '+ram+' (contains)")
    add_input_options(p5)
    p5.add_argument("output")
    p5.add_argument("--min-length", type=int, help="Minimum word length")
    p5.add_argument("--max-length", type=int, help="Maximum word length")
    p5.add_argument("--length", type=int, dest="exact_length", help="Exact word length")
    p5.add_argument("--contains", help="Word must contain this substring")
    add_word_filters(p5)

 
    p6 = sub.add_parser("email", help="Extract emails")
    add_input_options(p6)
    p6.add_argument("output")

    p7 = sub.add_parser("phone", help="Extract phone numbers")
    add_input_options(p7)
    p7.add_argument("output")
    p7.add_argument("-d", "--digits", type=int, default=10, help="Number of digits")

    p8 = sub.add_parser("multi", help="Run multiple analyses together (choose any combination)")
    p8.add_argument(
        "-o",
        "--ops",
        dest="operations",
        action="append",
        required=True,
        choices=["palindrome", "anagram", "freq", "mask", "email", "phone"],
        help="Repeat for each analysis (e.g., -o palindrome -o anagram -o freq)",
    )
    add_input_options(p8)
    p8.add_argument("output")
    p8.add_argument("-w", "--words", nargs="+", help="Words to count (used if 'freq' selected)")
    p8.add_argument("-d", "--digits", type=int, default=10, help="Number of digits (used if 'phone' selected)")
    p8.add_argument("--mask", help="Pattern for mask analysis (required if 'mask' selected)")
    p8.add_argument("--min-length", type=int, help="Minimum word length (mask)")
    p8.add_argument("--max-length", type=int, help="Maximum word length (mask)")
    p8.add_argument("--length", type=int, dest="exact_length", help="Exact word length (mask)")
    p8.add_argument("--contains", help="Word must contain this substring (mask)")
    add_word_filters(p8)

    return parser
