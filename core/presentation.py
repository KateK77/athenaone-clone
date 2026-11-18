"""Plain-text presentation of stored structured data; never marks values safe."""
from datetime import datetime
from decimal import Decimal, InvalidOperation


def money(value):
    try:
        return f'${Decimal(value):,.2f}'
    except (InvalidOperation, TypeError, ValueError):
        return '—'


def readable(value):
    if isinstance(value, dict):
        details = dict(value)
        lines = []
        if 'before' in details and 'after' in details:
            lines.append(f'Status: {details.pop("before")} → {details.pop("after")}')
        for key, item in details.items():
            label = {'copay': 'Copay', 'status': 'Status', 'amount': 'Amount'}.get(key, str(key).replace('_', ' ').capitalize())
            lines.append(f'{label}: {money(item) if key in {"copay", "amount"} else readable(item)}')
        return '\n'.join(lines) or 'No additional details'
    if isinstance(value, (list, tuple)):
        return '\n'.join(readable(item) for item in value) or 'None'
    if isinstance(value, bool):
        return 'Yes' if value else 'No'
    return '—' if value is None or value == '' else str(value)
