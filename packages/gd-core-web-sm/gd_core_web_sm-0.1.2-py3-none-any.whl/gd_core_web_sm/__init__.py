"""
gd_core_web_sm
--------------
Scottish Gaelic spaCy pipeline with:
- ML POS tagger
- POS-aware rule-based lemmatizer
"""

from spacy.lang.gd import Scottish  # make language class importable

# Import modules so that @Language.factory decorators run
# and register our custom components with spaCy:
from .models import tagger_module  # noqa: F401
from . import pos_aware_lemmatizer  # noqa: F401


def load(**overrides):
    """
    Entry-point used by `spacy.load("gd_core_web_sm")`.

    Instead of loading a serialized spaCy model from disk,
    we build the pipeline directly from `config.cfg` and our
    registered custom factories.
    """
    from pathlib import Path
    from spacy.util import load_config, load_model_from_config

    # Directory that contains config.cfg, lookups/, models/, etc.
    model_dir = Path(__file__).parent

    # Load spaCy config
    config = load_config(model_dir / "config.cfg")

    # Build nlp object from config (components come from our factories)
    nlp = load_model_from_config(config, auto_fill=True, validate=True)

    # Initialize components (so your PyTorch tagger, etc. are ready)
    # We don't need training data here, so we pass an empty lambda.
    nlp.initialize(lambda: [])

    return nlp


__all__ = ["Scottish", "load"]
