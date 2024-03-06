"""JobGrabber takes a URL for a job board and grabs jobs with the provided keyword."""

import asyncio
import urllib.parse

from typing import Optional, List
from bs4 import BeautifulSoup as bs
from parsing.job_parser import JobParser
from playwright.async_api import async_playwright


class JobGrabber:
    """
    Class to create a job grabber object to grab job data from a given URL.
    Currently only supports grabbing job data from Indeed.com and ZipRecruiter.com.
    keyword: the job to search for
    pages: the number of pages to grab jobs from (default is 2)
    exluded_keywords: a list of keywords to exclude from the search based on the job title (optional)
    location: the location to search for jobs, default is "remote"
    """

    def __init__(
        self,
        keyword: str,
        pages: int = 2,
        exluded_keywords: Optional[List[str]] = None,
        location: str = "remote",
    ):
        if exluded_keywords is None:
            self.excluded_keywords = []
        self.excluded_keywords = exluded_keywords
        self.keyword = urllib.parse.quote_plus(keyword)
        if pages > 10:
            print("Max pages is 10, setting pages to 10.")
            self.pages = 10
        else:
            self.pages = pages
        self.parser = JobParser()
        self.all_jobs = []
        self.location = urllib.parse.quote_plus(location)

    async def grab_jobs(self) -> List[dict[str, str]]:
        """
        Grab jobs from the job boards. (Indeed & ZipRecruiter)
        """
        async with async_playwright() as p:
            browser = await p.chromium.launch()
            context = await browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
                viewport={"width": 1920, "height": 1080},
            )
            page_indeed = await context.new_page()
            page_ziprecruiter = await context.new_page()
            await asyncio.gather(
                self._grab_jobs_pages_indeed(page_indeed),
                self._grab_jobs_pages_ziprecruiter(page_ziprecruiter),
            )
            await context.close()
            await browser.close()
        return self.all_jobs

    async def _grab_jobs_pages_indeed(self, page):
        """
        Get 'self.pages' number of pages of job listings from Indeed.
        """
        # limit to a max of 10 pages.
        if self.pages > 10:
            self.pages = 10
        for i in range(self.pages):
            if i == 0:
                url = f"https://www.indeed.com/jobs?q={self.keyword}&l={self.location}"
            url = f"https://www.indeed.com/jobs?q={self.keyword}&l={self.location}&start={i}0"
            data = await self._get_page_data(page, url)
            soup = bs(data, "html.parser")
            jobs = self.parser.parse_indeed(soup, self.excluded_keywords)
            self.all_jobs.extend(jobs)

    async def _grab_jobs_pages_ziprecruiter(self, page):
        """
        Get 'self.pages' number of pages of job listings from ZipRecruiter.
        """
        base_url = "https://www.ziprecruiter.com/jobs-search?search="
        for i in range(self.pages):
            if i == 0:
                url = f"{base_url}{self.keyword}&location={self.location}&days=30"
            url = (
                f"{base_url}{self.keyword}&location={self.location}&days=30&page={i+1}"
            )
            data = await self._get_page_data(page, url)
            if data == "":
                break
            soup = bs(data, "html.parser")
            jobs = self.parser.parse_ziprecruiter(soup, self.excluded_keywords)
            self.all_jobs.extend(jobs)

    async def _get_page_data(self, page, url: str) -> str:
        """
        Get the data from a single page.
        """
        res = await page.goto(url, wait_until="domcontentloaded")
        if res.status != 200:
            print(f"Failed to load page: {url}, status: {res.status}")
            return ""
        content = await page.content()

        # close Signup popup on ZipRecruiter
        if "ziprecruiter" in url:
            await page.keyboard.press("Escape")
            await page.wait_for_timeout(200)
            await page.keyboard.press("Escape")
        return content
