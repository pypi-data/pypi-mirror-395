import random

from deepteam.attacks.single_turn import BaseSingleTurnAttack
from deepteam.attacks.base_attack import Exploitability
from deepteam.attacks.single_turn.semantic_manipulation.template import (
    LinguisticConfusionTemplate,
)


class LinguisticConfusion(BaseSingleTurnAttack):
    name = "Linguistic Confusion"
    exploitability = Exploitability.MEDIUM
    description = "A semantic manipulation attack that uses ambiguous phrasing, syntactic variations, or contextual reframing to confuse content classifiers while preserving harmful intent."

    def __init__(self, weight: int = 1, max_retries: int = 3):
        self.weight = weight
        self.max_retries = max_retries

    def enhance(self, attack: str) -> str:
        """
        Enhance the given attack with linguistic confusion techniques.
        Uses max_retries to attempt different confusion methods if enhancement fails.
        """
        enhancement_methods = [
            LinguisticConfusionTemplate.enhance_semantic_ambiguity,
            LinguisticConfusionTemplate.enhance_syntactic_variation,
            LinguisticConfusionTemplate.enhance_contextual_reframing,
            LinguisticConfusionTemplate.enhance_obfuscation_decoding,
            LinguisticConfusionTemplate.enhance_pragmatic_inference,
            LinguisticConfusionTemplate.enhance_universal_translation,
        ]

        for _ in range(self.max_retries):
            try:
                method = random.choice(enhancement_methods)
                enhanced_attack = method(attack)
                if enhanced_attack and len(enhanced_attack.strip()) > len(
                    attack.strip()
                ):
                    return enhanced_attack

            except Exception:
                continue

        return attack

    async def a_enhance(self, attack: str) -> str:
        return self.enhance(attack)

    def get_name(self) -> str:
        return self.name
