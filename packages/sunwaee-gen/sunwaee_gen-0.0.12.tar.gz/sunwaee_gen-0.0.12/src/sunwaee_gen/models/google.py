# standard
# third party
# custom
from sunwaee_gen.model import Model

GEMINI_2_5_PRO = Model(
    name="gemini-2.5-pro",
    display_name="Gemini 2.5 Pro",
    origin="google",
)

GEMINI_2_5_FLASH = Model(
    name="gemini-2.5-flash",
    display_name="Gemini 2.5 Flash",
    origin="google",
)

GEMINI_2_5_FLASH_LITE = Model(
    name="gemini-2.5-flash-lite",
    display_name="Gemini 2.5 Flash Lite",
    origin="google",
)

GOOGLE_MODELS = [
    GEMINI_2_5_PRO,
    GEMINI_2_5_FLASH,
    GEMINI_2_5_FLASH_LITE,
]
