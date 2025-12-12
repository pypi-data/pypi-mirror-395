from __future__ import annotations


def option_build_short_name(option_name: str) -> str:
    words = option_name.split("_")
    return "".join(word[0].lower() for word in words if word)
