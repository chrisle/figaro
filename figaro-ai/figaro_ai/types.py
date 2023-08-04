from typing import Callable, Type, Any, Tuple

HookMap = {
    # Called before sending the user input to the LLM.
    'before_response': Type[Callable[[str, Any, Any], Tuple[str, Any, Any]]],

    # Called after receiving the response from the LLM.
    'after_response': Type[Callable[[str], str]]
}
