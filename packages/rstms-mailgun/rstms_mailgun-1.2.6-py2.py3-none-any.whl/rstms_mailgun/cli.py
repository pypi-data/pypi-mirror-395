"""Console script for rstms_mailgun."""

import json
import shlex
import subprocess
import sys
import time

import click
import click.core

from .context import Context
from .exception_handler import ExceptionHandler
from .shell import _shell_completion
from .version import __timestamp__, __version__

header = f"{__name__.split('.')[0]} v{__version__} {__timestamp__}"

VERIFY_INTERVAL = 5
VERIFY_TIMEOUT = 60


def fail(msg):
    click.echo(msg, err=True)
    sys.exit(-1)


def _ehandler(ctx, option, debug):
    ctx.obj = dict(ehandler=ExceptionHandler(debug))
    ctx.obj["debug"] = debug


@click.group("mailgun", context_settings={"auto_envvar_prefix": "MAILGUN"})
@click.version_option(message=header)
@click.option("-k", "--api-key", envvar="MAILGUN_API_KEY", show_envvar=True, help="mailgun API key")
@click.option("-d", "--debug", is_eager=True, is_flag=True, callback=_ehandler, help="debug mode")
@click.option("-v", "--verbose", is_flag=True, help="enable verbose output")
@click.option("-q", "--quiet", is_flag=True, help="suppress stdout")
@click.option("-c", "--compact", is_flag=True, help="compact JSON output")
@click.option("-j/-J", "--json/--no-json", "json_format", is_flag=True, default=True, help="output JSON")
@click.option("-f", "--force", is_flag=True, help="bypass confirmation")
@click.argument("domain")
@click.option(
    "--shell-completion",
    is_flag=False,
    flag_value="[auto]",
    callback=_shell_completion,
    help="configure shell completion",
)
@click.pass_context
def cli(ctx, domain, api_key, verbose, debug, quiet, json_format, compact, shell_completion, force):
    """rstms_mailgun top-level help"""
    ctx.obj = Context(api_key, domain)
    ctx.obj.json = json_format
    ctx.obj.quiet = quiet
    ctx.obj.compact = compact
    ctx.obj.verbose = verbose
    ctx.obj.force = force


@cli.command("list")
@click.pass_obj
def domains(ctx):
    """list configured domains"""
    ctx.list()


@cli.command()
@click.pass_obj
def exists(ctx):
    """exit code indicates domain configured in mailgun account"""
    ctx.validate(exists=None)
    ret = ctx.domain in ctx.domain_names
    ctx.exit(0 if ret else -1, str(ret))


@cli.command
@click.pass_obj
def detail(ctx):
    """detail for named domain"""
    ctx.validate(exists=True)
    result = ctx.get(f"v4/domains/{ctx.domain}")
    ctx.exit(0, result)


@cli.command
@click.pass_obj
@click.option("-r", "--reset", is_flag=True, help="reset SMTP account and generate password")
@click.option("-u", "--username", default="postmaster", show_default=True, help="set username")
@click.option("-p", "--password", help="specify password '-' reads from stdin)")
def smtp(ctx, reset, username, password):
    """show or reset SMTP credentials for named domain"""
    ctx.validate(exists=True)
    if reset:
        if password == "-":
            password = sys.stdin.readline().strip()
        result = ctx.reset_smtp_credentials(username, password)
    else:
        result = ctx.get_smtp_credentials()
    ctx.exit(0, result)


@cli.command
@click.pass_obj
def delete(ctx):
    """delete a domain"""
    ctx.validate(exists=True)
    if not ctx.force:
        click.confirm(f"Confirm DELETE mailgun domain {ctx.domain}?", abort=True)
    result = ctx.delete(f"v3/domains/{ctx.domain}")
    ctx.exit(0, result)


@cli.command
@click.option("-w", "--wildcard", is_flag=True, help="accept email from subdomains when sending")
@click.option("-d", "--dkim-key-size", type=click.Choice(["1024", "2048"]), default=None, help="set DKIM key size")
@click.option("-P", "--smtp-password", help="SMTP authentication password")
@click.option("-A", "--force-dkim-authority", is_flag=True, help="DKIM authority will be the created domain")
@click.option("-R", "--force-root-dkim-host", is_flag=True, help="DKIM authority will be the root domain")
@click.option("-h", "--dkim-host-name", help="DKIM host name")
@click.option("-s", "--dkim-selector", help="set DKIM selector for created domain")
@click.option("-p", "--pool-id", help="request IP Pool")
@click.option("-i", "--assign-ip", help="comma separated list of IP addresses assigned to new domain")
@click.option("-W", "--web-scheme", type=click.Choice(["http", "https"]), default=None, help="domain web scheme")
@click.option("-f", "--force", is_flag=True, help="bypass confirmation")
@click.pass_obj
def create(  # noqa: C901
    ctx,
    wildcard,
    dkim_key_size,
    smtp_password,
    force_dkim_authority,
    force_root_dkim_host,
    dkim_host_name,
    dkim_selector,
    pool_id,
    assign_ip,
    web_scheme,
    force,
):
    """create domain"""

    ctx.validate(exists=False)
    params = dict(name=ctx.domain)
    if wildcard:
        params["wildcard"] = True
    if dkim_key_size:
        params["dkim_key_size"] = dkim_key_size
    if smtp_password:
        params["smtp_password"] = smtp_password
    if force_dkim_authority:
        params["force_dkim_authority"] = True
    if force_root_dkim_host:
        params["force_root_dkim_host"] = True
    if dkim_host_name:
        params["dkim_host_name"] = dkim_host_name
    if dkim_selector:
        params["dkim_selector"] = dkim_selector
    if pool_id:
        params["pool_id"] = pool_id
    if assign_ip:
        params["ips"] = assign_ip
    if web_scheme:
        params["web_scheme"] = web_scheme
    if not ctx.force:
        click.echo("Creating domain {ctx.domain}:")
        click.echo(json.dumps(params, indent=2))
        click.confirm("Confirm?", abort=True)
    result = ctx.post("v4/domains", params=params)
    ctx.exit(0, result["message"])


@cli.command
@click.option("-P", "--smtp-password", help="SMTP authentication password")
@click.option("-w", "--wildcard", is_flag=True, help="accept email from subdomains when sending")
@click.option("-W", "--web-scheme", type=click.Choice(["http", "https"]), default=None, help="domain web scheme")
@click.option("-f", "--mail-from", help="MAILFROM hostname for outbound email")
@click.option(
    "-s", "--spam-action", type=click.Choice(["disabled", "tag", "block"]), default=None, help="domain web scheme"
)
@click.pass_obj
def update(ctx, smtp_password, wildcard, web_scheme, spam_action, mail_from):
    """update domain configuration"""

    ctx.validate(exists=True)

    if mail_from:
        result = ctx.put(f"v3/domains/{ctx.domain}/mailfrom_host", params=dict(mailfrom_host=mail_from))
        ctx.exit(0, result)

    params = dict(name=ctx.domain)
    if wildcard:
        params["wildcard"] = True
    if smtp_password:
        params["smtp_password"] = smtp_password
    if web_scheme:
        params["web_scheme"] = web_scheme
    if spam_action:
        params["spam_action"] = spam_action

    if len(params.keys()) > 1:
        result = ctx.put(f"v4/domains/{ctx.domain}", params=params)
        msg = result["message"]
    else:
        msg = "unchanged"
    ctx.exit(0, msg)


@cli.command
@click.option("-w", "--wait", is_flag=True, help="wait for verification")
@click.option("-i", "--interval", type=int, default=VERIFY_INTERVAL, help="seconds between verify requests")
@click.option("-t", "--timeout", type=int, default=VERIFY_TIMEOUT, help="wait timeout in seconds")
@click.argument("domain", required=False)
@click.pass_obj
def verify(ctx, domain, wait, interval, timeout):
    """request domain verification"""
    ctx.validate(exists=True)

    status = ctx.get_status()

    request_time = 0
    timeout_time = 0

    if timeout:
        timeout_time = time.time() + timeout
    else:
        timeout_time = 0

    while status["state"] != "active":

        if time.time() > request_time:
            if ctx.verbose:
                click.echo("\nRequesting verification...", nl=False)
            response = ctx.put(f"v4/domains/{ctx.domain}/verify")
            requested = True
            if ctx.verbose:
                click.echo(f"{response['message']}")
            request_time = time.time() + interval

        if not wait:
            break

        if ctx.verbose:
            if requested:
                requested = False
                click.echo(f"Status: {status['state']}; waiting...", nl=False)
            else:
                click.echo(".", nl=False)

        if timeout and time.time() > timeout_time:
            fail("Timeout")

        time.sleep(1)
        status = ctx.get_status()

    if ctx.verbose:
        click.echo()

    ctx.exit(0, status)


@cli.command
@click.argument("domain", required=False)
@click.pass_obj
def status(ctx, domain):
    """output verification state"""
    ctx.validate(exists=True)
    status = ctx.get_status()
    ret = 0 if status["state"] == "active" else -1
    ctx.exit(ret, status)


def dns_cmd(*args, dry_run=False, parse_json=True):
    if dry_run:
        click.echo(shlex.join(args))
        ret = []
    else:
        proc = subprocess.run(args, text=True, capture_output=True, check=True)
        if parse_json:
            ret = json.loads(proc.stdout)
        else:
            ret = proc.stdout.strip()
    return ret


def find_dns_record(record, dns_records):
    for dns in dns_records:
        if dns["domain"] == record["domain"] and dns["name"] == record["name"] and dns["type"] == record["type"]:
            return dns
    return {}


@cli.command
@click.option("-d", "--delete", "dns_delete", is_flag=True, help="delete from DNS")
@click.option("-u", "--update", "dns_update", is_flag=True, help="update to DNS")
@click.option("-q/-Q", "--query/--no-query", "dns_query", is_flag=True, default=True, help="query DNS")
@click.option("-c/-C", "--cname/--no-cname", is_flag=True, default=False, help="include CNAME record")
@click.option("-s/-S", "--spf/--no-spf", is_flag=True, default=True, help="include SPF record")
@click.option("-k/-K", "--dkim/--no-dkim", is_flag=True, default=True, help="include DKIM record")
@click.option("-t", "--ttl", type=int, default=60, show_default=True, help="DNS TTL")
@click.pass_obj
def dns(ctx, dns_update, dns_delete, dns_query, ttl, cname, spf, dkim):  # noqa: C901
    """show|update|delete required DNS records"""

    ctx.validate(exists=True)
    mailgun_records = ctx.get_dns_records()

    records = []
    for record in mailgun_records.values():
        out = {}
        if record["record_type"] == "CNAME" and not cname:
            continue
        if record["record_type"] == "TXT":
            if "_domainkey" in record["name"] and not dkim:
                continue
            if "v=spf1" in record["value"] and not spf:
                continue

        out["domain"] = ctx.domain
        out["name"] = ctx.record_name(record)
        out["type"] = record["record_type"]
        out["value"] = record["value"]
        out["dns"] = "unknown"
        records.append(out)

    dns_records = []

    if dns_update or dns_delete or dns_query:

        dns_records = ctx.get_deployed_dns_records(
            spf=spf,
            dkim=ctx.record_name(mailgun_records["DKIM"]) if dkim else False,
            cname=ctx.record_name(mailgun_records["CNAME"]) if cname else False,
        )

        for record in records:
            dns_record = find_dns_record(record, dns_records)
            record["id"] = dns_record.get("id", None)
            if dns_record.get("value", None) is None:
                record["dns"] = "absent"
            elif record["value"] == dns_record.get("value", None):
                record["dns"] = "present"
            else:
                record["dns"] = "mismatch"

    if dns_delete or dns_update:
        for dns in dns_records:
            deleted_id = ctx.cloudflare.delete_record(dns)
            for record in records:
                if record["id"] == deleted_id:
                    record["id"] = None
                    record["dns"] = "deleted"

    if dns_update:
        for record in records:
            added_id = ctx.cloudflare.add_record(ctx.domain, record["type"], record["name"], record["value"], ttl)
            record["dns"] = "updated"
            record["id"] = added_id

    for record in records:
        record.pop("id", None)

    if ctx.json:
        ret = records
    else:
        ret = []
        for record in records:
            name = record["name"]
            if name == ctx.domain or name == "@":
                name = ctx.domain
            else:
                name = ".".join([name, ctx.domain])
            ret.append(
                " ".join(
                    [
                        record["type"],
                        name,
                        record["value"],
                        record.get("dns", ""),
                    ]
                )
            )

    ctx.exit(0, ret)


@cli.command
@click.pass_obj
def bounces(ctx):
    """output bounce data"""
    ctx.validate(exists=True)
    bounces = ctx.get_bounces()
    ctx.exit(0, bounces)


@cli.command
@click.pass_obj
def events(ctx):
    """output events data"""
    ctx.validate(exists=True)
    ctx.exit(0, ctx.get_events())


if __name__ == "__main__":
    sys.exit(cli())  # pragma: no cover
