"""
AOS CLI - Command-line interface for the AOS SDK.

Usage:
    aos version              Show version
    aos health               Check server health
    aos capabilities         Show runtime capabilities
    aos skills               List available skills
    aos skill <id>           Describe a skill
    aos simulate <json>      Simulate a plan
"""

import argparse
import json
import sys
import os

from . import __version__
from .client import AOSClient, AOSError


def get_client() -> AOSClient:
    """Create a client from environment variables."""
    return AOSClient(
        api_key=os.getenv("AOS_API_KEY"),
        base_url=os.getenv("AOS_BASE_URL", "http://127.0.0.1:8000")
    )


def cmd_version(args):
    """Print version."""
    print(f"aos-sdk {__version__}")


def cmd_health(args):
    """Check server health."""
    client = get_client()
    try:
        resp = client._request("GET", "/health")
        print(json.dumps(resp, indent=2))
    except AOSError as e:
        print(f"Health check failed: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_capabilities(args):
    """Show runtime capabilities."""
    client = get_client()
    try:
        caps = client.get_capabilities()
        print(json.dumps(caps, indent=2))
    except AOSError as e:
        print(f"Failed to get capabilities: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_skills(args):
    """List available skills."""
    client = get_client()
    try:
        skills = client.list_skills()
        print(json.dumps(skills, indent=2))
    except AOSError as e:
        print(f"Failed to list skills: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_skill(args):
    """Describe a skill."""
    client = get_client()
    try:
        skill = client.describe_skill(args.skill_id)
        print(json.dumps(skill, indent=2))
    except AOSError as e:
        print(f"Failed to describe skill: {e}", file=sys.stderr)
        sys.exit(1)


def cmd_simulate(args):
    """Simulate a plan."""
    client = get_client()
    try:
        plan = json.loads(args.plan_json)
        result = client.simulate(
            plan=plan,
            budget_cents=args.budget
        )
        print(json.dumps(result, indent=2))
    except json.JSONDecodeError as e:
        print(f"Invalid JSON: {e}", file=sys.stderr)
        sys.exit(1)
    except AOSError as e:
        print(f"Simulation failed: {e}", file=sys.stderr)
        sys.exit(1)


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        prog="aos",
        description="AOS SDK Command-Line Interface"
    )
    subparsers = parser.add_subparsers(dest="command", help="Commands")

    # version
    subparsers.add_parser("version", help="Show version")

    # health
    subparsers.add_parser("health", help="Check server health")

    # capabilities
    subparsers.add_parser("capabilities", help="Show runtime capabilities")

    # skills
    subparsers.add_parser("skills", help="List available skills")

    # skill <id>
    skill_parser = subparsers.add_parser("skill", help="Describe a skill")
    skill_parser.add_argument("skill_id", help="Skill ID to describe")

    # simulate <json>
    sim_parser = subparsers.add_parser("simulate", help="Simulate a plan")
    sim_parser.add_argument("plan_json", help="Plan as JSON array")
    sim_parser.add_argument(
        "--budget",
        type=int,
        default=1000,
        help="Budget in cents (default: 1000)"
    )

    args = parser.parse_args()

    if args.command == "version":
        cmd_version(args)
    elif args.command == "health":
        cmd_health(args)
    elif args.command == "capabilities":
        cmd_capabilities(args)
    elif args.command == "skills":
        cmd_skills(args)
    elif args.command == "skill":
        cmd_skill(args)
    elif args.command == "simulate":
        cmd_simulate(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
