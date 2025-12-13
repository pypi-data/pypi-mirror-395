# Author: Timur Ulyahin, https://github.com/ucomru
# License: MIT – provided "as-is" without any warranty or liability
# Copyright: (c) 2024 Timur Ulyahin

"""
Name normalization utilities for puber.

Provides norm_name() to format personal names as 'Familia I.O.' or
'Familia I.' and handle common variations (spacing, fused initials,
inverted order).
"""

from __future__ import annotations
import re


# base character classes (RU/EN)
PAT_INIT_RU = r"[\u0410-\u042F\u0401]"  # Cyrillic [А–ЯЁ]
PAT_INIT_EN = r"[A-Z]"
PAT_INIT = rf"(?:{PAT_INIT_RU}|{PAT_INIT_EN})"

# familia patterns (support ALL CAPS and hyphenated)
PAT_FAM_RU = r"[\u0410-\u042F\u0401][\u0410-\u044F\u0401\u0451\-]+"  # Cyrillic [А–Я, а–я, Ёё]
PAT_FAM_EN = r"[A-Z][A-Za-z\-]+"
PAT_FAM = rf"(?:{PAT_FAM_RU}|{PAT_FAM_EN})"

# compiled regexes
RE_CANON_2 = re.compile(rf"^(?P<fam>{PAT_FAM}) (?P<i1>{PAT_INIT})\.(?P<i2>{PAT_INIT})\.$")
RE_CANON_1 = re.compile(rf"^(?P<fam>{PAT_FAM}) (?P<i1>{PAT_INIT})\.$")

# Firstname + Initial + Familia
RE_FIRST_INIT_FAM = re.compile(
    rf"^(?P<first>{PAT_FAM})\s+(?P<i1>{PAT_INIT})\.\s+(?P<fam>{PAT_FAM})$"
)

# initials first (dots/spaces): "T.M. Familia", "T. M. Familia", "T M Familia", "T Familia"
RE_INIT_FIRST = re.compile(
    rf"^(?P<i1>{PAT_INIT})\.?\s*(?:(?P<i2>{PAT_INIT})\.?)?\s+(?P<fam>{PAT_FAM})$"
)

# familia + initials in near-canonical forms
RE_FAM_INITS = re.compile(
    rf"^(?P<fam>{PAT_FAM})\s+(?P<init>({PAT_INIT}\.\s*{PAT_INIT}\.|{PAT_INIT}\.))$"
)

# familia + name (+ patronymic): no dots → compress to initials
RE_FAM_FIRST = re.compile(rf"^(?P<fam>{PAT_FAM}) (?P<i1>{PAT_FAM})(?: (?P<i2>{PAT_FAM}))?$")

# familia + initials, missing final dot on second
RE_MISS_DOT = re.compile(rf"^(?P<fam>{PAT_FAM})\s+(?P<i1>{PAT_INIT})\.(?P<i2>{PAT_INIT})?$")

# familia + initials without dots
RE_NO_DOTS = re.compile(rf"^(?P<fam>{PAT_FAM}) (?P<i1>{PAT_INIT})(?: (?P<i2>{PAT_INIT}))?$")


def _cap(s: str) -> str:
    """Title-case hyphenated familias."""
    return "-".join(w[:1].upper() + w[1:].lower() for w in s.split("-"))


def norm_name(s: str) -> str:
    """
    Normalize a personal name to the canonical form 'Familia I.O.' or 'Familia I.'.

    Args:
        s (str): Raw name string (Cyrillic or Latin, any case, optional commas/spaces).

    Returns:
        str: Normalized name in canonical form with title-cased familia and compact initials.
    """
    if not s:
        return ""

    # comma pre-normalization: handle "Name [Patronymic], Familia" and "I[.][I[.]], Familia"
    raw = s.strip()
    if raw.count(",") == 1:
        left, right = (p.strip() for p in raw.split(",", 1))
        left_words = left.split()
        right_words = right.split()

        # helper: is left an initials chunk like "T.", "T.M.", "T. M.", "T M"
        _left_compact = re.sub(r"\s+", "", left)
        is_left_initials = bool(re.fullmatch(rf"{PAT_INIT}\.?({PAT_INIT}\.?)?", _left_compact))

        # invert only if right is a single token AND (left has 2+ tokens OR is initials)
        if right and len(right_words) == 1 and (len(left_words) >= 2 or is_left_initials):
            s = f"{right} {left}"
        else:
            s = raw
    else:
        s = raw

    # standard cleanup
    s = re.sub(r"[,\u00A0]+", " ", s)
    s = re.sub(r"\s+", " ", s)

    # fix compact "M.Ivanova" → "M. Ivanova"
    s = re.sub(rf"(?<!{PAT_INIT})(?P<i>{PAT_INIT})\.(?P<fam>{PAT_FAM})", r"\g<i>. \g<fam>", s)

    m = RE_CANON_2.fullmatch(s)
    if m:
        return f"{_cap(m['fam'])} {m['i1']}.{m['i2']}."
    m = RE_CANON_1.fullmatch(s)
    if m:
        return f"{_cap(m['fam'])} {m['i1']}."

    # Firstname + Initial + Familia  →  Familia F.I.
    m = RE_FIRST_INIT_FAM.fullmatch(s)
    if m:
        fam = _cap(m["fam"])
        first = m["first"]
        i1 = first[0].upper()
        i2 = m["i1"]
        return f"{fam} {i1}.{i2}."

    # initials first (inversion)
    m = RE_INIT_FIRST.fullmatch(s)
    if m:
        i1, i2, fam = m["i1"], m["i2"], _cap(m["fam"])
        return f"{fam} {i1}.{i2}." if i2 else f"{fam} {i1}."

    # familia + (almost) canonical initials
    m = RE_FAM_INITS.fullmatch(s)
    if m:
        fam = _cap(m["fam"])
        init = m["init"].replace(" ", "")
        init = re.sub(rf"^({PAT_INIT})\.$", r"\1.", init)
        init = re.sub(rf"^({PAT_INIT})\.({PAT_INIT})\.?$", r"\1.\2.", init)
        return f"{fam} {init}"

    # familia + name (+ patronymic) → compress to initials
    m = RE_FAM_FIRST.fullmatch(s)
    if m:
        fam = _cap(m["fam"])
        t1, t2 = m["i1"], m["i2"]
        if t1 and "." not in t1 and (t2 is None or "." not in t2):
            ini = t1[0].upper() + "."
            if t2:
                ini += t2[0].upper() + "."
            return f"{fam} {ini}"

    # familia + initials with missing final dot
    m = RE_MISS_DOT.fullmatch(s)
    if m:
        fam = _cap(m["fam"])
        i1, i2 = m["i1"], m["i2"]
        return f"{fam} {i1}.{i2}." if i2 else f"{fam} {i1}."

    # familia + initials w/o dots
    m = RE_NO_DOTS.fullmatch(s)
    if m:
        fam = _cap(m["fam"])
        i1, i2 = m["i1"], m["i2"]
        return f"{fam} {i1}.{i2}." if i2 else f"{fam} {i1}."

    # fallback: take first token as familia, build initials from first letters of next tokens
    parts = s.split()
    if parts:
        fam = _cap(parts[0])
        tail_words = parts[1:]
        initials = []
        for w in tail_words:
            m0 = re.match(PAT_INIT, w)  # first letter only
            if m0:
                initials.append(m0.group(0).upper())
            if len(initials) == 2:
                break
        if initials:
            ini = ".".join(initials) + "."
            return f"{fam} {ini}"
        return fam
    return ""
