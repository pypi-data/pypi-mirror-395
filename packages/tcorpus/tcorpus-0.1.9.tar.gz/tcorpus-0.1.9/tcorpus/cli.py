from .CLI_handling import build_parser, process


def main():
    """Main CLI entry point."""
    args = build_parser().parse_args()

    input_text = getattr(args, "input_text", None)
    input_value = input_text if input_text is not None else getattr(args, "input", None)
    is_text = input_text is not None

    kwargs = {
        "is_text": is_text,
        "cli_stopwords": getattr(args, "stopwords", None),
        "starts_with": getattr(args, "starts_with", None),
        "config_path": getattr(args, "config", "config.ini"),
    }

    if args.command in ("mask", "multi"):
        kwargs["mask"] = getattr(args, "mask", None)
        kwargs["min_length"] = getattr(args, "min_length", None)
        kwargs["max_length"] = getattr(args, "max_length", None)
        kwargs["exact_length"] = getattr(args, "exact_length", None)
        kwargs["contains"] = getattr(args, "contains", None)

    if args.command in ("freq", "all", "multi"):
        kwargs["target_words"] = getattr(args, "words", None)

    if args.command in ("phone", "all", "multi"):
        kwargs["phone_digits"] = getattr(args, "digits", 10)

    if args.command == "multi":
        kwargs["operations"] = args.operations

    # Optional: print filtered words list to terminal
    kwargs["print_words"] = getattr(args, "print_words", False)

    process(args.command, input_value, args.output, **kwargs)


if __name__ == "__main__":
    main()


