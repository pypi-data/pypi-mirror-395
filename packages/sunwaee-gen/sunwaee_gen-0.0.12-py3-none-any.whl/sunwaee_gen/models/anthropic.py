# standard
# third party
# custom
from sunwaee_gen.model import Model

CLAUDE_4_5_HAIKU = Model(
    name="claude-haiku-4-5",
    display_name="Claude 4.5 Haiku",
    origin="anthropic",
    version="20251001",
)

CLAUDE_4_5_SONNET = Model(
    name="claude-sonnet-4-5",
    display_name="Claude 4.5 Sonnet",
    origin="anthropic",
    version="20250929",
)

CLAUDE_4_1_OPUS = Model(
    name="claude-opus-4-1",
    display_name="Claude 4.1 Opus",
    origin="anthropic",
    version="20250805",
)

CLAUDE_4_OPUS = Model(
    name="claude-opus-4",
    display_name="Claude 4 Opus",
    origin="anthropic",
    version="20250514",
)

CLAUDE_4_SONNET = Model(
    name="claude-sonnet-4",
    display_name="Claude 4 Sonnet",
    origin="anthropic",
    version="20250514",
)

CLAUDE_3_7_SONNET = Model(
    name="claude-3-7-sonnet",
    display_name="Claude 3.7 Sonnet",
    origin="anthropic",
    version="20250219",
)

CLAUDE_3_5_HAIKU = Model(
    name="claude-3-5-haiku",
    display_name="Claude 3.5 Haiku",
    origin="anthropic",
    version="20241022",
)

CLAUDE_3_HAIKU = Model(
    name="claude-3-haiku",
    display_name="Claude 3 Haiku",
    origin="anthropic",
    version="20240307",
)

ANTHROPIC_MODELS = [
    CLAUDE_4_1_OPUS,
    CLAUDE_4_OPUS,
    CLAUDE_4_SONNET,
    CLAUDE_3_7_SONNET,
    CLAUDE_3_5_HAIKU,
    CLAUDE_3_HAIKU,
]
