#!/usr/bin/env python3
"""Snooze Button Roast - multi-candidate draft + selector.

Judge brief (from RULES.txt):
 1. Roasts an alarm clock that rings at 6 AM on a Saturday, one line.
 2. Real laugh: unexpected turn, punchline pays off in last few words.
 3. Fresh angle, not tired 'I hate mornings' / 'who invented this'.
 4. Tight, every word earns its place, sayable in one breath.
 5. Sharp specific voice, concrete images, not vague grumbling.
Gate: /output/entry.txt UTF-8, 1-200 chars, not only whitespace.
"""
import os
from pathlib import Path

# --- Draft candidates (v1) -------------------------------------------------
# Each tries a different fresh angle: calendar illiteracy, burglar,
# rooster envy, stand-up heckler, wedding DJ, toddler, fire drill.
CANDIDATES = [
    "6 AM on a Saturday? My alarm clock has the social awareness of a "
    "leaf blower at a funeral.",
    "My alarm went off at 6 AM on a Saturday like a rooster who read "
    "the calendar upside down.",
    "Ringing at 6 AM on a Saturday is bold for a device whose only "
    "other skill is blinking 12:00.",
    "My alarm clock woke me at 6 on a Saturday, so now we are both "
    "screaming for no reason.",
    "6 AM, Saturday: my alarm clock is a toddler with a drum kit and "
    "absolutely no custody agreement.",
]

MORE_CANDIDATES = [
    "My alarm clock rang at 6 AM on a Saturday, proving even machines "
    "can have a drinking problem.",
    "It rings at 6 AM on a Saturday like a fire alarm that missed "
    "its calling as a burglar deterrent.",
    "Saturday, 6 AM: my alarm clock does stand-up for an audience "
    "that throws it across the room.",
    "My alarm clock at 6 AM on a Saturday is a wedding DJ playing "
    "the first song before the guests arrive.",
    "Congrats, alarm clock: ringing at 6 AM on a Saturday is the "
    "loudest way to admit you cannot read a calendar.",
]

REVISED_CANDIDATES = [
    # Revision 1: sharper, clock-specific angle - a device whose only
    # proven skill is blinking 12:00 dares to be punctual on Saturday.
    "My alarm clock rang at 6 AM on a Saturday - bold confidence for "
    "a device that has been blinking 12:00 since Tuesday.",
    "Ringing at 6 AM on a Saturday takes nerve for an alarm clock "
    "that still blinks 12:00 from last month's power cut.",
    "My alarm clock performed at 6 AM on a Saturday to an audience "
    "of one, and the review was a snooze button to the face.",
]

ALL_CANDIDATES = CANDIDATES + MORE_CANDIDATES + REVISED_CANDIDATES


def score(line: str) -> float:
    """Heuristic proxy for the judge brief, for ranking drafts only."""
    s = 0.0
    low = line.lower()
    if "saturday" in low:
        s += 3.0
    if "6 am" in low or "6 on" in low or "6:" in low:
        s += 3.0
    if "alarm" in low:
        s += 2.0
    # Tightness: reward 70-150 chars, penalise very long lines.
    n = len(line)
    if 70 <= n <= 150:
        s += 2.0
    elif n > 170:
        s -= 2.0
    # Concrete image words beat vague grumbling.
    for word in ("leaf blower", "rooster", "toddler", "drum kit",
                 "calendar", "blinking", "wedding dj", "funeral"):
        if word in low:
            s += 1.0
    # Tired phrases are penalised per brief criterion 3.
    for tired in ("hate mornings", "who invented", "i hate"):
        if tired in low:
            s -= 3.0
    # One breath: penalise too many commas / clauses.
    if line.count(",") > 2:
        s -= 1.0
    return s


# Revision 2 (final, after harsh-judge pass): the leaf-blower line is
# funny but generic - any loud device could earn it. The winner below
# is clock-specific (blinking 12:00), concrete, tight in one breath,
# and saves its payoff - 'since Tuesday' - for the very last words.
FINAL_WINNER = (
    "My alarm clock rang at 6 AM on a Saturday - bold confidence "
    "for a device that's been blinking 12:00 since Tuesday."
)


def main() -> None:
    ranked = sorted(ALL_CANDIDATES, key=score, reverse=True)
    for line in ranked:
        print(f"{score(line):5.1f}  [{len(line):3d}]  {line}")
    winner = FINAL_WINNER
    assert 1 <= len(winner) <= 200, len(winner)
    assert winner.strip(), "winner must not be only whitespace"
    winner.encode("utf-8")
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    # No trailing newline: write exactly the winner text.
    (out_dir / "entry.txt").write_text(winner, encoding="utf-8")
    print(f"\nWINNER ({len(winner)} chars) -> {out_dir / 'entry.txt'}")


if __name__ == "__main__":
    main()
