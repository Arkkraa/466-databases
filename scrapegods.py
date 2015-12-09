from lxml import html
import requests
import re
import sys

def scrape():
	page = requests.get('http://www.godchecker.com/pantheon/greek-mythology.php?list-gods-names')
	tree = html.fromstring(page.content)
	raw_html = tree.xpath("//a/@href")

	gods = []

	for href in raw_html:
		if "deity" in str(href) and "deity-of-the-day" not in str(href):
			deity_page = requests.get(str(href))
			deity_tree = html.fromstring(deity_page.content)
			deity_box = deity_tree.xpath("//div[@id='pant-vitalsbox']/p")
			deity = deity_tree.xpath("//h1[@class='']")
			deity = re.findall(r'[A-Z]\w+', html.tostring(deity[0]))[0]

			for p in deity_box:
				yo = re.findall(r"[A-Z]\w+", html.tostring(p))
				try:
					if "Father" in html.tostring(p):
						father = yo[yo.index("Father") + 1]
						gods.append((deity, father))
						gods.append((father, deity))
					if "Mother" in html.tostring(p):
						mother = yo[yo.index("Mother") + 1]
						gods.append((deity, mother))
						gods.append((mother, deity))
					if "Consort" in  html.tostring(p):
						consort = yo[yo.index("Consort") + 1]
						gods.append((deity, consort))
						gods.append((consort, deity))
				except IndexError:
					# this happens when the string mother father or consort 
					# is in some other piece of text within this block of html
					print "oops"

	return gods

def format_csv(gods):

	gods_csv = open('greekgods.csv', 'w')

	for g1, g2 in gods:
		gods_csv.write("\"" + str(g1) + "\"" + ',0,' + "\"" + str(g2) + "\"" +',0\n')

	gods_csv.close()

if __name__ == '__main__':
	gods = scrape()
	#sys.argv

	format_csv(gods)


