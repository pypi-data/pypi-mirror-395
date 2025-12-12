import enum


def parametrize_enum_flag_property_test(
    e: type[enum.Enum],
    truthy: list[enum.Enum] | tuple[enum.Enum] | set[enum.Enum],
) -> list[tuple[enum.Enum, bool]]:
    return [(value, value in truthy) for value in e]
