import os
from pprint import pprint

import pytest

from rstms_mailgun.context import Context


@pytest.fixture
def domain():
    return os.environ.get("TEST_DOMAIN", "example.org")


@pytest.fixture
def spf_domain():
    return os.environ.get("SPF_TEST_DOMAIN", "example.org")


@pytest.fixture
def api_key():
    return os.environ["MAILGUN_API_KEY"]


@pytest.fixture
def ctx(api_key, domain):
    return Context(api_key, domain)


@pytest.fixture
def spf_ctx(api_key, spf_domain):
    return Context(api_key, spf_domain)


def test_ctx_init(ctx):
    assert ctx


def test_ctx_record_name(spf_ctx):
    domain = spf_ctx.domain
    assert "@" == spf_ctx.record_name(dict(name="@"))
    assert "@" == spf_ctx.record_name(dict(name=domain))
    assert "host" == spf_ctx.record_name(dict(name="host." + domain))


@pytest.mark.skip
def test_ctx_get_spf(spf_ctx):
    domain = spf_ctx.domain
    records = spf_ctx.get_deployed_dns_records(spf=True)
    assert isinstance(records, list)
    breakpoint()
    record = records[0]
    assert "id" in record
    assert record["name"] == "@"
    assert record["type"] == "TXT"
    assert record["domain"] == domain
    assert record["value"].startswith("v=spf1")


def test_ctx_get_domains(ctx):
    domains = ctx.get_domains()
    pprint(domains)


def test_ctx_get_smtp_credentials(ctx):
    smtp = ctx.get_smtp_credentials()
    assert isinstance(smtp, list)
    for user in smtp:
        assert isinstance(user, str)
        assert "@" in user
    pprint(smtp)


def test_ctx_reset_smtp_credentials_generate_password(ctx):
    smtp = ctx.reset_smtp_credentials()
    pprint(smtp)


def test_ctx_reset_smtp_credentials_specify_password(ctx):
    smtp = ctx.reset_smtp_credentials(password="kniiggggiiitts")
    pprint(smtp)
