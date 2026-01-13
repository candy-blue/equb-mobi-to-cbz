import re


_number_re = re.compile(r"(\\d+)")


def natural_sort_key(value: str):
  parts = _number_re.split(value)
  key = []
  for part in parts:
    if part.isdigit():
      key.append(int(part))
    else:
      key.append(part.lower())
  return key
