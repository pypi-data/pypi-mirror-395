# standard
# third party
# custom
from sunwaee_gen.model import Model

GROK_CODE_FAST_1 = Model(
    name="grok-code-fast-1",
    display_name="Grok Code Fast 1",
    origin="xai",
)

GROK_4 = Model(
    name="grok-4",
    display_name="Grok 4",
    origin="xai",
)

GROK_3 = Model(
    name="grok-3",
    display_name="Grok 3",
    origin="xai",
)

GROK_3_MINI = Model(
    name="grok-3-mini",
    display_name="Grok 3 Mini",
    origin="xai",
)

XAI_MODELS = [
    GROK_CODE_FAST_1,
    GROK_4,
    GROK_3,
    GROK_3_MINI,
]
