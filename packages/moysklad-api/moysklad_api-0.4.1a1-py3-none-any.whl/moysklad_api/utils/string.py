def camel_to_slash(camel_str: str) -> str:
    result = ""
    for i, char in enumerate(camel_str):
        if (
            char.isupper()
            and i > 0
            and (i == len(camel_str) - 1 or camel_str[i + 1].islower())
        ):
            result += "/"
        result += char
    return result.lower()
