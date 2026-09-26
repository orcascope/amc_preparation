"""Checking typed answers to open-ended problems.

A lesson lists the accepted answers (for example ["585"] or ["\\frac{3}{4}", "0.75"]).
The student's answer counts as correct when, after normalizing both sides,
it equals one of them as text, or as an exact number (so 3/4, 0.75 and
\\frac{3}{4} all match).
"""
import re
from fractions import Fraction

_FRAC = re.compile(r"\\[dt]?frac\{([^{}]*)\}\{([^{}]*)\}")
_SQRT = re.compile(r"\\sqrt\{([^{}]*)\}")
_FRAC_SHORT = re.compile(r"\\[dt]?frac(\d)(\d)")
_DEGREES = re.compile(r"(\^\(?circ\)?|°|degrees?|deg)$")


def normalize(ans):
    """Lower-case text form with LaTeX, spaces, dollar signs and thousands commas removed."""
    s = str(ans).strip().strip("$").strip()
    s = _SQRT.sub(r"sqrt(\1)", s)  # before fractions, so \frac{\sqrt{2}}{2} works
    s = _FRAC.sub(r"(\1)/(\2)", s)
    s = _FRAC_SHORT.sub(r"(\1)/(\2)", s)  # \frac12
    s = s.replace("√", "sqrt").replace("\\cdot", "*").replace("×", "*").replace("\\pi", "pi").replace("π", "pi")
    s = s.replace("\\left", "").replace("\\right", "").replace("\\,", "").replace("\\!", "")
    s = s.replace("\\", "").replace("{", "(").replace("}", ")")
    s = re.sub(r"(?<=\d),(?=\d{3}(\D|$))", "", s)  # 10,000 -> 10000
    s = re.sub(r"\s+", "", s).lower()
    s = re.sub(r"^\((-?[\w.]+)\)$", r"\1", s)
    s = re.sub(r"sqrt\((\w+)\)", r"sqrt\1", s)  # sqrt(2) and sqrt2 compare equal
    s = re.sub(r"\(([\w.]+)\)(?=/)", r"\1", s)  # (25pi)/(8) -> 25pi/8
    s = re.sub(r"(?<=/)\(([\w.]+)\)", r"\1", s)
    s = re.sub(r"(?<=\d)\*(?=[a-z(])", "", s)  # 2*sqrt3 -> 2sqrt3
    s = _DEGREES.sub("", s)  # 60°, 60 degrees, 60^\circ -> 60
    s = re.sub(r"\^\((\w+)\)", r"^\1", s)  # 5^{38} and 5^(38) -> 5^38
    return s


def as_number(s):
    """Exact value of a plain number, decimal or fraction; None otherwise."""
    m = re.fullmatch(r"(-?\d*\.?\d+)(?:/(-?\d*\.?\d+))?", s)
    if not m:
        return None
    try:
        v = Fraction(m.group(1))
        return v / Fraction(m.group(2)) if m.group(2) else v
    except (ValueError, ZeroDivisionError):
        return None


def matches(given, accepted):
    g = normalize(given)
    if not g:
        return False
    gv = as_number(g)
    for a in accepted:
        n = normalize(a)
        if g == n:
            return True
        if gv is not None and as_number(n) == gv:
            return True
    return False
