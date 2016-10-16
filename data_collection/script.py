from bs4 import BeautifulSoup
import re
import json

# load in the file
# loaded_file = open("./data/r00-2016-09-21_17-09-32.html", 'r').read()

soup = BeautifulSoup(open("./data/r00-2016-09-21_17-09-32.html"), 'html.parser')

# get the content in the script tag

script_content = soup.find('script')

# re.match('/<td>Destination\b(.*)/g', script_content.text)

boundaries = {}

grabbed_content = re.findall('<td>.*', script_content.string, re.MULTILINE)
pixel_boundary_string = re.findall('if\s\(x.*', script_content.string, re.MULTILINE)

for x in pixel_boundary_string:
    split_text = x.split()
    print "Top left (x>= ): " + split_text[3]
    print "Top right (y>= ): " + split_text[7]
    print "Bottom left (x<= ): " + split_text[11]
    print "Bottom right (y<= ): " + split_text[15]
    print "++++++++++|| ======== ||++++++++++"

for x in grabbed_content:
    replace_td = re.compile('<td>')
    x = replace_td.sub(' ', x)
    replace_b = re.compile('<b>')
    x = replace_b.sub(' ', x)
    x = x.strip()[:-11]
    if ':' not in x:
        x = "Name of Vessel: " + x
    print x

# use the regular expression to locate the line
# for line in script_content.text:
#    if re.match('/<td>Destination\b(.*)/g', line):
#        print line

# split the line into fragments


# check for json file with present date exists.

# store the contents into a json object

# export json object
