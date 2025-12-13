# ckb_textify/emojis.py
import re

# Top used emojis mapped to spoken Kurdish
EMOJI_MAP = {
    # Faces
    "😂": "پێکەنینی زۆر",
    "😭": "گریانی زۆر",
    "🥺": "تکاکردن",
    "🤣": "پێکەنینی بەقەڵب",
    "❤️": "دڵی سوور",
    "✨": "بریقەدار",
    "😍": "خۆشەویستی",
    "🙏": "سوپاس",
    "😊": "زەردەخەنە",
    "🥰": "خۆشەویستی",
    "👍": "دەستخۆش",
    "😔": "خەمبار",
    "😁": "پێکەنین",
    "💕": "دڵ",
    "💙": "دڵی شین",
    "😢": "گریان",
    "🤔": "بیرکردنەوە",
    "🔥": "ئاگر",
    "💔": "دڵی شکاو",
    "🌹": "گوڵ",
    "🎉": "ئاھەنگ",
    "😎": "شاز",
    "👌": "تەواوە",
    "💜": "دڵی مۆر",
    "💛": "دڵی زەرد",
    "💚": "دڵی سەوز",
    "🖤": "دڵی ڕەش",
    "🤍": "دڵی سپی",
    "🧡": "دڵی پرتەقاڵی",
    "🤎": "دڵی قاوەیی",
    "👋": "سڵاو",
    "👀": "سەیرکردن",
    "🙂": "زەردەخەنە",
    "🤗": "لەباوەشگرتن",
    "💪": "بەھێز",
    "🔴": "خاڵی سوور",
    "✅": "ڕاستە",
    "✔️": "ڕاستە",
    "❌": "ھەڵەیە",
    "☀️": "خۆر",
    "🌙": "مانگ",
    "⭐": "ئەستێرە",
    "👑": "تاج",
    "🦁": "شێر",
    "🆔": "ئای دی",
    "🆕": "نوێ",
    "🆓": "بەلاش",
    "ℹ️": "زانیاری",
    "🆗": "ئۆکەی",
    "🔺": "سێگۆشەی سوور ڕوو لەسەرەوە",
}

# Regex to match specific emojis in the map
# Sort by length to handle multi-char emojis if any
ordered_keys = sorted(EMOJI_MAP.keys(), key=len, reverse=True)
KNOWN_EMOJI_RE = re.compile(r"(" + r"|".join(map(re.escape, ordered_keys)) + r")")

# Regex to catch ALL other emojis (Unicode ranges) to remove them
ALL_EMOJI_RE = re.compile(
    u'([\U00002600-\U000027BF])|'  # Misc symbols
    u'([\U0001f300-\U0001f64F])|'  # Emoticons
    u'([\U0001f680-\U0001f6FF])'  # Transport & Map
)


def normalize_emojis(text: str, mode: str = "remove") -> str:
    """
    Handles emojis in text.

    Args:
        mode (str):
            - "remove" (Default): Delete ALL emojis.
            - "convert": Convert known emojis to "ئیمۆجی [Description]", delete unknown.
            - "ignore": Do nothing.
    """
    if mode == "ignore":
        return text

    if mode == "convert":
        # 1. Replace known emojis with text prefixed by "ئیمۆجیەکی"
        def _replace_known(match):
            description = EMOJI_MAP.get(match.group(0), "")
            # Add "ئیمۆجی" prefix
            return f" ئیمۆجیەکی {description} "

        text = KNOWN_EMOJI_RE.sub(_replace_known, text)

        # 2. Remove any remaining unknown emojis
        text = ALL_EMOJI_RE.sub("", text)

    elif mode == "remove":
        # Remove known AND unknown (Cleanest for TTS)
        text = KNOWN_EMOJI_RE.sub("", text)
        text = ALL_EMOJI_RE.sub("", text)

    return text