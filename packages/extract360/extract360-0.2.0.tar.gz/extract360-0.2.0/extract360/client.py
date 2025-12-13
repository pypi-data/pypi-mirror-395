"""
Lightweight Extract360 client for Python.

Example:
    from extract360 import Extract360Client

    client = Extract360Client(api_key="your_api_key")

    # Synchronous scrape (recommended for simple tasks)
    result = client.scrape(
        input_url="https://example.com",
        output_format="markdown",
    )
    print(result["data"]["markdown"])

    # Or use async job with polling
    data = client.scrape_and_wait(
        input_url="https://example.com",
        output_format="markdown",
    )
    print(data["result"])
"""

from __future__ import annotations

import json
import os
import time
from typing import Any, Dict, List, Optional

import requests


class Extract360Error(Exception):
    """Raised when the Extract360 API returns an error."""


class Extract360Client:
    def __init__(
        self,
        api_key: str,
        base_url: Optional[str] = None,
        session: Optional[requests.Session] = None,
        request_timeout: float = 60.0,
        wait_timeout: float = 120.0,
        poll_interval: float = 2.0,
    ) -> None:
        if not api_key:
            raise Extract360Error("api_key is required")

        env_base = os.getenv("EXTRACT360_API_URL")
        self.base_url = (base_url or env_base or "http://localhost:5001/api").rstrip("/")
        self.api_key = api_key
        self.session = session or requests.Session()
        self.request_timeout = request_timeout
        self.wait_timeout = wait_timeout
        self.poll_interval = poll_interval

    def create_job(
        self,
        input_url: str,
        output_format: str,
        *,
        custom_prompt: Optional[str] = None,
        proxy_region: Optional[str] = None,
        scrape_options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Creates a new scraping job (async - returns job ID for polling).

        Args:
            input_url: URL to scrape
            output_format: Output format (html, markdown, screenshot, custom, search)
            custom_prompt: Custom prompt for AI extraction (required for 'custom' format)
            proxy_region: Proxy region to use
            scrape_options: Advanced scraping options (crawl, actions, etc.)

        Returns:
            Job object with id, status, etc.
        """
        payload: Dict[str, Any] = {
            "inputUrl": input_url,
            "outputFormat": output_format,
        }
        if custom_prompt:
            payload["customPrompt"] = custom_prompt
        if proxy_region:
            payload["proxyRegion"] = proxy_region
        if scrape_options:
            payload["scrapeOptions"] = scrape_options

        data = self._request("POST", "/jobs", json=payload)
        return data["job"]

    def get_job(self, job_id: str) -> Dict[str, Any]:
        """Gets job details and events by ID."""
        if not job_id:
            raise Extract360Error("job_id is required")
        return self._request("GET", f"/jobs/{job_id}")

    def list_jobs(
        self,
        *,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        status: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        search: Optional[str] = None,
        api_key_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Lists jobs with optional filters.

        Args:
            limit: Maximum number of jobs to return
            offset: Number of jobs to skip
            status: Filter by status (queued, running, succeeded, failed, canceled)
            start_date: Filter by start date (ISO format)
            end_date: Filter by end date (ISO format)
            search: Search by URL
            api_key_id: Filter by API key ID

        Returns:
            Dict with 'jobs' list and 'total' count
        """
        params: Dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if status:
            params["status"] = status
        if start_date:
            params["startDate"] = start_date
        if end_date:
            params["endDate"] = end_date
        if search:
            params["search"] = search
        if api_key_id:
            params["apiKeyId"] = api_key_id
        return self._request("GET", "/jobs", params=params if params else None)

    def cancel_job(self, job_id: str) -> bool:
        """Cancels a running or queued job."""
        data = self._request("POST", f"/jobs/{job_id}/cancel")
        if not data.get("success"):
            raise Extract360Error(data.get("error") or "Failed to cancel job")
        return True

    def get_stats(self) -> Dict[str, Any]:
        """Gets job statistics for the authenticated user."""
        return self._request("GET", "/jobs/stats")

    def get_wallet(self) -> Dict[str, Any]:
        """Gets the credits wallet for the authenticated user."""
        return self._request("GET", "/credits/wallet")

    def scrape(
        self,
        *,
        input_url: str,
        output_format: str,
        custom_prompt: Optional[str] = None,
        scrape_options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Performs a synchronous scrape - waits for result and returns directly.
        This is the recommended method for simple scraping tasks.

        Args:
            input_url: URL to scrape
            output_format: Output format (html, markdown, screenshot, custom, search)
            custom_prompt: Custom prompt for AI extraction (required for 'custom' format)
            scrape_options: Advanced scraping options

        Returns:
            Dict with 'success', 'data', 'creditsCost', etc.
        """
        payload: Dict[str, Any] = {
            "inputUrl": input_url,
            "outputFormat": output_format,
        }
        if custom_prompt:
            payload["customPrompt"] = custom_prompt
        if scrape_options:
            payload["scrapeOptions"] = scrape_options

        return self._request("POST", "/scrape", json=payload)

    def search(
        self,
        *,
        q: Optional[str] = None,
        url: Optional[str] = None,
        type: Optional[str] = None,
        gl: Optional[str] = None,
        hl: Optional[str] = None,
        location: Optional[str] = None,
        tbs: Optional[str] = None,
        num: Optional[int] = None,
        page: Optional[int] = None,
        autocorrect: Optional[bool] = None,
    ) -> Dict[str, Any]:
        """
        Search Google using the Serper API.
        Costs vary by search type (1-3 credits).

        Args:
            q: Search query (required for most types)
            url: Image URL (required for lens search)
            type: Search type (search, images, videos, places, maps, reviews, news, shopping, lens, scholar, patents, autocomplete)
            gl: Country code (e.g., "br", "us")
            hl: Language code (e.g., "pt-BR", "en")
            location: Location string (e.g., "Brazil", "Sao Paulo")
            tbs: Time-based search (e.g., "qdr:d" for past day)
            num: Number of results (1-100)
            page: Page number
            autocorrect: Enable autocorrect

        Returns:
            Search results from Google
        """
        is_lens = type == "lens"
        if is_lens and not url:
            raise Extract360Error("Image URL is required for lens search")
        if not is_lens and not q:
            raise Extract360Error("Search query (q) is required")

        payload: Dict[str, Any] = {}
        if q:
            payload["q"] = q
        if url:
            payload["url"] = url
        if type:
            payload["type"] = type
        if gl:
            payload["gl"] = gl
        if hl:
            payload["hl"] = hl
        if location:
            payload["location"] = location
        if tbs:
            payload["tbs"] = tbs
        if num is not None:
            payload["num"] = num
        if page is not None:
            payload["page"] = page
        if autocorrect is not None:
            payload["autocorrect"] = autocorrect

        return self._request("POST", "/search", json=payload)

    def wait_for_job(
        self,
        job_id: str,
        *,
        timeout: Optional[float] = None,
        poll_interval: Optional[float] = None,
    ) -> Dict[str, Any]:
        """Waits for a job to complete, polling at regular intervals."""
        deadline = time.monotonic() + (timeout or self.wait_timeout)
        interval = poll_interval or self.poll_interval

        while True:
            result = self.get_job(job_id)
            job = result["job"]
            status = job.get("status")

            if status == "succeeded":
                return job

            if status in ("failed", "canceled"):
                raise Extract360Error(job.get("errorMessage") or f"Job {status}")

            if time.monotonic() > deadline:
                raise Extract360Error(f"Timed out waiting for job {job_id}")

            time.sleep(interval)

    def scrape_and_wait(
        self,
        *,
        input_url: str,
        output_format: str,
        custom_prompt: Optional[str] = None,
        proxy_region: Optional[str] = None,
        scrape_options: Optional[Dict[str, Any]] = None,
        wait_timeout: Optional[float] = None,
        poll_interval: Optional[float] = None,
    ) -> Dict[str, Any]:
        """
        Creates a job and waits for it to complete.
        Use this for async jobs that need polling.

        Args:
            input_url: URL to scrape
            output_format: Output format (html, markdown, screenshot, custom, search)
            custom_prompt: Custom prompt for AI extraction
            proxy_region: Proxy region to use
            scrape_options: Advanced scraping options
            wait_timeout: Maximum time to wait for job completion
            poll_interval: Interval between status checks

        Returns:
            Dict with 'job' and 'result' keys
        """
        job = self.create_job(
            input_url=input_url,
            output_format=output_format,
            custom_prompt=custom_prompt,
            proxy_region=proxy_region,
            scrape_options=scrape_options,
        )
        finished_job = self.wait_for_job(
            job["id"],
            timeout=wait_timeout,
            poll_interval=poll_interval,
        )
        return {"job": finished_job, "result": self._map_result(finished_job)}

    def _map_result(self, job: Dict[str, Any]) -> Dict[str, Any]:
        fmt = job.get("outputFormat")
        if fmt == "html":
            return {"format": "html", "content": job.get("resultHtml")}
        if fmt == "markdown":
            return {"format": "markdown", "content": job.get("resultMarkdown")}
        if fmt == "screenshot":
            return {"format": "screenshot", "content": job.get("resultScreenshot")}
        if fmt in ("custom", "search"):
            raw = job.get("resultCustom")
            parsed: Any = None
            if isinstance(raw, str):
                try:
                    parsed = json.loads(raw)
                except json.JSONDecodeError:
                    parsed = raw
            return {"format": fmt, "content": parsed, "raw": raw}
        return {"format": fmt or "unknown", "content": None}

    def _request(
        self,
        method: str,
        path: str,
        *,
        params: Optional[Dict[str, Any]] = None,
        json: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        url = path if path.startswith("http") else f"{self.base_url}/{path.lstrip('/')}"
        headers = {"X-API-Key": self.api_key}

        response = self.session.request(
            method,
            url,
            params=params,
            json=json,
            headers=headers,
            timeout=self.request_timeout,
        )

        try:
            data = response.json() if response.text else {}
        except ValueError:
            data = {}

        if not response.ok:
            message = None
            if isinstance(data, dict):
                message = data.get("error")
            message = message or response.reason or "Request failed"
            raise Extract360Error(f"{response.status_code}: {message}")

        return data
