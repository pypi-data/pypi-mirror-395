"""Job search module using the JSearch API.

This module provides functionality to search for job postings using the
RapidAPI JSearch API. It allows filtering results by country, language,
employment type, requirements, and other criteria. Results can be exported
to JSON format.
"""

import requests
import json
from super_pocket.settings import click
import os
from dotenv import load_dotenv

load_dotenv()

def get_jobs(query: str,
             page: int = 1,
             num_pages: int = 10,
             country: str = "fr",
             language: str = "fr",
             date_posted: str = "month",
             employment_types: str = "FULLTIME",
             job_requirements: str = "no_experience",
             work_from_home: bool = False):
    """Retrieves job postings via the JSearch API.

    Makes a request to the RapidAPI JSearch API to search for job postings
    based on the specified criteria.

    Args:
        query: The search term for job postings.
        page: The page number to start from. Default: 1.
        num_pages: The number of pages to retrieve. Default: 10.
        country: The country code for the search (e.g., "fr", "us"). Default: "fr".
        language: The language code for results (e.g., "fr", "en"). Default: "fr".
        date_posted: The posting period ("today", "week", "month", "all").
            Default: "month".
        employment_types: The type of employment sought ("FULLTIME", "PARTTIME",
            "CONTRACTOR", "INTERN"). Default: "FULLTIME".
        job_requirements: Experience requirements ("under_3_years_experience",
            "more_than_3_years_experience", "no_experience", "no_degree").
            Default: "no_experience".
        work_from_home: If True, filters only remote work jobs.
            Default: False.

    Returns:
        dict: The JSON response data containing job postings.

    Raises:
        requests.exceptions.RequestException: If an error occurs during the HTTP request.
    """
    url = "https://jsearch.p.rapidapi.com/search"

    querystring = {"query": query,
                   "page": page,
                   "num_pages": num_pages,
                   "country": country,
                   "language": language,
                   "date_posted": date_posted,
                   "employment_types": employment_types,
                   "job_requirements":job_requirements,
                   "work_from_home":work_from_home if work_from_home else \
                    None}

    headers = {
        "x-rapidapi-key": os.environ.get("RAPIDAPI_API_KEY"),
        "x-rapidapi-host": "jsearch.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)

    return response.json()

def save_jobs_to_json(jobs: dict, filename: str):
    """Saves job postings to a JSON file.

    Writes job posting data to a JSON file formatted with 4-space
    indentation for better readability.

    Args:
        jobs: The dictionary containing job posting data.
        filename: The path to the output JSON file.

    Raises:
        IOError: If an error occurs while writing the file.
    """
    with open(filename, "w") as f:
        json.dump(jobs, f, indent=4)

@click.command(name="job-search")
@click.argument("query")
@click.option(
    "-p", "--page", type=int, default=1, help="Page number to start from"
)
@click.option("-n", "--num_pages", type=int, 
              default=10, help="Number of pages to scrape")
@click.option("-c", "--country", type=str, 
              default="fr", help="Country to search in")
@click.option("-l", "--language", type=str, 
              default="fr", help="Language to search in")
@click.option("-d", "--date_posted", type=str, 
              default="month", help="Date posted to search for")
@click.option("-t", "--employment_types", type=str, 
              default="FULLTIME", help="Employment types to search for")
@click.option("-r", "--job_requirements", type=str, 
              default="no_experience", 
              help="Job requirements to search for")
@click.option("--work_from_home", is_flag=True, 
              default=False, 
              help="Search for jobs that allow working from home")
@click.option("-o", "--output", type=str, 
              default="jobs.json", help="Output file name")
def main(query: str,
         page: int,
         num_pages: int,
         country: str = "fr",
         language: str = "fr",
         date_posted: str = "month",
         employment_types: str = "FULLTIME",
         job_requirements: str = "no_experience",
         work_from_home: bool = False,
         output: str = "jobs.json"):
    """CLI command to search for job postings and save the results.

    This command allows searching for job postings via the JSearch API
    using various filtering criteria, then saves the results to a JSON file.

    Args:
        query: The search term for job postings (required).
        page: The page number to start from.
        num_pages: The number of pages to retrieve.
        country: The country code for the search.
        language: The language code for results.
        date_posted: The posting period for jobs.
        employment_types: The type of employment sought.
        job_requirements: Experience requirements.
        work_from_home: Filter for remote work jobs.
        output: The name of the output JSON file.

    Examples:
        $ job-search "python developer" -c fr -l fr -o python_jobs.json
        $ job-search "data scientist" --work-from-home -n 5
        $ job-search "frontend engineer" -d week -t FULLTIME -r under_3_years_experience
    """
    jobs = get_jobs(query, 
                    page, 
                    num_pages, 
                    country, 
                    language, 
                    date_posted, 
                    employment_types, 
                    job_requirements, 
                    work_from_home)
    save_jobs_to_json(jobs, output)
