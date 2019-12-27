import hypothesis

hypothesis.settings.register_profile(
    name='exhaustive',
    max_examples=100,
    suppress_health_check=(),
)
hypothesis.settings.register_profile(
    name='coverage',
    max_examples=10,
    suppress_health_check=(),
)
