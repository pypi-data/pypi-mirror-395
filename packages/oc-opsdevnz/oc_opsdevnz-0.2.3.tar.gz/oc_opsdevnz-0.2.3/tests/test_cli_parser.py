from oc_opsdevnz.cli import build_parser


def _parse(argv: list[str]):
    parser = build_parser()
    return parser.parse_args(argv)


def test_hosts_accepts_config_alias():
    args = _parse(["hosts", "--config", "opencollective/staging-host.yaml"])
    assert args.config == "opencollective/staging-host.yaml"
    # --file keeps its default; --config is a separate alias
    assert args.file == "hosts.yaml"
    assert args.staging is False
    assert args.test is False
    assert args.prod is False


def test_collectives_accepts_config_alias():
    args = _parse(["collectives", "--config", "opencollective/staging-collectives.yaml"])
    assert args.config == "opencollective/staging-collectives.yaml"
    assert args.file == "collectives.yaml"


def test_projects_accepts_config_alias():
    args = _parse(["projects", "--config", "opencollective/staging-projects.yaml"])
    assert args.config == "opencollective/staging-projects.yaml"
    assert args.file == "projects.yaml"
    assert args.staging is False
    assert args.test is False
    assert args.prod is False


def test_version_command_outputs_version(capsys):
    args = _parse(["version"])
    assert args.command == "version"
    assert callable(args.func)
    # Execute and capture stdout
    args.func(args)
    out = capsys.readouterr().out.strip()
    assert out


def test_staging_flags_are_aliases():
    args = _parse(["hosts", "--staging"])
    assert args.staging is True
    assert args.test is False

    args2 = _parse(["hosts", "--test"])
    assert args2.test is True
    assert args2.staging is False
