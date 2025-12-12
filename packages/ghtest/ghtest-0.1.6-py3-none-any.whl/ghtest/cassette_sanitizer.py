#!/usr/bin/env python
# coding: utf-8

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any, Iterable, Iterator, List, Tuple

import yaml


DROP_KEY_EXACT = {
    "node_id",
    "gravatar_id",
    "avatar_url",
    "html_url",
    "url",
    "git_url",
    "ssh_url",
    "clone_url",
    "svn_url",
    "hooks_url",
    "issue_events_url",
    "assignees_url",
    "branches_url",
    "tags_url",
    "blobs_url",
    "git_tags_url",
    "git_refs_url",
    "trees_url",
    "statuses_url",
    "languages_url",
    "stargazers_url",
    "contributors_url",
    "subscribers_url",
    "subscription_url",
    "commits_url",
    "git_commits_url",
    "comments_url",
    "issue_comment_url",
    "contents_url",
    "compare_url",
    "merges_url",
    "archive_url",
    "downloads_url",
    "issues_url",
    "pulls_url",
    "milestones_url",
    "notifications_url",
    "labels_url",
    "releases_url",
    "deployments_url",
    "events_url",
    "received_events_url",
    "repo_url",
    "owner_url",
}
DROP_KEY_SUFFIXES = ("_url", "_urls")
DROP_DATETIME_KEYS = {"date", "created_at", "updated_at", "pushed_at", "expires_at"}

AUTH_LIKE_KEYS = {
    "authorization",
    "proxy-authorization",
    "x-api-key",
    "x-auth-token",
    "x-github-otp",
}
MASK_STRING_KEYS = {
    "login",
    "name",
    "full_name",
    "description",
    "email",
    "company",
    "message",
    "title",
    "path",
    "branch",
    "user",
    "owner",
}
MASK_STRING_CONTAINS = ("token", "secret", "password")
MASK_INT_KEYS = {"id"}
MASK_INT_SUFFIXES = ("_id",)


def sanitize_cassette_data(data: Any) -> bool:
    """Mutate the cassette data in-place to remove sensitive information."""
    if not isinstance(data, dict):
        return False
    changed = False
    _, root_changed = _sanitize_node(data, parent_key=None)
    changed |= root_changed
    interactions = data.get("interactions")
    if isinstance(interactions, list):
        for interaction in interactions:
            if not isinstance(interaction, dict):
                continue
            if _sanitize_http_body(interaction.get("request", {}).get("body")):
                changed = True
            if _sanitize_http_body(interaction.get("response", {}).get("body")):
                changed = True
    return changed


def sanitize_file(path: Path, *, dry_run: bool = False) -> bool:
    """Sanitize a cassette file. Returns True if the contents changed."""
    raw = path.read_text(encoding="utf-8")
    data = yaml.safe_load(raw)
    if data is None:
        return False
    changed = sanitize_cassette_data(data)
    if changed and not dry_run:
        serialized = yaml.safe_dump(data, sort_keys=False, allow_unicode=True)
        path.write_text(serialized, encoding="utf-8")
    return changed


def sanitize_paths(
    targets: Iterable[Path], *, dry_run: bool = False
) -> Tuple[int, int]:
    total = 0
    changed = 0
    for path in targets:
        if sanitize_file(path, dry_run=dry_run):
            changed += 1
        total += 1
    return changed, total


def _iter_cassette_paths(inputs: Iterable[str]) -> Iterator[Path]:
    for entry in inputs:
        path = Path(entry)
        if path.is_dir():
            yield from path.rglob("*.yaml")
        elif path.is_file():
            yield path


def _sanitize_node(value: Any, parent_key: str | None) -> Tuple[Any, bool]:
    if isinstance(value, dict):
        changed = False
        for key in list(value.keys()):
            child = value[key]
            normalized = key.lower()
            if _should_drop_key(normalized):
                del value[key]
                changed = True
                continue
            if key.lower() in DROP_DATETIME_KEYS:
                value[key] = "1970-01-01T00:00:00Z"
                changed = True
                continue
            sanitized_child, child_changed = _sanitize_node(child, normalized)
            if child_changed:
                value[key] = sanitized_child
                changed = True
        return value, changed
    if isinstance(value, list):
        changed = False
        for idx, item in enumerate(value):
            sanitized_item, item_changed = _sanitize_node(item, parent_key)
            if item_changed:
                value[idx] = sanitized_item
                changed = True
        return value, changed
    return _sanitize_primitive(value, parent_key)


def _sanitize_primitive(value: Any, parent_key: str | None) -> Tuple[Any, bool]:
    if isinstance(value, str):
        if parent_key in AUTH_LIKE_KEYS:
            masked = _mask_auth_value(value)
            return masked, masked != value
        if parent_key in MASK_STRING_KEYS or _key_contains_sensitive_fragment(
            parent_key
        ):
            masked = _mask_string(value)
            return masked, masked != value
        if _looks_like_secret(value):
            masked = _mask_string(value)
            return masked, masked != value
        return value, False
    if isinstance(value, int) and _should_mask_int_key(parent_key):
        masked_int = _mask_int(value)
        return masked_int, masked_int != value
    if isinstance(value, float) and _should_mask_int_key(parent_key):
        return 0.0, value != 0.0
    return value, False


def _should_drop_key(key: str) -> bool:
    if not key:
        return False
    if key in DROP_KEY_EXACT:
        return True
    return any(key.endswith(suffix) for suffix in DROP_KEY_SUFFIXES)


def _should_mask_int_key(key: str | None) -> bool:
    if not key:
        return False
    if key in MASK_INT_KEYS:
        return True
    return any(key.endswith(suffix) for suffix in MASK_INT_SUFFIXES)


def _key_contains_sensitive_fragment(key: str | None) -> bool:
    if not key:
        return False
    return any(fragment in key for fragment in MASK_STRING_CONTAINS)


def _mask_auth_value(value: str) -> str:
    lowered = value.lower()
    for prefix in ("bearer ", "token ", "basic "):
        if lowered.startswith(prefix):
            original_prefix = value[: len(prefix)]
            token = value[len(prefix) :]
            return f"{original_prefix}{_mask_token(token)}"
    if ":" in value:
        head, tail = value.split(":", 1)
        return f"{head}:{_mask_token(tail)}"
    return _mask_token(value)


def _mask_token(token: str) -> str:
    if not token:
        return token
    filler = "x"
    masked = "".join(filler if ch.isalnum() else ch for ch in token)
    return masked


def _mask_string(value: str) -> str:
    if not value:
        return value
    masked_chars: List[str] = []
    digest = hashlib.sha256(value.encode("utf-8")).digest()
    letters = "abcdefghijklmnopqrstuvwxyz"
    digits = "0123456789"
    for idx, ch in enumerate(value):
        if ch.isalpha():
            masked_chars.append(letters[digest[idx % len(digest)] % len(letters)])
        elif ch.isdigit():
            masked_chars.append(digits[digest[idx % len(digest)] % len(digits)])
        else:
            masked_chars.append(ch)
    return "".join(masked_chars)


def _mask_int(value: int) -> int:
    digest = hashlib.sha256(str(value).encode("utf-8")).hexdigest()
    return int(digest[:8], 16)


def _looks_like_secret(value: str) -> bool:
    lowered = value.lower()
    if "token " in lowered or "bearer " in lowered:
        return True
    return False


def _sanitize_http_body(body: Any) -> bool:
    if not isinstance(body, dict):
        return False
    content = body.get("string")
    if not isinstance(content, str):
        return False
    try:
        parsed = json.loads(content)
    except Exception:
        return False
    _, changed = _sanitize_node(parsed, parent_key=None)
    if changed:
        body["string"] = json.dumps(parsed, separators=(",", ":"), ensure_ascii=False)
    return changed


def main(argv: List[str] | None = None, vb: int = 0) -> int:
    parser = argparse.ArgumentParser(description="Sanitize VCR cassette files.")
    parser.add_argument(
        "paths", nargs="+", help="Cassette files or directories to sanitize."
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Report changes without writing files."
    )
    args = parser.parse_args(argv)
    targets = list(_iter_cassette_paths(args.paths))
    if not targets:
        print("No cassette files found.")
        return 1
    changed, total = sanitize_paths(targets, dry_run=args.dry_run)
    status = "would change" if args.dry_run else "updated"
    if vb:
        print(f"{status} {changed} cassette(s) out of {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
