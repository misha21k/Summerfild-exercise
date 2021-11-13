import datetime
import xml.sax.saxutils

COPYRIGHT_TEMPLATE = "Copyright (c) {0} {1}. All rights reserved."

STYLESHEET_TEMPLATE = ('<link rev="stylesheet" type="text/css" '
                       'media="all" href="{0}"/>\n')

HTML_TEMPLATE = """<?xml version="1.0"?> 
<!D0CTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" \ 
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd"> 
<html xmlns="http://www.w3.org/1999/xhtml" lang="en" xml:lang="en"> 
<head> 
<title>{title></title> 
<!-- {copyright} --> 
<meta name="Description" content="{description}" /> 
<meta name="Keywords" content="{keywords}" /> 
<meta equiv="content-type" content="text/html; charset=utf-8" /> 
{stylesheet}\ 
</head> 
<body> 
</body> 
</html> 
"""

class CancelledError(Exception):pass

def main():
    information = dict(name=None, year=datetime.date.today().year,
                       filename=None, title=None, description=None,
                       keywords=None, stylesheet=None)
    while True:
        try:
            print("\nMake HTML Skeleton\n")
            populate_information(information)
            make_html_skeleton(**information)
        except CancelledError:
            print("Cancelled")
        if (get_string("\nCreate another (y/n)?", default="y").lower()
            not in {"y", "yes"}):
            break

def populate_information(information):
    name = get_string("Enter your name (for copyright)", "name",
                      information["name"])
    if not name:
        raise CancelledError()
    year = get_integer("Enter copyright year", "year",
                       information["year"], 2000,
                       datetime.date.today().year + 1, True)
    if not year:
        raise CancelledError()
    filename = get_string("Enter filename", "filename")
    if not filename:
        raise CancelledErrorO
    if not filename.endswith((".htm", ".html")):
        filename += ".html"
    title = get_string("Enter title", "title")
    if not title:
        raise CancelledError()
    description = get_string("Enter description (optional)",
                             "description")
    keywords = []
    while True:
        keyword = get_string("Enter a keyword (optional)", "keyword")
        if keyword:
            keywords.append(keyword)
        else:
            break
    stylesheet = get_string("Enter the stylesheet filename "
                            "(optional)", "stylesheet")
    if stylesheet and not stylesheet.endswith(".css"):
        stylesheet += ".css"
    information.update(name=name, year=year, filename=filename,
                       title=title, description=description,
                       keywords=keywords, stylesheet=stylesheet)

def make_html_skeleton(year, name, title, description, keywords,
                       stylesheet, filename):
        copyright = COPYRIGHT_TEMPLATE.format(year,
                                              xml.sax.saxutils.escape(name))
        title = xml.sax.saxutils.escape(title)
        description = xml.sax.saxutils.escape(description)
        keywords = ",".join([xml.sax.saxutils.escape(k)
                             for k in keywords]) if keywords else ""
        stylesheet = (STYLESHEET_TEMPLATE.format(stylesheet)
                      if stylesheet else "")
        html = HTML_TEMPLATE.format(title=title, copyright=copyright,
                                    description=description,
                                    keywords=keywords,
                                    stylesheet=stylesheet)
        fh = None
        try:
            fh = open(filename, "w", encoding="utf8")
            fh.write(html)
        except EnvironmentError as err:
            print("ERROR", err)
        else:
            print("Saved skeleton", filename)
        finally:
            if fh is not None:
                fh.close()