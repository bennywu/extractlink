from articlelister import ArticlesLister
import re

class yeeyanLister(ArticlesLister):
	pattern = r"http://article.yeeyan.org/view/[1-9]+/[1-9]+"

class doubanLister(ArticlesLister):
	pattern = r"http://book.douban.com/subject/[1-9]+/"

class leiphoneLister(ArticlesLister):
	pattern = r"http://www.leiphone.com/.+\.html"


def extract(url):
	import urllib
	sock = urllib.urlopen(url)
	htmlSource = sock.read()
	sock.close()
	host = urllib.splithost(url.lstrip("http:"))[0]

	parserClass = globals()["ArticlesLister"]
	lister = [k for k in globals().keys() if k.endswith("Lister")]
	for ClassName in lister:
		if re.search(ClassName.rstrip('Lister'), host):
			parserClass = globals()[ClassName]
			break
	parser = parserClass()
	parser.feed(htmlSource)
	parser.close()
	return parser.output()


if __name__ == "__main__":

	for a, u in extract("http://www.leiphone.com/"):
		print a, ':', u