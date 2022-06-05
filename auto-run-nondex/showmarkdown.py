import html2text
import sys
import re

html_list = open(sys.argv[1], "r")
f_md = open("report_md.md", "w")
while True:
    # Get next line from file
    filename = html_list.readline().strip()
    filename = filename[filename.find("file://"):]
    filename = re.sub("file://", "", filename)
    if not filename:
        break
    with open(filename) as f:
        content = f.read()
        report = html2text.html2text(content).replace("|\n", "|")
        print(report.encode("utf-8"))
        f_md.write(report + "\n")
        f.close()
    print(filename)
