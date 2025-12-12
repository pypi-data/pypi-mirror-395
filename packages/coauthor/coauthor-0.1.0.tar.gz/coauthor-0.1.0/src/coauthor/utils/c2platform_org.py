from duckduckgo_search import DDGS
import requests
from bs4 import BeautifulSoup
from markdownify import markdownify as md


def search_using_ddg(search_string, max_results=5, return_docs=True):
    results = DDGS().text(search_string, max_results=max_results)
    if return_docs:
        for result in results:
            result["body"] = download_html_and_convert_to_markdown(result["href"])
            result["formatted-doc-md"] = f"{result['title']} ({result['href']}):\n{result['body']}"
    return results


def download_html_and_convert_to_markdown(url):
    """
    Downloads the HTML content from the given URL and converts it to markdown.

    Args:
        url (str): The URL of the HTML page to download.

    Returns:
        str: The converted markdown content.
    """
    try:
        print(f"url: {url}")
        response = requests.get(url)
        response.raise_for_status()  # Raises HTTPError for bad responses
        html_content = response.text

        # Create a BeautifulSoup object to parse the HTML content
        soup = BeautifulSoup(html_content, "html.parser")

        # Find the div with the class "td-content"
        td_content_div = soup.find("div", class_="td-content")

        # Extract the HTML within the specified div, if it exists
        if td_content_div is None:
            td_content_html = str(soup)
        else:
            td_content_html = str(td_content_div)

        # Convert the targeted HTML content to markdown
        markdown_content = md(td_content_html)
        return markdown_content
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"An error occurred while fetching the URL: {e}")
