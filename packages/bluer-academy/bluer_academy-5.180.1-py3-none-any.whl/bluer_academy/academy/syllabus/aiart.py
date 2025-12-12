from bluer_academy.academy.classes.topic import Topic

topic = Topic(
    "aiart",
    [
        "[image generation with OpenAI](https://github.com/kamangir/openai-commands)",
        "[image generation with Stable Fusion](https://github.com/kamangir/blue-stability)",
    ],
    duration=3,
    requires="python,bash,cloud",
    items={
        "https://github.com/kamangir/openai-commands/raw/main/assets/DALL-E.png?raw=true": "https://github.com/kamangir/openai-commands",
        "https://github.com/kamangir/blue-stability/raw/main/assets/carrot.png": "https://github.com/kamangir/blue-stability",
    },
    capstone=True,
)
