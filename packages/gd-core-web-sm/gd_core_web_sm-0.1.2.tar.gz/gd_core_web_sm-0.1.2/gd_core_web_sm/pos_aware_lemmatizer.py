# -*- coding: utf-8 -*-
"""
POS-aware Lemmatizer for Scottish Gaelic
----------------------------------------
Author: Oskar Diyali
Date: June 2025

This module defines a custom, rule-based lemmatizer that integrates with spaCy.
It handles preprocessing (lenition, dh’ removal, etc.), irregular dictionary lookups,
and POS-informed suffix stripping rules for nouns, verbs, and adjectives.
"""

import json
import os
import re
from pathlib import Path
from spacy.language import Language
from spacy.tokens import Doc



# PREPROCESSING FUNCTION
def preprocess_gaelic_word(word: str) -> str:
    """Apply normalization and remove prosthetic or emphatic forms."""
    acute_to_grave = {
        'á': 'à', 'é': 'è', 'í': 'ì', 'ó': 'ò', 'ú': 'ù',
        'Á': 'À', 'É': 'È', 'Í': 'Ì', 'Ó': 'Ò', 'Ú': 'Ù',
        'ʼ': '`'
    }
    word = ''.join(acute_to_grave.get(c, c) for c in word.lower())

    for suf in ['-sa', '-se', '-san', '-ne']:
        if word.endswith(suf) and len(word) > len(suf):
            word = word[:-len(suf)]
            break

    if word.startswith(("t-", "h-", "n-")):
        word = word[2:]

    if re.match(r"^dh[’']", word):
        word = word[3:]
    elif re.match(r"^d[’']", word):
        word = word[2:]

    if len(word) > 2 and word[1] == 'h':
        word = word[0] + word[2:]

    return word


# HELPER RULE FUNCTIONS
def remove_suffix(word: str, n: int) -> str:
    return word[:-n] if len(word) > n else word


def change_in_to_an(word: str) -> str:
    return word[:-2] + "an" if len(word) > 2 else word



# MAIN FACTORY COMPONENT
@Language.factory("gaelic_lemmatizer_pos_aware")
def make_gaelic_lemmatizer(nlp: Language, name: str,
                           irregular_path: str = "lookups/irregular_dict.json"):

    """Factory that loads irregular dictionary and returns the Gaelic lemmatizer."""

    file_path = os.path.join(os.path.dirname(__file__), irregular_path)
    irregulars = {}
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            irregulars = json.load(f)
    except FileNotFoundError:
        print(f"️  Warning: Irregular dictionary not found at {file_path}.")
    except json.JSONDecodeError:
        print(f"️  Warning: Could not decode irregular dictionary at {file_path}.")

# LEMMATIZATION LOGIC
    def gaelic_lemmatizer_pos_aware(doc: Doc) -> Doc:
        for token in doc:
            raw_text = token.text.lower()
            lemma_str = raw_text
            upos = token.pos_

            # 1) Irregular lookup
            if raw_text in irregulars:
                lemma_str = irregulars[raw_text]
            else:
                preprocessed = preprocess_gaelic_word(raw_text)

                if preprocessed in irregulars:
                    lemma_str = irregulars[preprocessed]
                else:
                    lemma_applied = False

                    # 2) POS-specific rules
                    if upos == "NOUN":
                        for suf, n in [("aichean", 7), ("annan", 5),
                                       ("ean", 3), ("an", 2)]:
                            if preprocessed.endswith(suf):
                                lemma_str = remove_suffix(preprocessed, n)
                                lemma_applied = True
                                break
                        if preprocessed.endswith("in") and not lemma_applied:
                            lemma_str = change_in_to_an(preprocessed)
                            lemma_applied = True

                    elif upos == "VERB":
                        for suf, repl in [
                            ("eachadh", "ich"), ("achadh", "aich")
                        ]:
                            if preprocessed.endswith(suf):
                                lemma_str = remove_suffix(preprocessed, len(suf)) + repl
                                lemma_applied = True
                                break
                        if not lemma_applied:
                            for suf in ["eamaid", "teadh", "tadh", "eadh", "aidh",
                                        "aibh", "ainn", "eas", "ear", "tar", "idh",
                                        "ibh", "inn", "eam", "adh", "as", "ar",
                                        "am", "te", "ta"]:
                                if preprocessed.endswith(suf):
                                    lemma_str = remove_suffix(preprocessed, len(suf))
                                    lemma_applied = True
                                    break

                    elif upos == "ADJ":
                        if preprocessed.endswith("ach"):
                            lemma_str = raw_text
                        elif preprocessed.endswith(("ta", "te")):
                            lemma_str = remove_suffix(preprocessed, 2)

                    # --- 3) Fallbacks ---
                    if not lemma_applied and preprocessed != raw_text:
                        lemma_str = preprocessed
                    if len(lemma_str) <= 1 and lemma_str != irregulars.get(raw_text):
                        lemma_str = raw_text

            # Assign lemma safely (auto-registers in vocab)
            token.lemma_ = lemma_str
        return doc

    return gaelic_lemmatizer_pos_aware


# DEMO / OUTPUT SECTION
if __name__ == "__main__":
    """
    When executed directly:
      • Loads small test data if present
      • Prints token → lemma | POS
      • Writes output file for inspection
    """

    import spacy
    from pathlib import Path

    # Example config (you can adapt)
    IRREG_PATH = Path("lookups/irregular_dict.json")
    POS_DATA_JSON = Path("../top_500_gaelic_pos.json")
    FREQ_LIST_TXT = Path("../Top500Words.txt")
    OUTPUT_TXT = Path("../lemmatized_output_pos_aware_example.txt")

    nlp = spacy.blank("gd")
    nlp.add_pipe("gaelic_lemmatizer_pos_aware",
                 config={"irregular_path": str(IRREG_PATH)})

    # --- Load POS lookup ---
    pos_lookup = {}
    if POS_DATA_JSON.exists():
        with POS_DATA_JSON.open("r", encoding="utf-8") as f:
            for entry in json.load(f):
                w = entry.get("word", "").lower()
                pos_lookup[w] = entry.get("upos", "")
    else:
        print("️  POS JSON not found; defaulting all to NOUN.")
        pos_lookup = {}

    # --- Load frequency list ---
    words = []
    if FREQ_LIST_TXT.exists():
        with FREQ_LIST_TXT.open("r", encoding="utf-8") as f:
            for line in f:
                w = line.strip().lower()
                if w:
                    words.append(w)
    else:
        print("️  Frequency list missing; using sample words.")
        words = ["Dh’òl", "mi", "uisge", "anns", "na", "h-eileanan"]

    # --- Run and write output ---
    changed = 0
    unchanged = 0
    with OUTPUT_TXT.open("w", encoding="utf-8") as out:
        print("Token  ->  Lemma   | POS")
        print("-" * 40)
        for w in words:
            doc = nlp.make_doc(w)
            tok = doc[0]
            upos = pos_lookup.get(w, "NOUN")
            tok.pos = nlp.vocab.strings[upos]
            processed = nlp(doc)
            lemma = processed[0].lemma_
            print(f"{w:<10} -> {lemma:<10} | {upos}")
            out.write(f"{w}\t{lemma}\n")
            if lemma == w.lower():
                unchanged += 1
            else:
                changed += 1

    print("\nSummary:")
    print(f"Changed:   {changed}")
    print(f"Unchanged: {unchanged}")
    print(f"Output saved to {OUTPUT_TXT.resolve()}")

