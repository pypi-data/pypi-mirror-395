# standard
# third party
# custom
from sunwaee_gen.model import Model

GPT_5 = Model(
    name="gpt-5",
    display_name="GPT 5",
    origin="openai",
)

GPT_5_MINI = Model(
    name="gpt-5-mini",
    display_name="GPT 5 Mini",
    origin="openai",
)

GPT_5_NANO = Model(
    name="gpt-5-nano",
    display_name="GPT 5 Nano",
    origin="openai",
)

GPT_4_1 = Model(
    name="gpt-4-1",
    display_name="GPT 4.1",
    origin="openai",
)

GPT_4_1_MINI = Model(
    name="gpt-4-1-mini",
    display_name="GPT 4.1 Mini",
    origin="openai",
)

GPT_4_1_NANO = Model(
    name="gpt-4-1-nano",
    display_name="GPT 4.1 Nano",
    origin="openai",
)

OPENAI_MODELS = [
    GPT_5,
    GPT_5_MINI,
    GPT_5_NANO,
    GPT_4_1,
    GPT_4_1_MINI,
    GPT_4_1_NANO,
]
