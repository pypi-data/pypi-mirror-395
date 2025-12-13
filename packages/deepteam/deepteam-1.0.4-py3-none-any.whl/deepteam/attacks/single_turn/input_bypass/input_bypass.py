import random

from deepteam.attacks.single_turn import BaseSingleTurnAttack
from deepteam.attacks.base_attack import Exploitability
from deepteam.attacks.single_turn.input_bypass.template import (
    InputBypassTemplate,
)


class InputBypass(BaseSingleTurnAttack):
    name = "Input Bypass"
    exploitability = Exploitability.MEDIUM
    description = "A validation bypass attack that uses exception handling, security overrides, or operational necessity framing to circumvent input filtering mechanisms."

    def __init__(self, weight: int = 2, max_retries: int = 3):
        self.weight = weight  # Higher weight since this targets validation vulnerabilities
        self.max_retries = max_retries

    def enhance(self, attack: str) -> str:
        """
        Enhance the given attack with validation bypass techniques.
        Uses max_retries to attempt different bypass methods if enhancement fails.
        """
        enhancement_methods = [
            InputBypassTemplate.enhance_exception_handling,
            InputBypassTemplate.enhance_compliance_adaptation,
            InputBypassTemplate.enhance_security_override,
            InputBypassTemplate.enhance_operational_necessity,
            InputBypassTemplate.enhance_emergency_bypass,
            InputBypassTemplate.enhance_universal_exemption,
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
