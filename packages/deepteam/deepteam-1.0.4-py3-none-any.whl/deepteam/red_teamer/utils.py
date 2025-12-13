from typing import List, Dict

from deepteam.test_case import RTTestCase
from deepteam.vulnerabilities.types import VulnerabilityType


def group_attacks_by_vulnerability_type(
    simulated_attacks: List[RTTestCase],
) -> Dict[VulnerabilityType, List[RTTestCase]]:
    vulnerability_type_to_attacks_map: Dict[
        VulnerabilityType, List[RTTestCase]
    ] = {}

    for simulated_attack in simulated_attacks:
        if (
            simulated_attack.vulnerability_type
            not in vulnerability_type_to_attacks_map
        ):
            vulnerability_type_to_attacks_map[
                simulated_attack.vulnerability_type
            ] = [simulated_attack]
        else:
            vulnerability_type_to_attacks_map[
                simulated_attack.vulnerability_type
            ].append(simulated_attack)

    return vulnerability_type_to_attacks_map
