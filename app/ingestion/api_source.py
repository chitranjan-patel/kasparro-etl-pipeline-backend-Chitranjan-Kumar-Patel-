from collections.abc import Iterable
from typing import Any
from datetime import datetime

import requests
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db import models
from app.schemas.unified import UnifiedRecordCreate


def fetch_api_data(last_external_id: int | None = None) -> list[dict[str, Any]]:
    """Fetch cryptocurrency market data from CoinGecko API.
    
    CoinGecko provides free, comprehensive cryptocurrency market data including:
    - Pricing (USD, EUR, GBP)
    - Market cap
    - Trading volume
    - Price changes
    
    Supports top cryptocurrencies: Bitcoin, Ethereum, Cardano, Solana, Polkadot, etc.
    No API key required for free tier.
    """
    params = {
        "vs_currency": "usd",
        "order": "market_cap_desc",
        "per_page": 250,
        "page": 1,
        "sparkline": False,
        "locale": "en"
    }
    
    headers = {}
    if settings.api_key and settings.api_key != "":
        headers["X-API-Key"] = settings.api_key
    
    resp = requests.get(str(settings.api_source_url), params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    items: list[dict[str, Any]] = resp.json()

    if last_external_id is not None:
        pass # items = [item for item in items if int(item.get("id", 0) or 0) > last_external_id]

    return items


def store_raw_api(db: Session, records: Iterable[dict[str, Any]]) -> list[int]:
    ids: list[int] = []
    for rec in records:
        # Use CoinGecko's unique identifier as external_id
        external_id = hash(rec.get("id", "")) % (10 ** 8)
        raw = models.RawAPIRecord(external_id=int(external_id), payload=rec)
        db.add(raw)
        ids.append(int(external_id))
    return ids


def transform_api_to_unified(records: Iterable[dict[str, Any]]) -> list[UnifiedRecordCreate]:
    """Transform CoinGecko cryptocurrency data to unified schema.
    
    Extracts:
    - Cryptocurrency name (Bitcoin, Ethereum, etc.)
    - Current USD price as value
    - Market last updated timestamp
    """
    unified: list[UnifiedRecordCreate] = []
    for rec in records:
        try:
            # Extract cryptocurrency identifier
            ext_id = str(rec.get("id", "unknown")).lower()
            # Get cryptocurrency symbol and name
            symbol = (rec.get("symbol") or "").upper()
            name = rec.get("name") or "Unknown"
            full_name = f"{name} ({symbol})" if symbol else name
            
            # Current price in USD
            price = rec.get("current_price") or 0
            
            # Use last_updated timestamp or current time
            last_updated = rec.get("last_updated")
            if last_updated:
                try:
                    timestamp = datetime.fromisoformat(last_updated.replace('Z', '+00:00'))
                except (ValueError, TypeError):
                    timestamp = datetime.utcnow()
            else:
                timestamp = datetime.utcnow()
            
            unified.append(
                UnifiedRecordCreate(
                    source="coingecko_api",
                    external_id=ext_id,
                    name=full_name,
                    value=int(price) if price else 0,
                    timestamp=timestamp,
                )
            )
        except Exception as e:
            # Log and skip malformed records
            print(f"Warning: Failed to transform record {rec}: {e}")
            continue
    
    return unified
