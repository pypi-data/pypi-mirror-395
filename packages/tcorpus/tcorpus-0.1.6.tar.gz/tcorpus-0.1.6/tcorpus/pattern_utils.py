import re

def mask_to_regex(mask: str) -> str:
    # cat → cat, c_t → c.t, c??t → c..t
    pattern = mask.replace("_", ".").replace("?", ".")
    return f"^{pattern}$"


def mask_match(word: str, mask: str) -> bool:
    regex = mask_to_regex(mask)
    return re.fullmatch(regex, word) is not None
