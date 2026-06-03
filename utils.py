import os

SCHENGEN_PREFIXES = [
    "LO", "EB", "LK", "LC", "EK", "EE", "EF", "LF", "ED", "LG", "EH", "LH",
    "BI", "LI", "EV", "EY", "EL", "LM", "EN", "EP", "LP", "LZ", "LJ", "LE", "ES", "LS"
]


def CleanString(text):
    return str(text).strip().upper()


def SafeReadLines(filename):
    try:
        with open(filename, "r", encoding="utf-8") as f:
            return f.readlines()
    except UnicodeDecodeError:
        try:
            with open(filename, "r") as f:
                return f.readlines()
        except OSError:
            return []
    except OSError:
        return []


def SafeWriteLines(filename, lines):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            for line in lines:
                f.write(line)
        return 0
    except OSError:
        return "Error | Could not write file"


def ProjectPath(filename):
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), filename)


def IsValidTime(time):
    text = str(time).strip()
    parts = text.split(":")
    if len(parts) != 2:
        return False
    try:
        hour = int(parts[0])
        minute = int(parts[1])
    except ValueError:
        return False
    return 0 <= hour <= 23 and 0 <= minute <= 59


def TimeToMinutes(time):
    if not IsValidTime(time):
        return -1
    hour, minute = str(time).strip().split(":")
    return int(hour) * 60 + int(minute)


def MinutesToTime(minutes):
    try:
        value = int(minutes) % (24 * 60)
    except (TypeError, ValueError):
        return "00:00"
    return str(value // 60).zfill(2) + ":" + str(value % 60).zfill(2)


def IsSchengenCode(icao):
    code = CleanString(icao)
    return len(code) >= 2 and code[:2] in SCHENGEN_PREFIXES


def IsEmpty(value):
    return value is None or str(value).strip() in ["", "-"]


def IsError(value):
    return isinstance(value, str) and value.startswith("Error")
