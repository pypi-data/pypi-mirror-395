import pytest
from click.testing import CliRunner

from super_pocket.cli import cli
from super_pocket.project import req_to_date as req_module
from super_pocket.project.req_to_date import PackageResult, req_to_date_cli


@pytest.fixture
def runner():
    return CliRunner()


def test_pocket_req_to_date_subcommand_invokes_runner(monkeypatch, runner):
    captured = {}
    fake_results = [
        PackageResult(
            package="click",
            current_version="8.1.0",
            latest_patch=None,
            latest_overall="8.1.7",
            status="outdated",
        ),
        PackageResult(
            package="rich",
            current_version="13.0.0",
            latest_patch=None,
            latest_overall="13.0.0",
            status="up-to-date",
        ),
    ]

    def fake_run(packages):
        captured["packages"] = packages
        return fake_results

    monkeypatch.setattr("super_pocket.cli.run_req_to_date", fake_run)

    result = runner.invoke(
        cli,
        ["project", "req-to-date", "click==8.1.0", "rich==13.0.0"],
    )

    assert result.exit_code == 0
    assert captured["packages"] == ("click==8.1.0", "rich==13.0.0")
    assert "click 8.1.0" in result.output
    assert "rich 13.0.0" in result.output


def test_standalone_req_update_accepts_multiple_inputs(tmp_path, monkeypatch, runner):
    captured = {}
    requirements = tmp_path / "requirements.txt"
    requirements.write_text("demo==0.1.0\n", encoding="utf-8")

    fake_results = [
        PackageResult(
            package="demo",
            current_version="0.1.0",
            latest_patch=None,
            latest_overall="0.2.0",
            status="outdated",
        ),
        PackageResult(
            package="other",
            current_version="1.0.0",
            latest_patch=None,
            latest_overall="1.1.0",
            status="outdated",
        ),
    ]

    def fake_run(packages):
        captured["packages"] = packages
        return fake_results

    monkeypatch.setattr("super_pocket.project.req_to_date.run_req_to_date", fake_run)

    result = runner.invoke(
        req_to_date_cli,
        ["demo==0.1.0", str(requirements), "other==1.0.0"],
    )

    assert result.exit_code == 0
    assert captured["packages"] == (
        "demo==0.1.0",
        str(requirements),
        "other==1.0.0",
    )
    assert "demo 0.1.0" in result.output
    assert "other 1.0.0" in result.output
