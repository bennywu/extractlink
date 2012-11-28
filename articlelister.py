from sgmllib import SGMLParser
import re

class ArticlesLister(SGMLParser):
	"""get url and the name of the url."""
	pattern = r".+"
	def reset(self):
		self.articles = []
		self.verbatim = 0
		SGMLParser.reset(self)

	def start_a(self, attrs):
		try:
			u = dict(attrs).get("href")
		except:
			return
		else:
			if re.match(self.pattern, u):
				self.url = u
				self.verbatim += 1

	def end_a(self):
		if self.verbatim > 0:
			self.verbatim -= 1

	def handle_data(self, text):
		if self.verbatim > 0 and text.strip():
			self.articles.append((text.strip(), self.url))

	def output(self):
		return self.articles

def extract(url):
	import urllib2
	sock = urllib2.urlopen(url)
	htmlSource = sock.read()
	sock.close()
	articleslister = ArticlesLister()
	articleslister.feed(htmlSource)
	articleslister.close()
	for a, u in articleslister.output():
		print a, ':', u


if __name__ == "__main__":
	extract("http://www.yeeyan.org/")
