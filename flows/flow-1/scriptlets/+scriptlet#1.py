import io

from typing import Literal

_Splitors = (",", "，", ".", "。")
_HieroglyphicIgnoreSplitors = (",", "，")

def main(params: dict):
  sentences: list[dict] = params["sentences"]
  limit_chars: int = params["limit_chars"]
  language: Literal["zh", "en"] = params["language"]
  alphabetic: bool = language != "zh"
  to_sentences: list[dict] = []

  for sentence in sentences:
    for sub_sentence in split_sentences(sentence, limit_chars, alphabetic):
      to_sentences.append(sub_sentence)

  return { "sentences": to_sentences }

def split_sentences(sentence: dict, limit_chars: int, alphabetic: bool):
  fragments: list[tuple[int, list[dict]]] = []
  for fragment in split_into_fragments(sentence["segments"], alphabetic):
    chars: int = 0
    for segment in fragment:
      text = segment["text"]
      chars += len(text)
    fragments.append((chars, fragment))

  chars = sum(chars for chars, _ in fragments)
  if chars <= limit_chars:
    yield merge_fragments(fragments, alphabetic)
  else:
    for chars, fragment in fragments:
      yield merge_fragments([(chars, fragment)], alphabetic)

def split_into_fragments(segments: list[dict], alphabetic: bool):
  global _Splitors
  fragment: list[dict] = []

  for segment in segments:
    text: str = segment["text"]
    kind: str = segment["kind"]
    if kind == "punctuation" and text in _Splitors and len(fragment) > 0:
      yield fragment
      fragment = []
    else:
      fragment.append(segment)

  if len(fragment) > 0:
    yield fragment

def merge_fragments(fragments: list[tuple[int, list[dict]]], alphabetic: bool):
  buffer = io.StringIO()
  segments = list(iter_fragments(fragments))
  did_write: bool = False
  min_begin_at: float = float("inf")
  max_end_at: float = 0.0

  for i, segment in enumerate(segments):
    is_last = i >= len(segments) - 1
    text: str = segment["text"]
    kind: str = segment["kind"]

    if kind == "punctuation" and ignore_punctuation(text, is_last, alphabetic):
      continue

    begin_at: float = segment["begin_at"]
    duration: float = segment["duration"]
    min_begin_at = min(min_begin_at, begin_at)
    max_end_at =  max(max_end_at, begin_at + duration)

    if alphabetic and did_write and kind != "punctuation":
      buffer.write(" ")
    buffer.write(text)
    did_write = True

  text = buffer.getvalue()

  return {
    "kind": "sentence",
    "text": text,
    "begin_at": min_begin_at,
    "duration": max_end_at - min_begin_at,
    "length": len(text),
    "offset": 0,
    "segments": [],
  }

def ignore_punctuation(text: str, is_last: bool, alphabetic: bool):
  global _Splitors, _HieroglyphicIgnoreSplitors
  if text not in _Splitors:
    return False
  if is_last:
    return True
  if alphabetic:
    return False
  if text in _HieroglyphicIgnoreSplitors:
    return True
  return False

def iter_fragments(fragments: list[tuple[int, list[dict]]]):
  for _, fragment in fragments:
    for segment in fragment:
      yield segment