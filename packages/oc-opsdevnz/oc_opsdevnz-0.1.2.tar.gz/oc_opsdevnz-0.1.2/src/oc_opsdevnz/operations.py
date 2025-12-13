from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, Optional, Sequence

import yaml

from .oc_client import GraphQLError, OpenCollectiveClient

Q_ACCOUNT = """
query Account($slug: String!) {
  account(slug: $slug) {
    __typename
    id
    slug
    name
    type
    isHost
    ... on Account { description longDescription tags website }
    ... on AccountWithHost { host { slug name } }
    ... on Account { socialLinks { type url } }
    stats { balance { currency } }
  }
}
"""

Q_HOST = """
query Host($slug: String!) {
  account(slug: $slug) {
    __typename
    id
    slug
    name
    type
    isHost
  }
}
"""

MUTATION_CREATE_ORG = """
mutation CreateOrganization($input: OrganizationCreateInput!) {
  createOrganization(organization: $input) {
    id
    slug
    name
    type
  }
}
"""

MUTATION_EDIT_ACCOUNT = """
mutation EditAccount($account: AccountUpdateInput!) {
  editAccount(account: $account) {
    id
    slug
    name
    description
    longDescription
    tags
    website
    socialLinks { type url }
    ... on AccountWithHost { host { slug name } }
  }
}
"""

MUTATION_CREATE_COLLECTIVE = """
mutation CreateCollective($input: CollectiveCreateInput!) {
  createCollective(collective: $input) {
    id
    slug
    name
    type
    ... on AccountWithHost { host { slug name } }
  }
}
"""

MUTATION_CREATE_PROJECT = """
mutation CreateProject($project: ProjectCreateInput!, $parent: AccountReferenceInput!) {
  createProject(project: $project, parent: $parent) {
    id
    slug
    name
    type
    ... on AccountWithParent { parent { slug } }
  }
}
"""

MUTATION_APPLY_TO_HOST = """
mutation ApplyToHost($collective: AccountReferenceInput!, $host: AccountReferenceInput!, $message: String) {
  applyToHost(collective: $collective, host: $host, message: $message) {
    id
    slug
    ... on AccountWithHost { host { slug name } }
  }
}
"""


@dataclass
class UpsertResult:
    slug: str
    created: bool = False
    updated: bool = False
    applied_to_host: bool = False
    warnings: list[str] = field(default_factory=list)
    account: Dict[str, Any] = field(default_factory=dict)


def load_items(path: Path) -> list[Dict[str, Any]]:
    """Load YAML or JSON list-of-dicts."""
    text = path.read_text()
    data = yaml.safe_load(text) if path.suffix.lower() in (".yaml", ".yml") else json.loads(text)
    if not isinstance(data, list):
        raise ValueError("Input file must contain a top-level array/list.")
    return data


def _arrays_equal(a: Optional[Sequence[Any]], b: Optional[Sequence[Any]]) -> bool:
    if a is None and b is None:
        return True
    if a is None or b is None:
        return False
    return list(a) == list(b)


def _norm_tags(v: Any) -> list[str]:
    if v is None:
        return []
    if isinstance(v, (list, tuple, set)):
        return [str(x) for x in v]
    return [str(v)]


def _upper_or_none(v: Optional[str]) -> Optional[str]:
    return (str(v).upper() if v is not None else None)


def _extract_website(acc: Dict[str, Any]) -> Optional[str]:
    if acc.get("website"):
        return acc["website"]
    for link in acc.get("socialLinks") or []:
        if link and link.get("type") == "WEBSITE":
            return link.get("url")
    return None


def _extract_social_links(acc: Dict[str, Any]) -> list[Dict[str, Any]]:
    return list(acc.get("socialLinks") or [])


def _upsert_website_link(links: list[Dict[str, Any]], website: Optional[str]) -> list[Dict[str, Any]]:
    if website is None:
        return links
    filtered = [l for l in links if (l or {}).get("type") != "WEBSITE"]
    filtered.append({"type": "WEBSITE", "url": website})
    return filtered


def _get_account_if_exists(client: OpenCollectiveClient, slug: str) -> Optional[Dict[str, Any]]:
    try:
        data = client.graphql(Q_ACCOUNT, {"slug": slug})
        return data.get("account")
    except GraphQLError as e:
        msg = str(e)
        not_found = (
            "No collective found with slug",
            "No account found with slug",
            "No organization found with slug",
        )
        if any(sig in msg for sig in not_found):
            return None
        raise


def _get_host_or_die(client: OpenCollectiveClient, slug: str) -> Dict[str, Any]:
    data = client.graphql(Q_HOST, {"slug": slug})
    host = data.get("account")
    if not host:
        raise RuntimeError(f"Host '{slug}' not found in this environment.")
    if not host.get("isHost"):
        raise RuntimeError(f"Account '{slug}' exists but isHost=false.")
    return host


def upsert_host(client: OpenCollectiveClient, item: Dict[str, Any]) -> UpsertResult:
    slug = item["slug"]
    desired_name = item["name"]
    desired_desc = item.get("description") or ""
    desired_long_desc = item.get("long_description") or item.get("longDescription")
    desired_site = item.get("website")
    desired_tags = _norm_tags(item.get("tags"))
    desired_currency = _upper_or_none(item.get("currency"))

    created = False
    updated = False
    warnings: list[str] = []

    acc = _get_account_if_exists(client, slug)

    if not acc:
        org_input: Dict[str, Any] = {
            "name": desired_name,
            "slug": slug,
            "description": desired_desc,
            "website": desired_site,
        }
        acc = client.graphql(MUTATION_CREATE_ORG, {"input": org_input})["createOrganization"]
        created = True

    website = _extract_website(acc)
    links = _extract_social_links(acc)
    merged_links = _upsert_website_link(links, desired_site)

    need_update = (
        acc.get("name") != desired_name
        or (acc.get("description") or "") != desired_desc
        or (
            desired_long_desc is not None
            and (acc.get("longDescription") or "") != str(desired_long_desc)
        )
        or not _arrays_equal(acc.get("tags"), desired_tags)
        or website != desired_site
    )

    if need_update:
        patch: Dict[str, Any] = {
            "id": acc["id"],
            "name": desired_name,
            "description": desired_desc,
            "tags": desired_tags,
            "socialLinks": merged_links,
        }
        if desired_long_desc is not None:
            patch["longDescription"] = str(desired_long_desc)
        acc = client.graphql(MUTATION_EDIT_ACCOUNT, {"account": patch})["editAccount"]
        updated = True

    # Currency comparison is informational only.
    current_currency = _upper_or_none(((acc.get("stats") or {}).get("balance") or {}).get("currency"))
    if desired_currency and desired_currency != current_currency:
        warnings.append(
            f"Currency mismatch: org has {current_currency or 'unset'}, yaml has {desired_currency}. "
            "Update Settings » Info before activating as host."
        )

    return UpsertResult(slug=slug, created=created, updated=updated, warnings=warnings, account=acc)


def upsert_collective(client: OpenCollectiveClient, item: Dict[str, Any]) -> UpsertResult:
    slug = item["slug"]
    desired_name = item["name"]
    desired_desc = item.get("description") or ""
    desired_tags = _norm_tags(item.get("tags"))
    host_slug = item.get("host_slug") or item.get("hostSlug")
    apply_flag = bool(item.get("apply_to_host") or item.get("applyToHost")) and bool(host_slug)
    host_apply_message = item.get("host_apply_message") or item.get("hostApplyMessage") or f"Please host {desired_name} (test/staging)."

    created = False
    updated = False
    applied = False

    # Pre-verify host if we're going to apply.
    if apply_flag and host_slug:
        _get_host_or_die(client, host_slug)

    acc = _get_account_if_exists(client, slug)
    if not acc:
        create_input = {
            "name": desired_name,
            "slug": slug,
            "description": desired_desc,
            "tags": desired_tags,
            "settings": {"features": {"expenses": True}},
        }
        acc = client.graphql(MUTATION_CREATE_COLLECTIVE, {"input": create_input})["createCollective"]
        created = True

    need_update = (
        acc.get("name") != desired_name
        or (acc.get("description") or "") != desired_desc
        or not _arrays_equal(acc.get("tags"), desired_tags)
    )

    if need_update:
        patch = {
            "id": acc["id"],
            "name": desired_name,
            "description": desired_desc,
            "tags": desired_tags,
        }
        acc = client.graphql(MUTATION_EDIT_ACCOUNT, {"account": patch})["editAccount"]
        updated = True

    if apply_flag and host_slug:
        current_host_slug = (acc.get("host") or {}).get("slug")
        if current_host_slug != host_slug:
            applied_resp = client.graphql(
                MUTATION_APPLY_TO_HOST,
                {"collective": {"id": acc["id"]}, "host": {"slug": host_slug}, "message": host_apply_message},
            )["applyToHost"]
            acc["host"] = applied_resp.get("host")
            applied = True

    return UpsertResult(slug=slug, created=created, updated=updated, applied_to_host=applied, account=acc)


def upsert_project(client: OpenCollectiveClient, item: Dict[str, Any]) -> UpsertResult:
    slug = item["slug"]
    parent_slug = item.get("parent_slug") or item.get("parentSlug")
    if not parent_slug:
        raise ValueError("Projects require parent_slug (the owning collective slug).")

    desired_name = item["name"]
    desired_desc = item.get("description") or ""
    desired_tags = _norm_tags(item.get("tags"))

    # Ensure parent exists
    parent = _get_account_if_exists(client, parent_slug)
    if not parent:
        raise RuntimeError(f"Parent collective '{parent_slug}' not found; create it first.")

    created = False
    updated = False

    acc = _get_account_if_exists(client, slug)
    if not acc:
        project_input: Dict[str, Any] = {
            "name": desired_name,
            "slug": slug,
            "description": desired_desc,
            "tags": desired_tags,
        }
        acc = client.graphql(MUTATION_CREATE_PROJECT, {"project": project_input, "parent": {"slug": parent_slug}})["createProject"]
        created = True

    need_update = (
        acc.get("name") != desired_name
        or (acc.get("description") or "") != desired_desc
        or not _arrays_equal(acc.get("tags"), desired_tags)
    )

    if need_update:
        patch = {
            "id": acc["id"],
            "name": desired_name,
            "description": desired_desc,
            "tags": desired_tags,
        }
        acc = client.graphql(MUTATION_EDIT_ACCOUNT, {"account": patch})["editAccount"]
        updated = True

    return UpsertResult(slug=slug, created=created, updated=updated, account=acc)
