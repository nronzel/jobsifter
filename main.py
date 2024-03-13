"""
Description: Grab job listings from job boards. Currently supports Indeed and ZipRecruiter.
Author: nronzel
Github: github.com/nronzel/jobsift
"""

import asyncio
import argparse

import pandas as pd
from job_data.job_grabber import JobGrabber


async def main():
    arg_parser = new_arg_parser()
    args = arg_parser.parse_args()
    if not args.title:
        print("Please provide a job title to search for. See --help for more info")
        return
    if not args.pages:
        pages = 2
    else:
        pages = int(args.pages)
    if not args.location:
        location = "remote"
    else:
        location = args.location

    grabber = JobGrabber(args.title, pages, args.exclude, location)
    jobs = await grabber.grab_jobs()
    jobs = grabber.parser.remove_duplicates(jobs)
    # put jobs in pandas dataframe and export to csv
    df = pd.DataFrame(jobs)
    title = args.title.replace(" ", "-")
    df.to_csv(f"{title}.csv", index=False)

    print(f"Found {len(jobs)} jobs.")
    print(f"Exported to {title}.csv")


def new_arg_parser():
    arg_parser = argparse.ArgumentParser(description="Grab job data from job boards.")
    arg_parser.add_argument("-t", "--title", help="Job title to search for.")
    arg_parser.add_argument(
        "-e",
        "--exclude",
        nargs="+",
        help="OPTIONAL - Keywords to exclude from job title - space separated.",
    )
    arg_parser.add_argument(
        "-p",
        "--pages",
        help="OPTIONAL - Number of pages to search. Default: 2, Max: 10.",
    )
    arg_parser.add_argument(
        "-l",
        "--location",
        help="OPTIONAL - Location to search for jobs. Default: remote.",
    )
    return arg_parser


if __name__ == "__main__":
    asyncio.run(main())
