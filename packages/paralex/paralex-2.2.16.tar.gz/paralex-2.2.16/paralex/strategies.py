#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
from collections import OrderedDict
from hypothesis import strategies as st

Cs = {'ʣ': 'ds', 'ʦ': 'ts', 'ɹ': 'r', 'l': 'l', 'ɫ': 'l', 'ɮ': 'lz', 'z': 'z', 'ɬ': 'l', 's': 's', 'n': 'n', 'd': 'd',
      't': 't', 'ɺ': 'r', 'ɾ': 'r', 'r': 'r',
      'ȶ': 't', 'ȡ': 'd', 'ʥ': 'dz', 'ʨ': 'č', 'ȴ': 'll', 'ʑ': 'ź', 'ɕ': 'š', 'ȵ': 'ny', 'ɸ': 'f', 'ɓ': 'b', 'm': 'm',
      'b': 'b', 'p': 'p', 'ʙ': 'b', 'ð': 'dh', 'ɗ': 'ɗ', 'ʢ': 'ʢ', 'ʜ': 'x', 'ʡ': 'g', 'ɦ': 'h', 'h': 'h', 'ʔ': '\'',
      'ɥ': 'w', 'w': 'w', 'ʍ': 'hw', 'ʋ': 'w', 'v': 'v', 'f': 'f', 'ɱ': 'm', 'j': 'y', 'ʎ': 'ly', 'ʝ': 'gl',
      'ç': 'j', 'ɟ': 'gu', 'c': 'tj', 'ʕ': 'r', 'ʆ': 'shl', 'ʤ': 'dj', 'ʧ': 'tsh', 'ʒ': 'j',
      'ʃ': 'sh', 'ɻ': 'r', 'ɭ': 'l', 'ʐ': 'zh', 'ʂ': 'sh', 'ɳ': 'rn', 'ɖ': 'd', 'ʈ': 't', 'ɽ': 'r', 'ʁ': 'r', 'ɴ': 'n',
      'ɢ': 'g', 'q': 'q', 'ʀ': 'r', 'ɰ': 'g', 'ʟ': 'l', 'ɣ': 'x', 'x': 'x', 'ɠ': 'g', 'ŋ': 'ng', 'g': 'g', 'k': 'k'}

Vs = {'a': 'a', 'ã': 'an', 'e': 'é', 'i': 'i', 'ĩ': 'in', 'o': 'o', 'õ': 'on', 'u': 'oo',
      'ũ': 'un', 'y': 'u', 'æ': 'ae', 'ø': 'eu', 'œ': 'oe', 'ɐ': 'e', 'ɑ': 'a', 'ɒ': 'a', 'ɔ': 'o', 'ɘ': 'e', 'ə': '',
      'ɛ': 'e', 'ɜ': 'e', 'ɞ': 'e', 'ɤ': 'u', 'ɨ': 'i', 'ɪ': 'u', 'ɯ': 'oo', 'ɵ': 'ö', 'ɶ': 'ø',
      'ʉ': 'uu', 'ʊ': 'o', 'ʌ': 'o', 'ʏ': 'ü'}

abbr = st.text("bcdfghjklmnpqrstvwxyzaeiou", min_size=1, max_size=3)

POS = [
    "verb",
    "numeral",
    "conjunction",
    "noun",
    "adposition",
    "determiner",
    "article",
    "adverb",
    "pronoun",
    "fusedPreposition",
    "adjective",
    "symbol",
    "particle",
    "conditionalParticle",
    "demonstrativePronoun",
    "interjection",
    "semiColon",
    "diminutiveNoun",
    "possessivePronoun",
    "prepositionalAdverb",
    "compoundPreposition",
    "interrogativeRelativePronoun",
    "possessiveParticle",
    "plainVerb",
    "letter",
    "interrogativeDeterminer",
    "relativePronoun",
    "postposition",
    "fusedPronounAuxiliary",
    "interrogativeOrdinalNumeral",
    "indefiniteOrdinalNumeral",
    "strongPersonalPronoun",
    "possessiveRelativePronoun",
    "ordinalAdjective",
    "collectivePronoun",
    "commonNoun",
    "infinitiveParticle",
    "comparativeParticle",
    "partitiveArticle",
    "invertedComma",
    "lightVerb",
    "emphaticPronoun",
    "distinctiveParticle",
    "genericNumeral",
    "possessiveAdjective",
    "reflexivePossessivePronoun",
    "colon",
    "coordinationParticle",
    "presentParticipleAdjective",
    "fusedPrepositionPronoun",
    "cardinalNumeral",
    "indefiniteDeterminer",
    "numeralFraction",
    "questionMark",
    "generalAdverb",
    "superlativeParticle",
    "point",
    "indefiniteMultiplicativeNumeral",
    "comma",
    "closeParenthesis",
    "futureParticle",
    "personalPronoun",
    "reflexivePersonalPronoun",
    "adverbialPronoun",
    "reciprocalPronoun",
    "openParenthesis",
    "pastParticipleAdjective",
    "negativePronoun",
    "relativeDeterminer",
    "existentialPronoun",
    "pronominalAdverb",
    "relativeParticle",
    "exclamativeDeterminer",
    "multiplicativeNumeral",
    "reflexiveDeterminer",
    "modal",
    "unclassifiedParticle",
    "properNoun",
    "allusivePronoun",
    "interrogativeCardinalNumeral",
    "bullet",
    "subordinatingConjunction",
    "irreflexivePersonalPronoun",
    "possessiveDeterminer",
    "negativeParticle",
    "indefinitePronoun",
    "generalizationWord",
    "coordinatingConjunction",
    "deficientVerb",
    "adjective-i",
    "impersonalPronoun",
    "indefiniteCardinalNumeral",
    "adjective-na",
    "qualifierAdjective",
    "affirmativeParticle",
    "mainVerb",
    "fusedPrepositionDeterminer",
    "indefiniteArticle",
    "weakPersonalPronoun",
    "suspensionPoints",
    "interrogativeMultiplicativeNumeral",
    "affixedPersonalPronoun",
    "auxiliary",
    "circumposition",
    "copula",
    "demonstrativeDeterminer",
    "participleAdjective",
    "exclamativePoint",
    "interrogativePronoun",
    "presentativePronoun",
    "punctuation",
    "definiteArticle",
    "slash",
    "exclamativePronoun",
    "preposition",
    "conditionalPronoun",
    "relationNoun",
    "interrogativeParticle"
]


@st.composite
def tags(draw, suffix):
    """ Strategy to generate fake tag values (for overabundance_tag, etc) """
    return draw(st.text(min_size=3, max_size=6)) + suffix


lexeme_cols = OrderedDict({
    "inflection_class": st.none() | st.text(min_size=1, max_size=6),
    "source": st.none() | st.text(min_size=4, max_size=10),
    "frequency": st.none() | st.floats(),
    "label": None,
    "gloss": st.none() | st.text(min_size=5, max_size=10),
    "meaning": st.none() | st.text(min_size=5, max_size=50),
    "comment": st.none() | st.text(),
    "POS": st.sampled_from(POS),
    "language_ID": st.text(min_size=3, max_size=6),
    "analysis_tag": tags("_analysis_tag"),
    "defectiveness_tag": tags("_def_tag"),
    "overabundant_tag": tags("_ov_tag"),
    "epistemic_tag": tags("_epis_tag"),
    "variants_tag": tags("_variant_tag")
})


@st.composite
def sound_inventory(draw):
    """ Strategy to generate a sound inventory as a dict """
    C = draw(st.sets(st.sampled_from(list(Cs)), min_size=10, max_size=len(Cs) // 2))
    V = draw(st.sets(st.sampled_from(list(Vs)), min_size=3, max_size=10))
    return {"C": list(C), "V": list(V)}


@st.composite
def word(draw, sound_inventory, min_size=2, max_size=None):
    """ Strategy to generate a word """
    C = st.sampled_from(sound_inventory["C"])
    V = st.sampled_from(sound_inventory["V"])
    size = draw(st.integers(min_value=min_size, max_value=max_size or 10))
    r = draw(st.randoms())
    cats = (V, C) if int(r.random() < 0.5) else (C, V)
    phonemes = [draw(cats[0]) if i % 2 == 0 else draw(cats[1]) for i in range(size)]
    letters = [Cs.get(x, Vs.get(x)) for x in phonemes]
    return " ".join(phonemes), "".join(letters)


@st.composite
def word_with_sound_inventory(draw, **kwargs):
    """ Strategy to generate a word, without requiring an existing sound inventory. """
    return draw(word(draw(sound_inventory()), **kwargs))


@st.composite
def feature_structures(draw):
    """ Strategy to create synthetic feature structures

    Featurestructures look like:
        {   feat: [val1, val2],
        }

    We want all abbreviations, be them features or values, to be unique.

    Args:
        draw:

    Returns:

    """
    # Pick a vocabulary of abbreviations (a unique set of abbreviations)
    abbrs = draw(st.sets(abbr, min_size=6, max_size=300))

    # Select a set of abbreviations to serve as features
    #  and remove them from the vocabulary
    features = draw(st.sets(st.sampled_from(sorted(abbrs)),
                            min_size=1,
                            max_size=len(abbrs) // 2))
    abbrs = abbrs - features
    # Build the dictionnary of feature => { frozenset({value}), ... }
    # Sample some abbreviations to serve as values for each feature,
    # removing them from the vocabulary each time
    # until either features or vocabulary are exhausted
    fs = {}
    for f in features:
        values = draw(st.sets(st.sampled_from(sorted(abbrs)), min_size=2, max_size=20))
        abbrs = abbrs - values
        fs[f.upper()] = values
        if len(abbrs) < 2:
            break
    return fs


@st.composite
def cell(draw, fs, features):
    """ Strategy to create synthetic cells

    cells are frozensets of values,
     such that each value is taken from a distinct feature.

    Args:
        draw:
        fs: a feature_structure

    Returns:

    """
    # pick one value in each feature
    values = [draw(st.sampled_from(sorted(fs[f]))) for f in features]
    return ".".join(values)


@st.composite
def features_conjunctions(draw, fs):
    """ Strategy to create synthetic feature conjunctions"""
    fs = sorted(fs)
    # Pick how many features in each set
    sizes = draw(st.lists(st.integers(1, len(fs)), min_size=1))
    f_tuples = []
    # Iterate over feature set sizes
    for s in sorted(sizes, reverse=True):
        # Pick a set of features (eg: number & case)
        f = draw(st.sets(st.sampled_from(fs), min_size=s, max_size=s))
        # Check we don't already have a superset (eg: number & case & gender)
        is_included = any((f <= f2 for f2 in f_tuples))
        if not is_included:
            f_tuples.append(f)
    return f_tuples


@st.composite
def cell_feats(draw, min_size=2, max_size=50):
    """ Strategy to create synthetic cells and features"""
    features = draw(feature_structures())
    feature_conjs = draw(features_conjunctions(features))
    cells = set()
    for feats in feature_conjs:
        new_cells = draw(st.sets(cell(features, feats), min_size=min_size, max_size=max_size))
        cells |= new_cells
        max_size -= len(new_cells)
        if max_size <= min_size:
            break
    return list(cells), features


@st.composite
def orth_word(draw, inventory, **kwargs):
    """ Strategy to create synthetic orthographic word"""
    phon, orth = draw(word(inventory, **kwargs))
    return orth


@st.composite
def phon_word(draw, inventory, **kwargs):
    """ Strategy to create synthetic phonological word"""
    phon, orth = draw(word(inventory, **kwargs))
    return phon


@st.composite
def affix(draw, inventory):
    """ Strategy to create synthetic affix"""
    r = draw(st.randoms())
    form = draw(word(inventory, min_size=0, max_size=3))
    is_suffix = r.random() < 0.5
    return (is_suffix, form)


@st.composite
def lexemes_list(draw, sounds, lexemes_size=None):
    word_strategy = word(sounds, min_size=3, max_size=6)
    citation_forms = st.sets(word_strategy,
                             min_size=lexemes_size or 2,
                             max_size=lexemes_size or 10)
    return sorted(draw(citation_forms))


@st.composite
def lexemes_table(draw, lexemes, sounds):
    df = pd.DataFrame([(b, a) for (a, b) in lexemes],
                      columns=["lexeme_id", "label"])
    extra_cols = draw(st.lists(st.sampled_from(lexeme_cols), unique=True))
    for col in extra_cols:
        if col == "label":
            df[col] = df["lexeme_id"]
            df["lexeme_id"] = ["lexeme_n_"+str(i+1) for i in range(df.shape[0])]
        else:
            df[col] = [draw(lexeme_cols[col]) for _ in range(df.shape[0])]
    df = df.set_index("lexeme_id")
    return df

@st.composite
def paralex_dataset(draw, lexemes_size=None, cells_size=None):
    """ This represents a full paralex dataset

    Returns:
        a strategy to generate false long form paradigms
    """
    # Mandatory: forms table
    # Mandatory: metadata df
    # Optional: feature-values; cells; lexemes; sounds; graphemes

    m = draw(metadata())
    sounds = draw(sound_inventory())
    lexemes = draw(lexemes_list(sounds, lexemes_size=lexemes_size))
    cells, feats = draw(cell_feats(min_size=cells_size or 2, max_size=cells_size or 50))
    form_table = draw(forms_df(sounds, lexemes, cells))
    files = {"forms.csv": form_table}
    m["resources"].append({"path": "forms.csv",
                           "name": "forms"})
    extra_tables = draw(st.lists(st.sampled_from(["cells.csv",
                                                  "lexemes.csv",
                                                  "sounds.csv",
                                                  "graphemes.csv"
                                                  ]), unique=True))
    if "cells.csv" in extra_tables:
        files["cells.csv"] = pd.DataFrame(cells, columns=["cell_id"])
        files["cells.csv"].set_index("cell_id")
        m["resources"].append({"path": "cells.csv",
                               "name": "cells"})
    if "lexemes.csv" in extra_tables:
        files["lexemes.csv"] = draw(lexemes_table(lexemes, sounds))
        m["resources"].append({"path": "lexemes.csv",
                               "name": "lexemes"})
    if "sounds.csv" in extra_tables:
        files["sounds.csv"] = pd.DataFrame(sounds["C"] + sounds["V"],
                                           columns=["sound_id"])
        files["sounds.csv"].set_index("sound_id")
        m["resources"].append({"path": "sounds.csv",
                               "name": "sounds"})
    if "graphemes.csv" in extra_tables:
        files["graphemes.csv"] = pd.DataFrame([Cs[c] for c in sounds["C"]] +
                                              [Vs[v] for v in sounds["V"]],
                                              columns=["grapheme_id"])
        files["graphemes.csv"].set_index("grapheme_id")
        m["resources"].append({"path": "graphemes.csv",
                               "name": "graphemes"})
    if draw(st.booleans()):
        fvs = pd.DataFrame([
            [v, f, i] for f in feats for i, v in enumerate(feats[f])
        ], columns=["value_id", "feature", "canonical_order"])
        fvs["label"] = fvs["value_id"] + "ive"
        fvs = fvs.set_index("value_id")
        files["feature_values.csv"] = fvs
        m["resources"].append({"path": "feature_values.csv",
                               "name": "features-values"})

    files["paralex.package.json"] = m
    return files


@st.composite
def forms_df(draw, sounds, lexemes, cells):
    """ Strategy to generate a synthetic forms dataframe. """
    max_affixes = max(1, len(lexemes) // 2)
    # sample affixes
    affixes = {c: draw(st.sets(affix(sounds), min_size=1, max_size=max_affixes)) for c in cells}

    def concatenate_words(a, is_suffix, b):
        phon, orth = zip(a, b) if is_suffix else zip(b, a)
        return " ".join(phon), "".join(orth)

    rows = []

    i = 0
    for lex in lexemes:
        for c in cells:
            exp = draw(st.lists(st.sampled_from(list(affixes[c])), min_size=1, max_size=3, unique=True))
            for a in exp:
                i += 1
                rows.append([
                    "f" + str(i),
                    lex[1],
                    c,
                    *concatenate_words(lex, *a)
                ])
    df = pd.DataFrame(rows, columns=["form_id", "lexeme", "cell", "phon_form", "orth_form"])
    return df


@st.composite
def metadata(draw):
    """ Strategy to generate fake metadata for a dataset

    This includes a list of resources with paths & names,

    """
    meta = {"resources": [],
            "title": draw(st.text(min_size=5, max_size=20)),
            "description": draw(st.text(min_size=10, max_size=50)),
            "profile": "data-package",
            }
    if draw(st.booleans()):
        meta["contributors"] = [
            {
                "title": draw(st.text(min_size=5, max_size=10)) + " " + draw(st.text(min_size=5, max_size=10)),
            } for _ in range(draw(st.integers(min_value=1, max_value=6)))
        ]
    if draw(st.booleans()):
        meta["keywords"] = draw(st.lists(st.text(min_size=3, max_size=10)))
    return meta
