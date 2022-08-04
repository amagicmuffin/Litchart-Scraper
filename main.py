from typing import List

import requests
from bs4 import BeautifulSoup

"""
creates an html file from a litchart url that has all the summary info
only has functions in here
"""

BASE_URL = "https://www.litcharts.com"


def getChapterLinks(mainUrl: str) -> List[str]:
    """
    get a list of the links from the detailed Summary and Analysis dropdown in the top bar
    mainUrl such as "https://www.litcharts.com/lit/how-to-read-literature-like-a-professor"
    """
    ans: List[str] = []

    # get soup
    page = requests.get(mainUrl)
    print(f"{mainUrl} exit code: {page.status_code}")

    soup = BeautifulSoup(page.text, "html.parser")

    # get and return links
    dropdownMenuHTML = soup.find("div", class_="summary-sections")
    dropdownItems = dropdownMenuHTML.find_all("li")
    for i in dropdownItems:
        ans.append(BASE_URL + i.find("a").get("href"))

    return ans


def getPageHTMLOutput(pageUrl: str, includeAnalysis: bool) -> str:
    """parses a litcharts summary page and gives html output"""
    pageName: str = pageUrl.split("/")[-1]
    htmlOutput: str = f"<br><strong>..............<br>{pageName}</strong><br>"

    # get soup
    page = requests.get(pageUrl)
    print(f"{pageUrl} exit code: {page.status_code}")

    soup = BeautifulSoup(page.text, "html.parser")

    paragraphs = soup.find_all("div", class_="summary")

    for paragraphHTML in paragraphs:
        summary: str = paragraphHTML.find("div", class_="summary-text").text
        analysis: str = paragraphHTML.find("div", class_="analysis-text").text

        htmlOutput += "<strong>...</strong>"
        htmlOutput += "<p>" + summary + "</p>"
        htmlOutput += "<p>" + analysis if includeAnalysis else "" + "</p>"
        htmlOutput += "<br>"

    return htmlOutput


def generateOutput(mainUrl: str, includeAnalysis: bool = True):
    """creates an html file from a litchart url that has all the summary info"""
    innerHTMLOutput: str = ""

    chapterLinks: List[str] = getChapterLinks(mainUrl=mainUrl)

    for page in chapterLinks:
        innerHTMLOutput += getPageHTMLOutput(page, includeAnalysis=includeAnalysis)

    outputFile = "outputFull.html" if includeAnalysis else "outputNoAnalysis.html"
    with open(outputFile, "w", encoding="utf-8") as output:
        finalHTMLOutput: str = "" \
                               "<body style=\"display: flex; justify-content: center;\">" \
                               "  <div style=\"max-width: 544px\">" \
                               f"   {innerHTMLOutput}" \
                               "  </div>" \
                               "</body>"

        output.write(finalHTMLOutput)
