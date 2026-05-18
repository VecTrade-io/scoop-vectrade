"""Tests for scoop-vectrade GitHub configuration files."""

from pathlib import Path

import pytest

ROOT = Path(__file__).parent.parent
CI_FILE = ROOT / ".github" / "workflows" / "ci.yml"
CODEOWNERS_FILE = ROOT / ".github" / "CODEOWNERS"
PR_TEMPLATE_FILE = ROOT / ".github" / "PULL_REQUEST_TEMPLATE.md"
ISSUE_TEMPLATE_DIR = ROOT / ".github" / "ISSUE_TEMPLATE"
SECURITY_FILE = ROOT / "SECURITY.md"


@pytest.fixture
def ci_content():
    return CI_FILE.read_text()


@pytest.fixture
def codeowners_content():
    return CODEOWNERS_FILE.read_text()


@pytest.fixture
def pr_template_content():
    return PR_TEMPLATE_FILE.read_text()


@pytest.fixture
def security_content():
    return SECURITY_FILE.read_text()


class TestGitHubConfigExists:
    """Verify all GitHub config files exist."""

    def test_ci_workflow_exists(self):
        assert CI_FILE.is_file()

    def test_codeowners_exists(self):
        assert CODEOWNERS_FILE.is_file()

    def test_pr_template_exists(self):
        assert PR_TEMPLATE_FILE.is_file()

    def test_issue_template_dir_exists(self):
        assert ISSUE_TEMPLATE_DIR.is_dir()

    def test_security_file_exists(self):
        assert SECURITY_FILE.is_file()

    def test_bug_report_template_exists(self):
        assert (ISSUE_TEMPLATE_DIR / "bug_report.md").is_file()


class TestCIWorkflowContent:
    """Verify CI workflow configuration details."""

    def test_name_is_ci(self, ci_content):
        assert "name: CI" in ci_content

    def test_triggers_on_push(self, ci_content):
        assert "push:" in ci_content

    def test_triggers_on_pr(self, ci_content):
        assert "pull_request:" in ci_content

    def test_triggers_on_workflow_dispatch(self, ci_content):
        assert "workflow_dispatch:" in ci_content

    def test_has_read_permissions(self, ci_content):
        assert "contents: read" in ci_content

    def test_uses_checkout_v4(self, ci_content):
        assert "actions/checkout@v4" in ci_content

    def test_validates_json(self, ci_content):
        assert "json" in ci_content.lower()

    def test_runs_pytest(self, ci_content):
        assert "pytest" in ci_content

    def test_uses_python_setup(self, ci_content):
        assert "setup-python" in ci_content

    def test_targets_main_branch(self, ci_content):
        assert "main" in ci_content

    def test_targets_fix_branches(self, ci_content):
        assert "fix/**" in ci_content

    def test_has_windows_runner(self, ci_content):
        assert "windows" in ci_content

    def test_has_multiple_jobs(self, ci_content):
        assert ci_content.count("runs-on:") >= 2

    def test_validates_scoop_manifest(self, ci_content):
        assert "scoop" in ci_content.lower()


class TestCodeowners:
    """Verify CODEOWNERS configuration."""

    def test_has_global_owner(self, codeowners_content):
        assert "*" in codeowners_content

    def test_references_vectrade_team(self, codeowners_content):
        assert "@VecTrade-io/" in codeowners_content

    def test_is_not_empty(self, codeowners_content):
        assert len(codeowners_content.strip()) > 0


class TestPRTemplate:
    """Verify PR template structure."""

    def test_has_summary(self, pr_template_content):
        assert "Summary" in pr_template_content

    def test_has_checklist(self, pr_template_content):
        assert "- [ ]" in pr_template_content

    def test_warns_about_auto_generated(self, pr_template_content):
        assert "auto-generated" in pr_template_content.lower() or "GoReleaser" in pr_template_content

    def test_mentions_tests(self, pr_template_content):
        assert "pytest" in pr_template_content or "test" in pr_template_content.lower()


class TestIssueTemplates:
    """Verify issue templates."""

    def test_bug_report_has_frontmatter(self):
        content = (ISSUE_TEMPLATE_DIR / "bug_report.md").read_text()
        assert content.startswith("---")
        assert "name:" in content
        assert "about:" in content

    def test_bug_report_has_steps(self):
        content = (ISSUE_TEMPLATE_DIR / "bug_report.md").read_text()
        assert "Steps to Reproduce" in content or "Reproduce" in content

    def test_bug_report_has_environment(self):
        content = (ISSUE_TEMPLATE_DIR / "bug_report.md").read_text()
        assert "Environment" in content

    def test_bug_report_mentions_scoop(self):
        content = (ISSUE_TEMPLATE_DIR / "bug_report.md").read_text()
        assert "scoop" in content


class TestSecurity:
    """Verify SECURITY.md."""

    def test_has_reporting_section(self, security_content):
        assert "Reporting" in security_content

    def test_has_email(self, security_content):
        assert "security@vectrade.io" in security_content

    def test_has_response_time(self, security_content):
        assert "48 hours" in security_content

    def test_mentions_vectrade_cli(self, security_content):
        assert "VecTrade CLI" in security_content

    def test_warns_against_public_issues(self, security_content):
        assert "Do not open" in security_content or "do not" in security_content.lower()
