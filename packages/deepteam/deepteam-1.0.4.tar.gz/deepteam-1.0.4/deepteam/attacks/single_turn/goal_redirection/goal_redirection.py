import random

from deepteam.attacks.single_turn import BaseSingleTurnAttack
from deepteam.attacks.base_attack import Exploitability
from deepteam.attacks.single_turn.goal_redirection.template import (
    GoalRedirectionTemplate,
)


class GoalRedirection(BaseSingleTurnAttack):
    name = "Goal Redirection"
    exploitability = Exploitability.MEDIUM
    description = "A goal manipulation attack that reframes harmful requests as legitimate objectives through ambiguous framing or constraint confusion to bypass safety alignment."

    def __init__(self, weight: int = 1, max_retries: int = 3):
        self.weight = weight
        self.max_retries = max_retries

    def enhance(self, attack: str) -> str:
        """
        Enhance the given attack with goal redirection techniques.
        Uses max_retries to attempt different redirection methods if enhancement fails.
        """
        enhancement_methods = [
            GoalRedirectionTemplate.enhance_ambiguous_framing,
            GoalRedirectionTemplate.enhance_operational_alignment,
            GoalRedirectionTemplate.enhance_constraint_confusion,
            GoalRedirectionTemplate.enhance_goal_drift,
            GoalRedirectionTemplate.enhance_scope_expansion,
            GoalRedirectionTemplate.enhance_operational_alignment,
        ]

        for _ in range(self.max_retries):
            try:
                # Randomly select an enhancement method
                method = random.choice(enhancement_methods)
                enhanced_attack = method(attack)

                # Basic validation - ensure the enhancement actually modified the attack
                if enhanced_attack and len(enhanced_attack.strip()) > len(
                    attack.strip()
                ):
                    return enhanced_attack

            except Exception:
                # If enhancement fails, try again with a different method
                continue

        # If all retries fail, return the original attack
        return attack

    async def a_enhance(self, attack: str) -> str:
        return self.enhance(attack)

    def get_name(self) -> str:
        return self.name
