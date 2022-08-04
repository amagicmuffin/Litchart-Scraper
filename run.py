import main

# user config
URL = "https://www.litcharts.com/lit/how-to-read-literature-like-a-professor"
INCLUDE_ANALYSIS = True

# runs code to generate the html
main.generateOutput(mainUrl=URL, includeAnalysis=INCLUDE_ANALYSIS)
