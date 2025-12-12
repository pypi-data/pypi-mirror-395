from pathlib import Path
from shutil import rmtree


def clear_directory(directory_path: str):
    """Empty the specified directory (remove all files and directories)."""
    dir_path = Path(directory_path)
    if dir_path.exists() and dir_path.is_dir():
        for item in dir_path.iterdir():
            if item.is_dir():
                rmtree(item)
            else:
                item.unlink()


def str_to_bool(value: str) -> bool:
    value = value.strip().lower()
    if value in ('y', 'yes', 't', 'true', 'on', '1'):
        return True
    if value in ('n', 'no', 'f', 'false', 'off', '0'):
        return False
    raise ValueError(f"invalid truth value {value!r}")


def separate(names, described):
    expected = []
    unexpected = []
    for name in sorted(names, key=str):
        (
            expected
            if name in described
            else unexpected
        ).append(name)
    return expected, unexpected


def reduce(name):
    return ''.join(c for c in str(name) if c.isascii and c.isalnum()).lower().rstrip('s')


def interpret(expected, unexpected, described):
    interpretation = {}
    if unexpected:
        reduced_described = {
            reduce(name): name
            for name in described
            if name not in expected
        }
        for name in unexpected:
            reduced_name = reduce(name)
            if reduced_name in reduced_described:
                interpretation[name] = reduced_described.pop(reduced_name)
    return interpretation


def separate_and_interpret(names, described):
    expected, unexpected = separate(names, described)
    interpretation = interpret(expected, unexpected, described)
    return expected, unexpected, interpretation


def display_interpretation(expected, unexpected, interpretation, display_function=print, legend='', indent=''):
    if unexpected:
        if legend:
            legend += ' '
        if interpretation:
            display_function(f"{indent}Interpreted {legend}names:")
            for k, v in interpretation.items():
                display_function(f"{indent}  '{k}' → '{v}'")
        if expected or interpretation:
            unidentified = [k for k in unexpected if k not in interpretation]
            if unidentified:
                display_function(f"{indent}Unidentified {legend}names:")
                for k in unidentified:
                    display_function(f"{indent}  '{k}'")
        else:
            display_function(f"{indent}No {legend}name identified")


def separate_and_interpret_with_display(names, described, display_function=print, legend='', indent=''):
    expected, unexpected, interpretation = separate_and_interpret(names, described)
    display_interpretation(expected, unexpected, interpretation, display_function, legend, indent)
    return expected, unexpected, interpretation
