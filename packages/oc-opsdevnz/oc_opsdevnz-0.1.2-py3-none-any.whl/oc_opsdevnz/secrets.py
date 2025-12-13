from op_opsdevnz.onepassword import SecretError, get_secret


def get_oc_token(*, secret_ref_env: str = "OC_SECRET_REF", env_override: str = "OC_TOKEN", prefer_cli: bool = True) -> str:
    """Resolve the OpenCollective token via 1Password (human CLI for local dev)."""
    try:
        return get_secret(
            secret_ref_env=secret_ref_env,  # op://... reference you exported
            env_override=env_override,      # optional local override
            prefer_cli=prefer_cli,          # force CLI for local dev
        )
    except SecretError as e:
        raise RuntimeError(f"Failed to resolve OC token: {e}") from e
