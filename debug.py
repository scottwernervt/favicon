"""

TODO: FEATURE: Check in manifest.json and browserconfig.xml for icons.

https://github.com/phillipsm/pyfav
https://github.com/phillipsm/pyfav/blob/master/pyfav/pyfav.py
https://stackoverflow.com/questions/21991044/how-to-get-high-resolution-website-logo-favicon-for-a-given-url
https://github.com/mat/besticon/

"""

import favicon

# urls = [
#     'http://www.autodesk.com',
#     'https://www.github.com',
#     'https://www.oracle.com',
#     'https://www.kicktipp.de/',
#     'https://www.bing.com',
#     'http://www.yelp.com',
#     'http://www.clearvoice.com',
#     'http://www.adeccousa.com',
#     'http://www.mindmatters.de',
#     'https://www.kogan.com',
# ]
#
# for url in urls:
#     icons = favicon.get(url)
#     print(url)
#     for icon in icons:
#         print(icon)
#     print()

icons = favicon.get('https://www.python.org/')
for icon in icons:
    print(icon)