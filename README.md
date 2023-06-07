# Job Description Scraping
All files for a HigherEdJobs and Glassdoor Scraper that bypasses ReCAPTCHA


- Setup: Contains driver configuration, as well as helper files used in the scraping notebooks, such as adding random mouse movement to simulate a real person, and functions to interect with ReCAPTCHA

- Scrapers: This folder contains notebooks with code to scrape information from Glassdoor and Higheredjobs. It is better to use notebooks than a .py file for these, as the scrapes can take a long time and be interrupted sometimes. With the notebooks we are better able to pickup from where the interruption happened than with a .py file.
