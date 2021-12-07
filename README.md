# Introduction
This is a web spider for [Galaxy Tool Shed](https://toolshed.g2.bx.psu.edu/).

# Requirement
Python 3.x \
selenium \
bs4 \
pandas 

# To run
Warning: 
You have to run tools_category.py at first in order to get the URLs.
- tools_category.py: get all categories of tools and the corresponding URL.
- tools.py: get all tools by category.

Tips:
 
There is a problem with the website page link, please do not simulate the button click to get the next page.
Therefore, this script changes the page number parameter of the get request to get the correct next page.