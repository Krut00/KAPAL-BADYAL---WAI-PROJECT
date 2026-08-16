"""Integrity checks for CCC components parsed from Screener.in.

Values are never overridden: the app must display exactly what Screener
publishes. These helpers only flag inconsistencies for transparency.
"""

from typing import Dict, List


class DataValidator:
    """Reports data-quality issues without altering Screener's published figures."""

    # Screener rounds each ratio independently, so components can differ from
    # the published CCC by a couple of days without being wrong.
    ROUNDING_TOLERANCE_DAYS = 3

    @staticmethod
    def check(components: Dict[str, float]) -> List[str]:
        """Return human-readable warnings for a set of CCC components."""
        if not components:
            return ['No CCC components were returned by Screener.']

        warnings: List[str] = []
        inventory = components.get('inventory_days') or 0
        receivable = components.get('receivable_days') or 0
        payable = components.get('payable_days') or 0
        published_ccc = components.get('ccc')

        if published_ccc is None:
            warnings.append('Screener did not publish a Cash Conversion Cycle for this period.')
        else:
            derived = inventory + receivable - payable
            if abs(derived - published_ccc) > DataValidator.ROUNDING_TOLERANCE_DAYS:
                warnings.append(
                    f'Screener publishes CCC {published_ccc:g} while its components imply '
                    f'{derived:g}. Showing the published value.'
                )

        for label, value in (('Inventory days', inventory),
                             ('Debtor days', receivable),
                             ('Days payable', payable)):
            if value < 0:
                warnings.append(f'{label} is negative on Screener ({value:g}).')

        return warnings
