import argparse
import json
import sys
from pathlib import Path

from . import __version__
from .oc_client import OpenCollectiveClient, PROD_URL
from .operations import UpsertResult, load_items, upsert_collective, upsert_host, upsert_project

WHOAMI_QUERY = """
query Account($slug: String!) {
  account(slug: $slug) {
    id
    slug
    name
    type
  }
}
"""


def _add_common_options(ap: argparse.ArgumentParser) -> None:
    ap.add_argument("--prod", action="store_true", help="Use production API (staging is the default).")
    ap.add_argument("--api-url", help="Override GraphQL endpoint.")
    ap.add_argument("--token", help="Override token (defaults to OC_SECRET_REF/OC_TOKEN).")
    ap.add_argument("--auth-mode", choices=["personal", "oauth"], default="personal", help="Personal-Token vs OAuth bearer.")
    ap.add_argument("--log-requests", action="store_true", help="Print request summaries (also via OC_DEBUG=1).")


def _client_from_args(args) -> OpenCollectiveClient:
    kwargs = {"token": args.token, "auth_mode": args.auth_mode, "log_requests": args.log_requests}
    if args.api_url:
        return OpenCollectiveClient(api_url=args.api_url, allow_prod=args.api_url == PROD_URL, **kwargs)
    if args.prod:
        return OpenCollectiveClient.for_prod(**kwargs)
    return OpenCollectiveClient.for_staging(**kwargs)


def _print_result(label: str, result: UpsertResult) -> None:
    summary = {
        "slug": result.slug,
        "created": result.created,
        "updated": result.updated,
        "applied_to_host": result.applied_to_host,
        "warnings": result.warnings,
    }
    print(f"[{label}] {json.dumps(summary)}")
    print(json.dumps({"account": result.account}, indent=2))


def cmd_whoami(args) -> int:
    client = _client_from_args(args)
    data = client.graphql(WHOAMI_QUERY, {"slug": args.slug})
    print(json.dumps(data, indent=2))
    return 0


def cmd_hosts(args) -> int:
    path = Path(args.config or args.file)
    if not path.exists():
        print(f"hosts file not found: {path}", file=sys.stderr)
        return 2

    items = load_items(path)
    client = _client_from_args(args)

    for item in items:
        if args.only and item.get("slug") != args.only:
            continue
        result = upsert_host(client, item)
        _print_result("host", result)
    return 0


def cmd_collectives(args) -> int:
    path = Path(args.config or args.file)
    if not path.exists():
        print(f"collectives file not found: {path}", file=sys.stderr)
        return 2

    items = load_items(path)
    client = _client_from_args(args)

    for item in items:
        if args.only and item.get("slug") != args.only:
            continue
        result = upsert_collective(client, item)
        _print_result("collective", result)
    return 0


def cmd_projects(args) -> int:
    path = Path(args.config or args.file)
    if not path.exists():
        print(f"projects file not found: {path}", file=sys.stderr)
        return 2

    items = load_items(path)
    client = _client_from_args(args)

    for item in items:
        if args.only and item.get("slug") != args.only:
            continue
        result = upsert_project(client, item)
        _print_result("project", result)
    return 0


def cmd_version(args) -> int:  # noqa: ARG001 - required by argparse
    print(__version__)
    return 0


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="OpenCollective automation helpers (staging-first).")
    sub = ap.add_subparsers(dest="command", required=True)

    p_whoami = sub.add_parser("whoami", help="Fetch account/collective metadata by slug.")
    _add_common_options(p_whoami)
    p_whoami.add_argument("slug", help="Account slug to query.")
    p_whoami.set_defaults(func=cmd_whoami)

    p_hosts = sub.add_parser("hosts", help="Create/update host organizations from YAML/JSON.")
    _add_common_options(p_hosts)
    p_hosts.add_argument("--file", default="hosts.yaml", help="Path to hosts YAML/JSON (array).")
    p_hosts.add_argument("--config", help="Alias for --file when using env-named configs (e.g., staging-host.yaml).")
    p_hosts.add_argument("--only", help="Only process the matching slug.")
    p_hosts.set_defaults(func=cmd_hosts)

    p_colls = sub.add_parser("collectives", help="Create/update collectives and optionally apply to a host.")
    _add_common_options(p_colls)
    p_colls.add_argument("--file", default="collectives.yaml", help="Path to collectives YAML/JSON (array).")
    p_colls.add_argument(
        "--config", help="Alias for --file when using env-named configs (e.g., staging-collectives.yaml)."
    )
    p_colls.add_argument("--only", help="Only process the matching slug.")
    p_colls.set_defaults(func=cmd_collectives)

    p_projects = sub.add_parser("projects", help="Create/update projects under a parent collective from YAML/JSON.")
    _add_common_options(p_projects)
    p_projects.add_argument("--file", default="projects.yaml", help="Path to projects YAML/JSON (array).")
    p_projects.add_argument(
        "--config", help="Alias for --file when using env-named configs (e.g., staging-projects.yaml)."
    )
    p_projects.add_argument("--only", help="Only process the matching slug.")
    p_projects.set_defaults(func=cmd_projects)

    p_version = sub.add_parser("version", help="Print package version.")
    _add_common_options(p_version)
    p_version.set_defaults(func=cmd_version)

    return ap


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        return args.func(args)
    except Exception as e:  # pragma: no cover - convenience for CLI use
        print(f"[error] {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
