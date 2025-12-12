"""Core module for syncing Keycloak teams with SSSD."""

import re
import subprocess
from shutil import copyfile
from textwrap import dedent
from typing import Iterable

from vantage_agent.logger import logger
from vantage_agent.settings import SETTINGS
from vantage_agent.vantage_api_client import AsyncBackendClient


def create_backup(file_path: str):
    """Create a backup of the given file."""
    bkp_name = str(file_path).split("/").pop()
    backup_path = f"{SETTINGS.CACHE_DIR}/{bkp_name}.bkp"
    copyfile(file_path, backup_path)
    logger.info(f"Backup of {bkp_name} created at {backup_path}")


def _extract_org_id_from_filter(filter_value: str) -> str | None:
    """Extract the org_id from an ldap_access_filter value."""
    match = re.search(r"ou=([^,]+),ou=organizations", filter_value)
    if match:
        return match.group(1)
    return None


def _build_ldap_filter(org_id: str, team_names: Iterable[str]) -> str:
    """Build the ldap_access_filter value, always keeping slurm-users present."""
    slurm_group_filter = (
        f"(memberOf=cn=slurm-users,ou=Groups,ou={org_id},ou=organizations,dc=vantagecompute,dc=ai)"
    )
    team_filters = [
        f"(memberOf=cn={team},ou=Teams,ou={org_id},ou=organizations,dc=vantagecompute,dc=ai)"
        for team in sorted({name for name in team_names if name})
    ]
    return f"(|{slurm_group_filter}{''.join(team_filters)})"


def _resolve_org_id(teams: list[dict], sssd_lines: list[str]) -> str | None:
    """Pick the organization id from teams response or the existing SSSD filter."""
    for team in teams:
        org_id = team.get("organization")
        if org_id:
            return org_id

    for line in sssd_lines:
        if line.strip().startswith("ldap_access_filter"):
            _, _, filter_value = line.partition("=")
            org_id = _extract_org_id_from_filter(filter_value)
            if org_id:
                return org_id
    return None


def update_sssd_access_filter(org_id: str, team_names: list[str], sssd_lines: list[str]) -> bool:
    """Update ldap_access_filter in the sssd.conf file. Returns True if the file was changed."""
    create_backup(SETTINGS.SSSD_CONF_PATH)

    new_filter_value = _build_ldap_filter(org_id, team_names)
    new_line = f"ldap_access_filter = {new_filter_value}\n"

    updated_lines = list(sssd_lines)
    for idx, line in enumerate(updated_lines):
        if line.strip().startswith("ldap_access_filter"):
            if line.strip() == new_line.strip():
                logger.info("ldap_access_filter already up to date. No changes made to sssd.conf.")
                return False
            updated_lines[idx] = new_line
            break
    else:
        updated_lines.append(new_line)

    with open(SETTINGS.SSSD_CONF_PATH, "w") as f:
        f.writelines(updated_lines)

    logger.info("Updated ldap_access_filter in %s", SETTINGS.SSSD_CONF_PATH)
    return True


async def get_cluster_teams() -> list[dict]:
    """Fetch teams associated with the current cluster."""
    query = dedent(
        """
        query($clusterId: String!) {
            teamsByCluster(clusterId: $clusterId) {
                id
                name
                organization
            }
        }
        """
    )
    body = {"query": query, "variables": {"clusterId": SETTINGS.OIDC_CLIENT_ID}}

    async with AsyncBackendClient() as backend_client:
        response = await backend_client.post("/teams/graphql", json=body)
        response.raise_for_status()
        payload = response.json()
        print(payload)

    data = payload.get("data") or {}
    # Support both camelCase and snake_case keys just in case.
    teams = data.get("teamsByCluster")
    return teams


def reload_sssd():
    """Reload the SSSD to get the new changes in the sssd.conf."""
    try:
        logger.debug("Reloading SSSD config.")
        result = subprocess.run(
            ["systemctl", "restart", "sssd"], check=True, capture_output=True, text=True
        )
        logger.info(f"SSSD config reloaded:\n{result.stdout}")
    except subprocess.CalledProcessError as e:
        logger.error(f"Error while reloading SSSD conf:\n{e.stderr}")
        raise e


async def sync_cluster_teams():
    """Sync Keycloak teams with SSSD ldap_access_filter."""
    try:
        logger.info("Syncing SSSD teams access filter.")
        teams = await get_cluster_teams()
        team_names = [team.get("name", "") for team in teams]

        with open(SETTINGS.SSSD_CONF_PATH, "r") as f:
            sssd_lines = f.readlines()

        org_id = _resolve_org_id(teams, sssd_lines)
        if not org_id:
            logger.error(
                "Unable to determine organization id from teams or existing sssd.conf. Aborting update."
            )
            return

        updated = update_sssd_access_filter(org_id=org_id, team_names=team_names, sssd_lines=sssd_lines)
        if updated:
            logger.info(f"SSSD ldap_access_filter synced with {len(set(team_names))} team(s).")
            logger.debug("Reloading SSSD config.")
            reload_sssd()

    except FileNotFoundError:
        logger.error("SSSD configuration file not found at %s", SETTINGS.SSSD_CONF_PATH)
    except Exception as exc:
        logger.error(f"Error while syncing teams to SSSD: {exc}")
