from __future__ import annotations

import json
import re
from datetime import datetime
from typing import Any, Optional, Tuple

import dateparser
import requests

from competition_intel.settings import APP_SETTINGS

DATE_PATTERN = re.compile(r"(20\d{2}[年\-/\. ]\d{1,2}[月\-/\. ]\d{1,2}日?)")
ORGANIZER_PATTERN = re.compile(r"(?:主办方|主办单位|主办)[:：]\s*([^\n]{2,80})")
PRIZE_PATTERN = re.compile(r"(?:奖金|奖项)[:：]\s*([^\n]{2,80})")


def _normalize_date(raw: Optional[str]) -> Optional[str]:
    if not raw:
        return None
    dt = dateparser.parse(raw, languages=["zh", "en"])
    if dt is None:
        return None
    return dt.strftime("%Y-%m-%d")


def _pick_dates(text: str) -> Tuple[Optional[str], Optional[str], Optional[str]]:
    all_dates = [_normalize_date(m.group(1)) for m in DATE_PATTERN.finditer(text)]
    normalized = [d for d in all_dates if d]
    if not normalized:
        return None, None, None
    unique_sorted = sorted(set(normalized))
    registration_start = unique_sorted[0] if len(unique_sorted) >= 1 else None
    registration_deadline = unique_sorted[1] if len(unique_sorted) >= 2 else unique_sorted[0]
    competition_date = unique_sorted[-1]
    return registration_start, registration_deadline, competition_date


def _detect_level(text: str) -> Optional[str]:
    if "国际" in text or "international" in text.lower():
        return "国际级"
    if "全国" in text or "国家" in text:
        return "国家级"
    if "校内" in text or "校级" in text:
        return "校级"
    return None


def _extract_json_from_text(raw: str) -> Optional[dict[str, Any]]:
    # Prefer the first JSON object in the model output.
    match = re.search(r"\{[\s\S]*\}", raw)
    if not match:
        return None
    try:
        value = json.loads(match.group(0))
    except json.JSONDecodeError:
        return None
    if not isinstance(value, dict):
        return None
    return value


def _extract_with_llm(
    text: str,
    announcement_title: str,
    source_url: str,
    competition_name: str,
) -> Optional[dict[str, Any]]:
    if not APP_SETTINGS.openai_api_key:
        return None

    prompt = {
        "task": "从竞赛公告正文提取结构化信息，缺失字段返回 null，返回 JSON 对象。",
        "schema": {
            "competition_name": "string|null",
            "organizer": "string|null",
            "announcement_title": "string|null",
            "registration_start": "YYYY-MM-DD|null",
            "registration_deadline": "YYYY-MM-DD|null",
            "competition_date": "YYYY-MM-DD|null",
            "prize": "string|null",
            "competition_level": "国家级|国际级|校级|null",
            "source_url": "string|null",
        },
        "input": {
            "competition_name": competition_name,
            "announcement_title": announcement_title,
            "source_url": source_url,
            "text": text[:12000],
        },
    }

    url = APP_SETTINGS.openai_base_url.rstrip("/") + "/chat/completions"
    headers = {
        "Authorization": f"Bearer {APP_SETTINGS.openai_api_key}",
        "Content-Type": "application/json",
    }
    body = {
        "model": APP_SETTINGS.openai_model,
        "messages": [
            {"role": "system", "content": "你是信息抽取器，只输出 JSON。"},
            {"role": "user", "content": json.dumps(prompt, ensure_ascii=False)},
        ],
        "temperature": 0,
    }

    try:
        resp = requests.post(url, headers=headers, json=body, timeout=40)
        resp.raise_for_status()
        data = resp.json()
        content = data["choices"][0]["message"]["content"]
        parsed = _extract_json_from_text(content)
        if not parsed:
            return None
        parsed["competition_name"] = parsed.get("competition_name") or competition_name
        parsed["announcement_title"] = parsed.get("announcement_title") or announcement_title
        parsed["source_url"] = parsed.get("source_url") or source_url
        parsed["extracted_at"] = datetime.utcnow().isoformat()
        return parsed
    except Exception:
        return None


def extract_information(
    text: str,
    announcement_title: str,
    source_url: str,
    competition_name: str,
) -> dict[str, Any]:
    llm_payload = _extract_with_llm(
        text=text,
        announcement_title=announcement_title,
        source_url=source_url,
        competition_name=competition_name,
    )
    if llm_payload is not None:
        return llm_payload

    organizer_match = ORGANIZER_PATTERN.search(text)
    prize_match = PRIZE_PATTERN.search(text)
    registration_start, registration_deadline, competition_date = _pick_dates(text)

    payload: dict[str, Any] = {
        "competition_name": competition_name,
        "organizer": organizer_match.group(1).strip() if organizer_match else None,
        "announcement_title": announcement_title,
        "registration_start": registration_start,
        "registration_deadline": registration_deadline,
        "competition_date": competition_date,
        "prize": prize_match.group(1).strip() if prize_match else None,
        "competition_level": _detect_level(text),
        "source_url": source_url,
        "extracted_at": datetime.utcnow().isoformat(),
    }
    return payload


def payload_to_json(payload: dict[str, Any]) -> str:
    return json.dumps(payload, ensure_ascii=False)
