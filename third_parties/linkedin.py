import os
from typing import Dict, Any
import requests
from dotenv import load_dotenv

load_dotenv()

def scrape_linkedin_profile(linkedin_profile_url: str, mock: bool = False) -> Dict[str, Any]:
    """scrape information from LinkedIn profiles,
    Manually scrape the information from the LinkedIn profile"""

    if mock:
        linkedin_profile_url: str = "https://gist.githubusercontent.com/ferponse/400dc6e96dde4fd54cafa9c91a10718d/raw/361d0b6572365c7de76b3b5f71d46d3d13ac1742/ferran-pons.json"
        response: requests.Response = requests.get(linkedin_profile_url, timeout=10)
    else:
        api_endpoint: str = "https://nubela.co/proxycurl/api/v2/linkedin"
        headers: Dict[str, str] = {'Authorization': 'Bearer ' + os.getenv("PROXYCURL_API_KEY")}
        response: requests.Response = requests.get(api_endpoint, params={"url": linkedin_profile_url}, headers=headers, timeout=10)

    data: Dict[str, Any] = response.json()

    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "", None)
        and k not in ["people_also_viewed", "certifications"]
    }

    return data

if __name__ == "__main__":
    print("Scraping LinkedIn profile...")
    result: Dict[str, Any] = scrape_linkedin_profile(linkedin_profile_url="https://linkedin.com/in/ferranponsdev/")
    print(result)
