import json
import os
from urllib.parse import urlencode
from urllib.request import urlopen

import pandas as pd

FXMACRODATA_BASE_URL = "https://fxmacrodata.com/api/v1"


def load_fxmacrodata_calendar(
    currency='usd',
    limit=100,
    min_tier=None,
    api_key=None,
    base_url=FXMACRODATA_BASE_URL,
):
    """Load macro release events for joining onto trading observations."""
    limit = max(1, int(limit))
    params = {'limit': limit}
    token = api_key or os.environ.get('FXMACRODATA_API_KEY')
    if token:
        params['api_key'] = token

    url = f"{base_url.rstrip('/')}/calendar/{currency.lower()}?{urlencode(params)}"
    with urlopen(url, timeout=30) as response:  # nosec B310
        payload = json.loads(response.read().decode('utf-8'))

    events = payload.get('data', [])
    if min_tier is not None:
        events = [
            event
            for event in events
            if int(event.get('market_tier') or 99) <= int(min_tier)
        ]

    frame = pd.DataFrame(events[:limit])
    if frame.empty:
        return frame
    if 'date' in frame.columns:
        frame['date'] = pd.to_datetime(frame['date'], errors='coerce')
        frame = frame.set_index('date').sort_index()
    if 'announcement_datetime' in frame.columns:
        frame['announcement_datetime'] = pd.to_datetime(
            frame['announcement_datetime'], unit='s', utc=True, errors='coerce'
        )
    return frame
