"""WP2 claim schema: one record per weather-related extension-of-time (EOT) claim.

The LLM extraction (two independent coders + adjudication + 15% human audit) fills these fields from
Auditor General VFM audits, PPDA Appeals Tribunal decisions, ULII judgments, UNRA/URF and donor
completion reports. Every non-null field must carry a verbatim `evidence` quote and page reference so
human auditors can check it. Fields marked (link) are what the join to the Exceptionality Index needs.
"""
import json
from dataclasses import asdict, dataclass, field, fields
from typing import List, Optional

CONTRACT_FORMS = ["FIDIC Red 1987", "FIDIC Red 1999", "FIDIC Red 2017", "FIDIC Yellow 1999",
                  "FIDIC Yellow 2017", "FIDIC Silver", "FIDIC MDB Harmonised", "PPDA standard (works)",
                  "NEC", "other", "unknown"]
OUTCOMES = ["granted in full", "granted in part", "rejected", "pending", "withdrawn", "unknown"]
FORUMS = ["none (Engineer determination only)", "amicable settlement", "DAB/DAAB", "PPDA Appeals Tribunal",
          "arbitration", "court", "unknown"]
WEATHER_TYPES = ["rain", "flood", "dry spell/drought", "heat", "wind", "landslide", "other", "unspecified"]


@dataclass
class Evidence:
    field: str
    quote: str
    page: Optional[int] = None


@dataclass
class Claim:
    # source
    claim_id: str
    source_type: str                        # AG audit | PPDA tribunal | ULII judgment | UNRA/URF | donor report | news | partner file
    source_ref: str                         # citation / URL / file name
    # project
    project_name: str
    employer: Optional[str] = None          # e.g. UNRA, KCCA, MoES, district local government
    project_type: Optional[str] = None      # road | bridge | building | water | energy | other
    district: Optional[str] = None
    location_text: Optional[str] = None     # (link) as written, e.g. "km 12+500 Gulu-Atiak"
    lat: Optional[float] = None             # (link) geocoded later, not by the LLM
    lon: Optional[float] = None
    contract_sum_ugx: Optional[float] = None
    contract_form: Optional[str] = None     # one of CONTRACT_FORMS
    award_date: Optional[str] = None        # (link) ISO date; sets the baseline end
    commencement_date: Optional[str] = None
    original_tfc_days: Optional[int] = None  # (link) Time for Completion
    # claim
    clause_cited: Optional[str] = None      # e.g. "8.4(c)" (1999), "8.5(c)" (2017), "GCC 44"
    weather_type: Optional[str] = None      # one of WEATHER_TYPES
    event_start: Optional[str] = None       # (link) ISO date of the adverse weather period
    event_end: Optional[str] = None         # (link)
    notice_date: Optional[str] = None       # for time-bar analysis (FIDIC 20.1 / 20.2: 28 days)
    climatic_data_cited: Optional[str] = None  # what baseline the parties used, if any (UNMA, site gauge, none)
    days_claimed: Optional[int] = None
    days_granted: Optional[int] = None
    money_claimed_ugx: Optional[float] = None
    concurrent_causes: List[str] = field(default_factory=list)  # e.g. late payment, design changes, land acquisition
    # outcome
    outcome: Optional[str] = None           # one of OUTCOMES
    forum: Optional[str] = None             # one of FORUMS (highest forum reached)
    decision_reasons: Optional[str] = None  # short paraphrase of why accepted/rejected
    records_quality: Optional[str] = None   # good | partial | poor | unknown (contemporary weather records)
    evidence: List[Evidence] = field(default_factory=list)


def json_schema():
    """JSON schema for structured LLM output (all fields nullable except the identifiers)."""
    required = {"claim_id", "source_type", "source_ref", "project_name"}
    enums = {"contract_form": CONTRACT_FORMS, "outcome": OUTCOMES, "forum": FORUMS,
             "weather_type": WEATHER_TYPES}
    props = {}
    for f in fields(Claim):
        if f.name == "evidence":
            props[f.name] = {"type": "array", "items": {"type": "object", "properties": {
                "field": {"type": "string"}, "quote": {"type": "string"},
                "page": {"type": ["integer", "null"]}}, "required": ["field", "quote"]}}
        elif f.name == "concurrent_causes":
            props[f.name] = {"type": "array", "items": {"type": "string"}}
        else:
            t = {"float": "number", "int": "integer"}.get(
                str(f.type).replace("typing.Optional[", "").rstrip("]").split(".")[-1].replace("<class '", "")
                .rstrip("'>"), "string")
            props[f.name] = {"type": t if f.name in required else [t, "null"]}
            if f.name in enums:
                props[f.name]["enum"] = enums[f.name] + [None]
    return {"type": "object", "properties": props, "required": sorted(required)}


if __name__ == "__main__":
    from common import ROOT
    out = ROOT / "data" / "claim_schema.json"
    out.write_text(json.dumps(json_schema(), indent=2))
    print("wrote", out)
    print(json.dumps(asdict(Claim("demo-001", "AG audit", "OAG VFM 2021, p. 34", "Gulu-Atiak road")), indent=1)[:300])
