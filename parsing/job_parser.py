"""Parser for job listings on Indeed and ZipRecruiter."""

from typing import List, Optional


class JobParser:
    """
    Class to parse job listings from Indeed and ZipRecruiter.
    """

    def __init__(self):
        self.jobs = []

    def parse_indeed(
        self, job_soup, excluded_keywords: Optional[List[str]] = []
    ) -> List[dict[str, str]]:
        """Parse the job listings from the soup object and return a list of jobs"""

        job_cards = job_soup.find_all("div", attrs={"data-testid": "slider_item"})

        for card in job_cards:
            title_element = card.find("a", class_="jcs-JobTitle")
            if not title_element:
                continue

            href = title_element.get("href")
            title = " ".join(title_element.stripped_strings)
            if excluded_keywords and self._contains_excluded_keyword(
                title, excluded_keywords
            ):
                continue

            salary_element = card.find(
                "div", attrs={"data-testid": "attribute_snippet_testid"}
            )
            company_name = card.find("span", attrs={"data-testid": "company-name"})
            location_element = card.find("div", attrs={"data-testid": "text-location"})

            company = company_name.text if company_name else None

            salary = None
            if salary_element:
                salary = salary_element.text
                salary = salary.replace("a year", "/ yr").replace("an hour", "/ hr")
                if salary.strip().lower() == "full_time":
                    salary = None

            location = location_element.text if location_element else None

            # add to list of jobs if there is a title and link
            if title and href:
                self.jobs.append(
                    {
                        "title": title,
                        "salary": salary,
                        "company": company,
                        "location": location,
                        "link": f"www.indeed.com{href}",
                    }
                )
        return self.jobs

    def parse_ziprecruiter(
        self, job_soup, excluded_keywords: Optional[List[str]] = []
    ) -> List[dict[str, str]]:
        """Parse the job listings from the soup object and return a list of jobs"""

        job_cards = job_soup.find_all("div", class_="flex flex-col gap-24 md:gap-36")

        for card in job_cards:
            title_element = card.find("h2", class_="font-bold")
            if not title_element or not title_element.find("a"):
                continue

            href = title_element.find("a").get("href")
            title = title_element.text.strip()
            if excluded_keywords and self._contains_excluded_keyword(
                title, excluded_keywords
            ):
                continue

            company_element = card.find("a", attrs={"data-testid": "job-card-company"})

            company = company_element.text.strip() if company_element else None

            salary_element = card.find("div", class_="mr-8")
            salary = None
            if salary_element:
                salary_text_element = salary_element.find(
                    "p", class_="text-black normal-case text-body-md"
                )
                if salary_text_element:
                    salary = salary_text_element.text.strip()

            location_element = card.find(
                "p", class_="text-black normal-case text-body-md"
            )
            location = location_element.text.strip() if location_element else None

            if title and href:
                self.jobs.append(
                    {
                        "title": title,
                        "salary": salary,
                        "company": company,
                        "location": location,
                        "link": href,
                    }
                )

        return self.jobs

    def remove_duplicates(self, jobs: List[dict[str, str]]) -> List[dict[str, str]]:
        """
        Remove duplicate jobs from the list of jobs
        Some jobs are posted multiple times and will have different links, but
        the same title, company, location, and salary. This method removes the
        duplicates.
        """
        seen = set()
        unique_jobs = []
        for job in jobs:
            job_copy = job.copy()
            job_copy.pop("link", None)

            hashable = tuple(job_copy.items())

            if hashable not in seen:
                seen.add(hashable)
                unique_jobs.append(job)
        return unique_jobs

    def _contains_excluded_keyword(self, title, excluded_keywords: List[str]) -> bool:
        """Check if the title contains any of the excluded keywords. If it does, return True."""
        for keyword in excluded_keywords:
            if keyword.lower() in title.lower():
                return True
        return False
