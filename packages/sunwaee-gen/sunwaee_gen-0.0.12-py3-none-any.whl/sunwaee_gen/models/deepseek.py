# standard
# third party
# custom
from sunwaee_gen.model import Model

DEEPSEEK_REASONER = Model(
    name="deepseek-reasoner",
    display_name="DeepSeek Reasoner",
    origin="deepseek",
)

DEEPSEEK_CHAT = Model(
    name="deepseek-chat",
    display_name="DeepSeek Chat",
    origin="deepseek",
)

DEEPSEEK_MODELS = [
    DEEPSEEK_REASONER,
    DEEPSEEK_CHAT,
]
