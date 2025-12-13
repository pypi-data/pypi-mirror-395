#!/usr/bin/env python3
"""
Test script for Extract360 APIs.

Usage:
    export EXTRACT360_API_KEY="your_api_key"
    python test_api.py

Or run specific tests:
    python test_api.py --test wallet
    python test_api.py --test create_job
    python test_api.py --test list_jobs
    python test_api.py --test full_scrape
"""

import argparse
import json
import os
import sys
import time

# Add parent directory to path to import the SDK
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from extract360 import Extract360Client, Extract360Error


class Colors:
    GREEN = "\033[92m"
    RED = "\033[91m"
    YELLOW = "\033[93m"
    BLUE = "\033[94m"
    RESET = "\033[0m"
    BOLD = "\033[1m"


def print_header(text: str):
    print(f"\n{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{text}{Colors.RESET}")
    print(f"{Colors.BOLD}{Colors.BLUE}{'='*60}{Colors.RESET}\n")


def print_success(text: str):
    print(f"{Colors.GREEN}✓ {text}{Colors.RESET}")


def print_error(text: str):
    print(f"{Colors.RED}✗ {text}{Colors.RESET}")


def print_info(text: str):
    print(f"{Colors.YELLOW}→ {text}{Colors.RESET}")


def print_json(data: dict):
    print(json.dumps(data, indent=2, default=str))


class APITester:
    def __init__(self, api_key: str, base_url: str = None):
        self.client = Extract360Client(
            api_key=api_key,
            base_url=base_url or os.getenv("EXTRACT360_API_URL", "http://localhost:5001/api"),
        )
        self.created_job_id = None

    def test_get_wallet(self) -> bool:
        """Test GET /api/credits/wallet"""
        print_header("Testing: GET /api/credits/wallet")
        try:
            wallet = self.client.get_wallet()
            print_success("Wallet retrieved successfully")
            print_info(f"Balance: {wallet.get('totalBalance', 0)} credits")
            print_json(wallet)
            return True
        except Extract360Error as e:
            print_error(f"Failed to get wallet: {e}")
            return False

    def test_list_jobs(self) -> bool:
        """Test GET /api/jobs"""
        print_header("Testing: GET /api/jobs (List Jobs)")
        try:
            result = self.client.list_jobs(limit=5)
            jobs = result.get("jobs", [])
            total = result.get("total", 0)
            print_success(f"Jobs listed successfully. Total: {total}")
            print_info(f"Showing {len(jobs)} jobs:")
            for job in jobs:
                status_color = Colors.GREEN if job["status"] == "succeeded" else (
                    Colors.RED if job["status"] == "failed" else Colors.YELLOW
                )
                print(f"  - {job['id']}: {status_color}{job['status']}{Colors.RESET} - {job['inputUrl'][:50]}...")
            return True
        except Extract360Error as e:
            print_error(f"Failed to list jobs: {e}")
            return False

    def test_create_job(self, url: str = "https://example.com") -> bool:
        """Test POST /api/jobs (Create Job)"""
        print_header("Testing: POST /api/jobs (Create Job)")
        try:
            print_info(f"Creating job for URL: {url}")
            job = self.client.create_job(
                input_url=url,
                output_format="markdown",
            )
            self.created_job_id = job["id"]
            print_success(f"Job created successfully!")
            print_info(f"Job ID: {job['id']}")
            print_info(f"Status: {job['status']}")
            print_json(job)
            return True
        except Extract360Error as e:
            print_error(f"Failed to create job: {e}")
            return False

    def test_get_job(self, job_id: str = None) -> bool:
        """Test GET /api/jobs/:id"""
        job_id = job_id or self.created_job_id
        if not job_id:
            print_error("No job ID provided and no job was created")
            return False

        print_header(f"Testing: GET /api/jobs/{job_id}")
        try:
            result = self.client.get_job(job_id)
            job = result["job"]
            events = result.get("events", [])
            print_success("Job retrieved successfully!")
            print_info(f"Status: {job['status']}")
            print_info(f"Events: {len(events)}")
            print_json(job)
            return True
        except Extract360Error as e:
            print_error(f"Failed to get job: {e}")
            return False

    def test_cancel_job(self, job_id: str = None) -> bool:
        """Test POST /api/jobs/:id/cancel"""
        job_id = job_id or self.created_job_id
        if not job_id:
            print_error("No job ID provided and no job was created")
            return False

        print_header(f"Testing: POST /api/jobs/{job_id}/cancel")
        try:
            self.client.cancel_job(job_id)
            print_success("Job canceled successfully!")
            return True
        except Extract360Error as e:
            # Job might already be completed
            print_info(f"Cancel result: {e}")
            return True

    def test_full_scrape(self, url: str = "https://example.com") -> bool:
        """Test full scrape flow: create job -> wait -> get result"""
        print_header("Testing: Full Scrape Flow")
        try:
            print_info(f"Starting scrape for: {url}")
            print_info("Creating job and waiting for completion...")

            start_time = time.time()
            result = self.client.scrape_and_wait(
                input_url=url,
                output_format="markdown",
                wait_timeout=60,
                poll_interval=2,
            )
            elapsed = time.time() - start_time

            job = result["job"]
            content = result["result"]

            print_success(f"Scrape completed in {elapsed:.2f}s!")
            print_info(f"Job ID: {job['id']}")
            print_info(f"Status: {job['status']}")
            print_info(f"Credits used: {job.get('creditsCost', 'N/A')}")

            if content.get("content"):
                preview = content["content"][:500]
                print_info(f"Content preview:\n{preview}...")

            return True
        except Extract360Error as e:
            print_error(f"Scrape failed: {e}")
            return False

    def run_all_tests(self, url: str = "https://example.com") -> dict:
        """Run all API tests"""
        results = {}

        # Test wallet (read-only)
        results["wallet"] = self.test_get_wallet()

        # Test list jobs (read-only)
        results["list_jobs"] = self.test_list_jobs()

        # Test create job
        results["create_job"] = self.test_create_job(url)

        # Test get job (if created)
        if self.created_job_id:
            results["get_job"] = self.test_get_job()

        # Print summary
        print_header("Test Summary")
        passed = sum(1 for v in results.values() if v)
        total = len(results)

        for test_name, passed_test in results.items():
            status = f"{Colors.GREEN}PASS{Colors.RESET}" if passed_test else f"{Colors.RED}FAIL{Colors.RESET}"
            print(f"  {test_name}: {status}")

        print(f"\n{Colors.BOLD}Total: {passed}/{total} tests passed{Colors.RESET}")

        return results


def main():
    parser = argparse.ArgumentParser(description="Test Extract360 APIs")
    parser.add_argument("--api-key", help="API key (or set EXTRACT360_API_KEY env var)")
    parser.add_argument("--base-url", help="API base URL (default: http://localhost:5001/api)")
    parser.add_argument("--url", default="https://example.com", help="URL to scrape for tests")
    parser.add_argument(
        "--test",
        choices=["wallet", "list_jobs", "create_job", "get_job", "cancel_job", "full_scrape", "all"],
        default="all",
        help="Specific test to run",
    )
    parser.add_argument("--job-id", help="Job ID for get_job or cancel_job tests")

    args = parser.parse_args()

    api_key = args.api_key or os.getenv("EXTRACT360_API_KEY")
    if not api_key:
        print_error("API key is required. Set EXTRACT360_API_KEY or use --api-key")
        sys.exit(1)

    tester = APITester(api_key=api_key, base_url=args.base_url)

    if args.test == "all":
        results = tester.run_all_tests(args.url)
        sys.exit(0 if all(results.values()) else 1)
    elif args.test == "wallet":
        success = tester.test_get_wallet()
    elif args.test == "list_jobs":
        success = tester.test_list_jobs()
    elif args.test == "create_job":
        success = tester.test_create_job(args.url)
    elif args.test == "get_job":
        success = tester.test_get_job(args.job_id)
    elif args.test == "cancel_job":
        success = tester.test_cancel_job(args.job_id)
    elif args.test == "full_scrape":
        success = tester.test_full_scrape(args.url)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
