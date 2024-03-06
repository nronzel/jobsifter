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
            salary_element = card.find(
                "div", attrs={"data-testid": "attribute_snippet_testid"}
            )
            company_name = card.find("span", attrs={"data-testid": "company-name"})
            location_element = card.find("div", attrs={"data-testid": "text-location"})

            if title_element:
                href = title_element.get("href")
                title = " ".join(title_element.stripped_strings)
                if excluded_keywords:
                    if self._contains_excluded_keyword(title, excluded_keywords):
                        continue
            else:
                href, title = None, None

            if company_name:
                company = company_name.text
            else:
                company = None

            if salary_element:
                salary = salary_element.text
                if "a year" in salary.lower():
                    salary = salary.replace("a year", "/ yr")
                if "an hour" in salary.lower():
                    salary = salary.replace("an hour", "/ hr")
                if salary.strip().lower() == "full-time":
                    salary = None
            else:
                salary = None
            if location_element:
                location = location_element.text
            else:
                location = None

            # ensure there is a title and link
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
            company_element = card.find("a", attrs={"data-testid": "job-card-company"})
            salary_element = card.find("div", class_="mr-8")
            location_element = card.find(
                "p", class_="text-black normal-case text-body-md"
            )

            if title_element:
                href = title_element.find("a").get("href")
                title = title_element.text
                if excluded_keywords:
                    if self._contains_excluded_keyword(title, excluded_keywords):
                        continue
            else:
                href, title = None, None

            if company_element:
                company = company_element.text
            else:
                company = None

            if salary_element:
                salary = salary_element.find(
                    "p", class_="text-black normal-case text-body-md"
                ).text
            else:
                salary = None

            if location_element:
                location = location_element.text
            else:
                location = None

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

    def _contains_excluded_keyword(self, title, excluded_keywords: List[str]) -> bool:
        """Check if the title contains any of the excluded keywords. If it does, return True."""
        for keyword in excluded_keywords:
            if keyword.lower() in title.lower():
                return True
        return False

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
