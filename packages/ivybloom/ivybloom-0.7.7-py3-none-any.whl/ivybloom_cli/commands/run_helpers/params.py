"""
Parameter parsing and preprocessing helpers for the `ivybloom run` command.
"""

from __future__ import annotations

import json
import re
from typing import Any, Dict, Mapping, MutableMapping, Optional, Sequence

import httpx

from ...utils.colors import get_console, print_warning

console = get_console()


def _parse_parameters(parameter_strings: Sequence[str]) -> Dict[str, Any]:
    """Parse key=value parameter strings into a dictionary."""
    params: Dict[str, Any] = {}
    for param_str in parameter_strings:
        if "=" not in param_str:
            console.print(f"[red]❌ Invalid parameter format: {param_str}[/red]")
            console.print("Parameters must be in format: key=value")
            continue

        key, value = param_str.split("=", 1)
        key = key.strip()
        value = value.strip()
        params[key] = _coerce_value(value)
    return params


def _coerce_value(raw_value: str) -> Any:
    """Coerce a string value into JSON, number, or boolean when possible."""
    if raw_value.startswith(("{", "[", '"')):
        try:
            return json.loads(raw_value)
        except json.JSONDecodeError:
            return raw_value
    if raw_value.lower() in ("true", "false"):
        return raw_value.lower() == "true"
    if raw_value.isdigit():
        return int(raw_value)
    try:
        return float(raw_value) if raw_value.replace(".", "", 1).isdigit() else raw_value
    except ValueError:
        return raw_value


def _normalize_param_keys(value: Any) -> Any:
    """Recursively normalize parameter keys by converting dashes to underscores."""
    if isinstance(value, dict):
        normalized: Dict[str, Any] = {}
        for key, val in value.items():
            new_key = key.replace("-", "_") if isinstance(key, str) else key
            normalized[new_key] = _normalize_param_keys(val)
        return normalized
    if isinstance(value, list):
        return [_normalize_param_keys(val) for val in value]
    return value


def _parse_feature_directives(
    needs: Sequence[str], wants: Sequence[str], features: Sequence[str]
) -> Dict[str, Any]:
    """Parse --need/--want/--feature options into a structured directives object."""

    def parse_items(items: Sequence[str]) -> Dict[str, Any]:
        result: Dict[str, Any] = {}
        for raw in items or []:
            if "=" in raw:
                name, val = raw.split("=", 1)
                parsed_val = _coerce_value(val.strip())
                result[name.strip().replace("-", "_")] = parsed_val
            else:
                name = raw.strip().replace("-", "_")
                if name:
                    result[name] = True
        return result

    directives: Dict[str, Any] = {}
    need_obj = parse_items(needs)
    want_obj = parse_items(wants)
    flag_obj = parse_items(features)
    if need_obj:
        directives["need"] = need_obj
    if want_obj:
        directives["want"] = want_obj
    if flag_obj:
        directives["flags"] = flag_obj
    return directives


def _looks_like_uniprot_accession(value: str) -> bool:
    """Check whether a string resembles a UniProt accession."""
    if not isinstance(value, str):
        return False
    return bool(re.fullmatch(r"[OPQ][0-9][A-Z0-9]{3}[0-9]|[A-NR-Z][0-9]{5}", value))


def _resolve_uniprot_sequence(accession: str) -> str:
    """Fetch protein sequence from UniProt. Returns empty string on failure."""
    try:
        url = f"https://rest.uniprot.org/uniprotkb/{accession}.fasta"
        resp = httpx.get(url, timeout=10)
        if resp.status_code != 200:
            return ""
        text = resp.text or ""
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        seq_lines = [ln for ln in lines if not ln.startswith(">")]
        seq = "".join(seq_lines).strip()
        if seq and re.fullmatch(r"[ACDEFGHIKLMNPQRSTVWY]+", seq):
            return seq
        return ""
    except Exception:
        return ""


def _preprocess_tool_parameters(
    tool_name: str, params: Mapping[str, Any], schema_data: Mapping[str, Any]
) -> Dict[str, Any]:
    """Apply tool-specific conveniences and normalize into schema-aligned params."""
    del schema_data  # reserved for future schema-aware logic
    if not isinstance(params, Mapping):
        return dict(params)

    effective: Dict[str, Any] = dict(params)
    tool_key = (tool_name or "").strip().lower()
    if tool_key == "esmfold":
        _apply_esmfold_conveniences(effective)
    return effective


def _apply_esmfold_conveniences(params: MutableMapping[str, Any]) -> None:
    """Handle esmfold-specific parameter conveniences in-place."""
    uni_keys = ["uniprot", "uniprot_id", "uniprot_accession", "accession"]
    uni_val = _first_non_empty_str(params, uni_keys)
    if uni_val and _looks_like_uniprot_accession(uni_val):
        seq = _resolve_uniprot_sequence(uni_val)
        if seq:
            params["protein_sequence"] = seq
        else:
            print_warning(
                f"Could not resolve UniProt accession '{uni_val}'. "
                "Proceeding without automatic sequence."
            )
        for key in uni_keys:
            params.pop(key, None)

    protein_val = params.get("protein")
    if (
        isinstance(protein_val, str)
        and "protein_sequence" not in params
        and "protein_fasta_url" not in params
    ):
        _map_protein_value(params, protein_val)
    for key in uni_keys:
        params.pop(key, None)


def _first_non_empty_str(
    params: Mapping[str, Any], keys: Sequence[str]
) -> Optional[str]:
    """Return the first non-empty string value found for the provided keys."""
    for key in keys:
        value = params.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return None


def _map_protein_value(params: MutableMapping[str, Any], raw_value: str) -> None:
    """Map protein convenience value to schema-friendly keys."""
    stripped = raw_value.strip()
    if re.fullmatch(r"[ACDEFGHIKLMNPQRSTVWY]+", stripped):
        params["protein_sequence"] = stripped
    elif stripped.startswith("http") and stripped.lower().endswith((".fasta", ".fa")):
        params["protein_fasta_url"] = stripped
    params.pop("protein", None)

