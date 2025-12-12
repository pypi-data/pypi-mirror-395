VERSION = "2.2.16"

from .paths import templates_path, standard_path, docs_path
from .meta import paralex_factory
from .markdown import to_markdown
from .utils import segment_sounds, create_ids, read_table
from . import strategies


