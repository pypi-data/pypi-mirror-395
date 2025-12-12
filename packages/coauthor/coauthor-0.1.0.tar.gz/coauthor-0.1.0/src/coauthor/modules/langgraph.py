# from typing import Annotated, Literal, TypedDict

# from langchain_core.messages import HumanMessage

# # from langchain_anthropic import ChatAnthropic
# from langchain_openai import ChatOpenAI
# from langchain_core.tools import tool
# from langgraph.checkpoint.memory import MemorySaver
# from langgraph.graph import END, START, StateGraph, MessagesState
# from langgraph.prebuilt import ToolNode
# from coauthor.utils.c2platform_org import search_using_ddg, download_html_and_convert_to_markdown


# @tool
# def search_c2platform_website(search_string: str, max_results=5):
#     """
#     Perform a DuckDuckGo search focused on the C2 Platform website.

#     This function appends "site:c2platform.org" to the provided search string to
#     restrict the results to the C2 Platform documentation site. The website is
#     available in two languages: English (default) and Dutch. Providing a search
#     string such as "What is C2 Platform" will return a specified number of
#     results, with the top result typically being "https://c2platform.org". If
#     the search string specifies a language, such as "What is C2 Platform?
#     language:nl", the top result would likely be the language-specific page,
#     such as "https://c2platform.org/nl".

#     Args:
#         search_string (str): The query string to search the C2 Platform website.
#         max_results (int, optional): Maximum number of search results to return.
#                                      Defaults to 5.

#     Returns:
#         list: A list of search results, where each result contains details
#               like 'href', the URL of the page.
#     """
#     search_string += " site:c2platform.org"
#     results = search_using_ddg(search_string, max_results)
#     return results


# @tool
# def get_c2platform_webpage(url):
#     """
#     Downloads the HTML content from the given C2 Platform URL and converts it to
#     markdown.

#     Args:
#         url (str): The URL of the HTML page to download.

#     Returns:
#         str: The converted markdown content.
#     """
#     return download_html_and_convert_to_markdown(url)


# def process_file_with_langgraph(config, logger):
#     task = config["current-task"]
#     task["response"] = process_with_openai_agent(config, logger)
#     return task["response"]
