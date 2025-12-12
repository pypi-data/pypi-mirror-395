#!/usr/bin/env python
"""CLI entry point for running the full job example."""
import sys
import os
import json
import argparse
import requests
from .auth import ClientCredentials, ClientCredentialsAuth
from .clients import APIError, SchedulerClient, ManagementClient, JobSubmissionConfig


def load_creds_from_file(path: str) -> ClientCredentials:
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    try:
        return ClientCredentials(client_id=data["client_id"], client_secret=data["client_secret"])
    except KeyError as e:
        raise ValueError(f"SDK key file missing field: {e}")


def resolve_credentials(args: argparse.Namespace) -> ClientCredentials:
    # 1) explicit file flag
    if args.sdk_key:
        return load_creds_from_file(args.sdk_key)

    # 2) env var file path
    sdk_key_env = os.getenv("OPENQUANTUM_SDK_KEY")
    if sdk_key_env and os.path.exists(sdk_key_env):
        return load_creds_from_file(sdk_key_env)

    # 3) direct args
    if args.client_id and args.client_secret:
        return ClientCredentials(client_id=args.client_id, client_secret=args.client_secret)

    # 4) env direct
    env_id = os.getenv("OPENQUANTUM_CLIENT_ID")
    env_secret = os.getenv("OPENQUANTUM_CLIENT_SECRET")
    if env_id and env_secret:
        return ClientCredentials(client_id=env_id, client_secret=env_secret)

    raise SystemExit(
        "Missing credentials. Provide --sdk-key <file.json> or --client-id/--client-secret "
        "or set OPENQUANTUM_SDK_KEY or OPENQUANTUM_CLIENT_ID/OPENQUANTUM_CLIENT_SECRET."
    )


def build_arg_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="Run an example job via Open Quantum SDK")

    # --- Job Inputs (NEW/UPDATED) ---
    p.add_argument(
        "-i", "--input",
        required=True,
        help="Path to the input file (e.g., circuit.qasm)"
    )
    p.add_argument(
        "-b", "--backend",
        required=True,
        help="Backend to use (UUID or short code, e.g., 'ionq:aria-1')"
    )
    p.add_argument(
        "-c", "--subcategory",
        required=True,
        help="Job subcategory (UUID or short code, e.g., 'finance:option-pricing')"
    )
    p.add_argument(
        "-n", "--name",
        default="SDK CLI Job",
        help="Name for the job"
    )
    p.add_argument(
        "-s", "--shots",
        type=int,
        default=100,
        help="Number of shots"
    )

    # --- Auth ---
    p.add_argument("--sdk-key", help="Path to SDK key JSON containing client_id and client_secret")
    p.add_argument("--client-id", help="OAuth2 client_id (alternative to --sdk-key)")
    p.add_argument("--client-secret", help="OAuth2 client_secret (alternative to --sdk-key)")
    p.add_argument("--keycloak-base", default="https://id.openquantum.com", help="Keycloak base URL")
    p.add_argument("--realm", default="platform", help="Keycloak realm")

    # --- Resource Specifiers (NEW) ---
    p.add_argument(
        "-o", "--organization",
        help="Organization ID (UUID) to use. If omitted, auto-discovers first org."
    )

    # --- API Bases ---
    p.add_argument("--scheduler-base", default="https://scheduler.openquantum.com", help="Scheduler API base URL")
    p.add_argument("--management-base", default="https://management.openquantum.com", help="Management API base URL")

    # --- Behavior ---
    p.add_argument(
        "--auto-approve",
        action="store_true",
        help="Automatically approve the job quote without prompting (default: False). "
             "Quote will show plan names like 'Public Plan' and priorities like 'Standard Queue'."
    )
    p.add_argument(
        "--job-timeout",
        type=int,
        default=86_400,  # 1 day
        help="Timeout in seconds for job execution (default: 86400 = 1 day)"
    )
    return p


def main():
    args = build_arg_parser().parse_args()

    # Resolve creds
    creds = resolve_credentials(args)

    # Build auth provider
    auth = ClientCredentialsAuth(
        keycloak_base=args.keycloak_base,
        realm=args.realm,
        creds=creds
    )

    scheduler = SchedulerClient(base_url=args.scheduler_base, auth=auth)
    management = ManagementClient(base_url=args.management_base, auth=auth)

    try:
        print("--- Open Quantum Job Submission CLI ---")

        # Step 1: Use user-provided inputs
        print(f" > Using backend: {args.backend}")
        print(f" > Using subcategory: {args.subcategory}")
        print("---------------------------------------")

        # Step 2: Build config for high-level submission
        config = JobSubmissionConfig(
            backend_class_id=args.backend,
            name=args.name,
            job_subcategory_id=args.subcategory,
            shots=args.shots,
            configuration_data=None,  # Not supported via CLI example

            # Use 'auto' for plan/priority
            execution_plan="auto",
            queue_priority="auto",

            # Set from CLI args
            auto_approve_quote=args.auto_approve,
            job_timeout_seconds=args.job_timeout,

            # Enable verbose output for CLI
            verbose=True,
        )

        # Step 3: Submit job
        job = scheduler.submit_job(config, file_path=args.input)

        # Step 4: Print result
        print("\n--- JOB SUCCEEDED ---")
        print(f"Job ID: {job.id}")
        print(f"Final Status: {job.status}")
        print(f"Submitted At: {job.submitted_at}")
        print(f"Output URL: {job.output_data_url}")
        print("---------------------")

        if job.output_data_url:
            print("\nFetching job output...")
            try:
                output_json = scheduler.download_job_output(job.id)
                print("\n--- JOB OUTPUT (JSON) ---")
                print(json.dumps(output_json, indent=2))
                print("-------------------------")
            except Exception as e:
                print(f"Failed to download/parse output: {e}", file=sys.stderr)
        else:
            print("\nNo output_data_url available (job may have failed or produced no output).")

    except requests.exceptions.HTTPError as e:
        print(f"API error: {e.response.status_code} - {e.response.text}", file=sys.stderr)
        sys.exit(1)
    except APIError as e:
        print(f"API Error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        scheduler.close()
        management.close()


if __name__ == "__main__":
    main()
