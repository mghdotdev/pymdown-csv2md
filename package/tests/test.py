import markdown
import os
from ..csv2md.csv2md import Csv2MdExtension

CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))

class TestMarkdown():
	def __init__(self, *args, **kwargs):

		self.md = markdown.Markdown(extensions = [ Csv2MdExtension(), 'pymdownx.extra' ], extension_configs = {})

		for subdir, dirs, files in os.walk(os.path.join(CURRENT_DIR, 'fixtures')):
			for file in files:
				if (file.endswith('.md')):
					self.md.convertFile(input = os.path.join(CURRENT_DIR, 'fixtures', file), output = os.path.join(CURRENT_DIR, 'fixtures', (file + '.html')))

# run test
test = TestMarkdown()