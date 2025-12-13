# oc_opsdevnz

Staging-first OpenCollective client and CLI for OpsDev.nz. Resolves tokens from 1Password via `op-opsdevnz` and defaults to the staging API unless you explicitly opt into prod.

## Features
- httpx GraphQL client with retries/backoff and redacted error messages.
- Environment guardrails: staging by default, `for_prod()`/`--prod` required for production.
- Token resolution via `OC_SECRET_REF`/`OC_TOKEN` using `op-opsdevnz`.
- CLI helpers for whoami, host organization upserts, collective creation/apply-to-host flows, and project creation from YAML/JSON.

## Install
```bash
pip install oc-opsdevnz op-opsdevnz
# or editable while hacking in this repo
pip install -e modules/oc_opsdevnz[dev]
```

## CLI (staging by default)
```bash
export OC_SECRET_REF="op://startmeup.nz/api-staging.opencollective.com/credential"  # or set OC_TOKEN

# Fetch an account/collective by slug
oc-opsdevnz whoami opsdevnz

# Show installed version
oc-opsdevnz version

# Create/update host orgs from YAML
oc-opsdevnz hosts --file hosts.yaml

# Create/update collectives and optionally apply to a host
oc-opsdevnz collectives --file collectives.yaml

# Create/update projects under a parent collective
oc-opsdevnz projects --file projects.yaml
```
Use `--file` or `--config` to point at any filename you prefer; defaults above are just examples. Use `--prod` to target production (only when you mean it), or `--api-url` to override explicitly.

### Example YAML shapes
`hosts.yaml` (real staging values):
```yaml
- name: StartMeUp.NZ
  slug: startmeup-nz
  description: Fiscal sponsor for OpsDev.NZ and NZ startups (staging)
  website: https://startmeup.nz
  currency: nzd
  tags: [fiscal-host, newzealand, aotearoa]
```

`collectives.yaml` (real staging values):
```yaml
- name: OpsDev.NZ
  slug: opsdev-nz
  description: OpsDev.NZ community and projects.
  tags: [opsdev, operations, engineering, nz]
  host_slug: startmeup-nz
  apply_to_host: true
  host_apply_message: Please host OpsDev.NZ on staging.
```

`projects.yaml`:
```yaml
- name: GetJJobs.NZ
  slug: getjjobs-nz
  parent_slug: opsdev-nz
  description: Pilot job-matching project under OpsDev.NZ.
  tags: [jobs, pilot]
```

## Python API
```python
from oc_opsdevnz import OpenCollectiveClient

client = OpenCollectiveClient.for_staging()
data = client.graphql("query { account(slug:\"opsdevnz\") { id slug name } }")

prod_client = OpenCollectiveClient.for_prod()  # explicit opt-in
```

Helpers for YAML-driven workflows:
```python
from oc_opsdevnz import load_items, upsert_collective, upsert_host, upsert_project
from pathlib import Path

client = OpenCollectiveClient.for_staging()
for host in load_items(Path("hosts.yaml")):
    upsert_host(client, host)
for project in load_items(Path("projects.yaml")):
    upsert_project(client, project)
```

## Development
```bash
cd modules/oc_opsdevnz
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
pytest
```

## License
Apache-2.0 © OpsDev.nz
