import shutil
import subprocess
import sys

import pytest


@pytest.mark.parametrize(
    "pkg",
    [
        "flask_principal-stubs",
        "invenio_audit_logs-stubs",
        "invenio_communities-stubs",
        "invenio_db-stubs",
        "invenio_drafts_resources-stubs",
        "invenio_records_permissions-stubs",
        "invenio_records_resources-stubs",
        "invenio_records-stubs",
        "invenio_requests-stubs",
        "invenio_vocabularies-stubs",
        "invenio_pidstore-stubs",
        "invenio_search-stubs",
        "flask_resources-stubs",
        "invenio_jsonschemas-stubs",
    ],
)
def test_mypy_for_each_package(pkg):
    """Run mypy for each package."""

    shutil.rmtree(".mypy_cache", ignore_errors=True)

    subprocess.check_call(
        [
            sys.executable,
            "-m",
            "mypy",
            "--check-untyped-defs",
            "--ignore-missing-imports",
            pkg,
        ],
        stdout=sys.stdout,
        stderr=sys.stderr,
    )
