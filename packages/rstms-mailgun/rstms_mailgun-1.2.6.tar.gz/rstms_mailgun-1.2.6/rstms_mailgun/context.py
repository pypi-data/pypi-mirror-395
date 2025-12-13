"""Console script for rstms_mailgun."""

import json
import sys

import click
import click.core
import requests
import rstms_cloudflare
from requests.auth import HTTPBasicAuth


class Context:
    def __init__(self, api_key, domain):
        self.api_key = api_key
        self.base_url = "https://api.mailgun.net"
        self.auth = HTTPBasicAuth("api", api_key)
        self.json = True
        self.domain = domain
        self.quiet = False
        self.compact = False
        self.get_domains()
        self.cloudflare = rstms_cloudflare.cloudflare.API()

    def _request(self, func, path, **kwargs):
        url = f"{self.base_url}/{path}"
        kwargs["auth"] = self.auth
        response = func(url, **kwargs)
        response.raise_for_status()
        return response.json()

    def get(self, path, **kwargs):
        return self._request(requests.get, path, **kwargs)

    def put(self, path, **kwargs):
        return self._request(requests.put, path, **kwargs)

    def delete(self, path, **kwargs):
        return self._request(requests.delete, path, **kwargs)

    def post(self, path, **kwargs):
        return self._request(requests.post, path, **kwargs)

    def validate(self, exists=True, dns_domain=True):
        if exists is True:
            if self.domain not in self.domain_names:
                raise RuntimeError(f"Unknown domain: {repr(self.domain)}")
        elif exists is False:
            if self.domain in self.domain_names:
                raise RuntimeError(f"Domain exists: {repr(self.domain)}")

        if dns_domain:
            if "." not in self.domain:
                raise RuntimeError(f"Unexpected domain format: {repr(self.domain)}")

    def get_domains(self):
        result = self.get("v4/domains")
        self.domains = {item["name"]: item for item in result["items"]}
        self.domain_names = list(self.domains.keys())
        return self.domains

    def exit(self, exit_code=0, output=None):
        if output and not self.quiet:
            if self.json:
                if self.compact:
                    output = json.dumps(output, separators=(",", ":"))
                else:
                    output = json.dumps(output, indent=2)
            else:
                if isinstance(output, dict):
                    output = "\n".join([f"{k}: {v}" for k, v in output.items()])
                elif isinstance(output, list):
                    output = "\n".join(output)
            click.echo(output)
        sys.exit(exit_code)

    def list(self):
        self.exit(0, self.domain_names)

    def get_status(self):
        result = self.get(f"v4/domains/{self.domain}")
        records = self.get_dns_records(result)
        return dict(
            domain=self.domain,
            state=result["domain"]["state"],
            spf=records["SPF"]["valid"],
            dkim=records["DKIM"]["valid"],
        )

    def get_dns_records(self, result=None):
        if not result:
            result = self.get(f"v4/domains/{self.domain}")
        ret = {}
        for record in result["sending_dns_records"]:
            _type = record["record_type"]
            value = record["value"]
            name = record["name"]
            if _type == "TXT" and "v=spf" in value:
                ret["SPF"] = record
            elif _type == "TXT" and "domainkey" in name:
                ret["DKIM"] = record
            elif _type == "CNAME":
                ret["CNAME"] = record
        return ret

    def get_deployed_dns_records(self, spf=False, cname=False, dkim=False):
        records = self.cloudflare.get_zone_records(self.domain)
        ret = []
        for record in records:
            if spf and record["type"] == "TXT" and self.record_name(record) == "@" and "v=spf" in record["content"]:
                ret.append(record)
            elif dkim and record["type"] == "TXT" and self.record_name(record) == dkim:
                ret.append(record)
            elif cname and record["type"] == "CNAME" and self.record_name(record) == cname:
                ret.append(record)
        return [
            dict(
                id=r["id"],
                zone_id=r["zone_id"],
                domain=r["zone_name"],
                type=r["type"],
                name=self.record_name(r),
                value=r["content"],
            )
            for r in ret
        ]

    def record_name(self, record):
        name = record["name"]
        if name in ["@", self.domain]:
            name = "@"
        elif name.endswith("." + self.domain):
            name = name[: -1 - len(self.domain)]
        return name

    def get_smtp_credentials(self):
        response = self.get(f"v3/domains/{self.domain}/credentials")
        return [item["login"] for item in response["items"]]

    def reset_smtp_credentials(self, username="postmaster", password=None):
        self.delete(f"v3/domains/{self.domain}/credentials")
        form_data = {"login": (None, username + "@" + self.domain)}
        if password is not None:
            form_data["password"] = (None, password)
        response = self.post(f"v3/domains/{self.domain}/credentials", files=form_data)
        if "credentials" not in response:
            for username in self.get_smtp_credentials():
                return {username: password}
        return response["credentials"]

    def get_bounces(self):
        url = f"v3/{self.domain}/bounces"
        query = dict(limit=100, page="", term="")
        bounces = []
        while True:
            response = self.get(url, params=query)
            items = response["items"]
            if len(items) > 0:
                bounces.extend(items)
                query["page"] = "next"
                query["address"] = items[-1]["address"]
            else:
                break
        return bounces

    def get_events(self):
        url = f"v3/{self.domain}/events"
        bounces = []
        while True:
            response = self.get(url)
            items = response["items"]
            if len(items) > 0:
                bounces.extend(items)
                url = response["paging"]["next"]
                url = url[len(self.base_url) + 1 :]  # noqa: E203
            else:
                break
        return bounces
