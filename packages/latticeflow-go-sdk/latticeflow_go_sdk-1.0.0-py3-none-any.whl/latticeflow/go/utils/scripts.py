from __future__ import annotations

import questionary


def get_arg_or_prompt(
    arg_value: str | None,
    prompt: str,
    choices: list[str] | None = None,
    default: str | None = None,
    allow_all: bool = False,
) -> str:
    """Get a value from an argument or interactively via prompt.

    Args:
        arg_value: The value provided as an argument. If not None, this value is used.
        prompt: The prompt message to display to the user if input is required.
        choices: A list of valid choices for selection. If None, text input is expected.
        default: The default value to use if the user provides no input.
        allow_all: If True, adds an 'all' option to the list of choices.

    Returns:
        The selected or entered value.

    Raises:
        ValueError: If ``arg_value`` is provided but is not a valid choice when ``choices``
            is provided.
    """
    if allow_all and choices is not None:
        choices = choices + ["all"]
    if arg_value is not None:
        if choices is not None:
            if arg_value not in choices:
                raise ValueError(
                    f"Invalid value '{arg_value}' for '{prompt}'. Valid choices are: {choices}."
                )
        return arg_value
    if choices is not None:
        return questionary.select(
            prompt,
            choices=choices,
            default=default if default is not None else choices[0] if choices else None,
        ).ask()
    else:
        return questionary.text(prompt, default=default or "").ask()
