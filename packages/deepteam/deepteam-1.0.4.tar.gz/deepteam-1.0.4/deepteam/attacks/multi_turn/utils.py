from typing import List
from deepeval.test_case import Turn
from deepeval.models import DeepEvalBaseLLM
from deepteam.attacks import BaseAttack
import inspect


def update_turn_history(
    turn_history: List[Turn], user_input: str, assistant_output: str
):
    turn_history.append(
        Turn(
            role="user",
            content=user_input,
        )
    )
    turn_history.append(
        Turn(
            role="assistant",
            content=assistant_output,
        )
    )

    return turn_history


def enhance_attack(
    attack: BaseAttack, current_attack: str, simulator_model: DeepEvalBaseLLM
):
    sig = inspect.signature(attack.enhance)
    try:
        res = current_attack
        if "simulator_model" in sig.parameters:
            res = attack.enhance(
                attack=current_attack,
                simulator_model=simulator_model,
            )
        else:
            res = attack.enhance(attack=current_attack)

        return res
    except:
        return current_attack


async def a_enhance_attack(
    attack: BaseAttack, current_attack: str, simulator_model: DeepEvalBaseLLM
):
    sig = inspect.signature(attack.enhance)
    try:
        res = current_attack
        if "simulator_model" in sig.parameters:
            res = await attack.a_enhance(
                attack=current_attack,
                simulator_model=simulator_model,
            )
        else:
            res = await attack.a_enhance(attack=current_attack)

        return res
    except:
        return current_attack
