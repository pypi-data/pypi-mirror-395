import csv
import json
import re
from collections import defaultdict


def convert_translation_txt_to_json():
    LANG_CODE_RE = re.compile(r"^[a-z]{2,3}$")
    result = defaultdict(dict)

    with open("data.tsv", encoding="utf-8") as f:
        reader = csv.reader(f, delimiter="\t")
        for row in reader:
            if not row:
                continue
            row = row[:4]
            if len(row) < 4:
                continue
            _, place_id, lang, translation = row
            lang = lang.strip()
            translation = translation.strip()
            if not translation:
                continue
            if not LANG_CODE_RE.match(lang):
                continue
            result[place_id][lang] = translation

    result = dict(result)
    with open("translations_clean2.json", "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)
