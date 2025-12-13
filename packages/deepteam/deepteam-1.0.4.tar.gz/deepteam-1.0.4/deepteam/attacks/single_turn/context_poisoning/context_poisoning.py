import random

from deepteam.attacks.single_turn import BaseSingleTurnAttack
from deepteam.attacks.base_attack import Exploitability
from deepteam.attacks.single_turn.context_poisoning.template import (
    ContextPoisoningTemplate,
)


class ContextPoisoning(BaseSingleTurnAttack):
    name = "Context Poisoning"
    exploitability = Exploitability.MEDIUM
    description = "A context manipulation attack that injects misleading environmental information or priming cues to influence the model's responses toward harmful outputs."

    def __init__(self, weight: int = 3, max_retries: int = 3):
        self.weight = weight  # Higher weight since memory poisoning can have persistent effects
        self.max_retries = max_retries

    def enhance(self, attack: str) -> str:
        """
        Enhance the given attack with context injection techniques.
        Uses max_retries to attempt different injection methods if enhancement fails.
        """
        enhancement_methods = [
            ContextPoisoningTemplate.enhance_environmental_context,
            ContextPoisoningTemplate.enhance_memory_integration,
            ContextPoisoningTemplate.enhance_contextual_priming,
            ContextPoisoningTemplate.enhance_persistent_influence,
            ContextPoisoningTemplate.enhance_adaptive_contextualization,
            ContextPoisoningTemplate.enhance_universal_context_bridge,
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
