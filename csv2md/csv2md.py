from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from mdtable import MDTable
import re

RE_CSV_FILE_INCLUDE = r'{@csv "([^\s"]+\.csv)"}'

class Cvs2MdProcessor(Preprocessor):
	def run (self, lines = []):
		new_lines = []
		for line in lines:
			match = re.search(RE_CSV_FILE_INCLUDE, line)
			if match:
				""" Do something """
				print(match)
		return new_lines

class Csv2MdExtension(Extension):
	def __init__(self, *args, **kwargs):

		self.config = {}

		super().__init__(*args, **kwargs)
	
	def extendMarkdown(self, md):
		md.registerExtension(self)
		

def makeExtension(*args, **kwargs):
	return Csv2MdExtension(*args, **kwargs)