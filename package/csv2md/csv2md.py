from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from mdtable import MDTable
import logging
import re
import os

RE_CSV_FILE_INCLUDE = r'\[([^\]]*)\]\(([^\s\)]+\.csv)\)'

logging.basicConfig()
LOGGER_NAME = 'csv2md'
log = logging.getLogger(LOGGER_NAME)

def replace_new_lines(str):
	return str.replace('\n', ' ')

class Cvs2MdProcessor(Preprocessor):
	def __init__(self, md, config):
		super(Cvs2MdProcessor, self).__init__(md)

		# Compile regex
		self.compiled_regex = re.compile(RE_CSV_FILE_INCLUDE)

		# Create cache
		self.cache = {}

		# Set Config
		self.base_path = config['base_path'][0]
		self.padding = config['padding'][0]
		self.delimiter = config['delimiter'][0]
		self.quotechar = config['quotechar'][0]
		self.escapechar = config['escapechar'][0]
	
	def resolve_file_path(self, file_path):
		return os.path.normpath(os.path.join(self.base_path, os.path.expanduser(file_path)))
	
	def get_table_lines(self, file_path, caption):
		table_lines = []
		try:
			file_path = self.resolve_file_path(file_path)
			if file_path in self.cache:
				table_lines = self.cache[file_path]
			else:
				markdown_table = MDTable(file_path, None, self.padding, self.delimiter, self.quotechar, self.escapechar)
				table = markdown_table.get_table()
				table_lines.append('<!-- ' + caption + '-->')
				table_lines.extend(list(map(replace_new_lines, re.split('(?<=\\|)\\n', table))))
				table_lines.append('\n')
				self.cache[file_path] = table_lines
		except Exception as e:
			log.exception(' Could not find file: {}'.format(file_path))
		return table_lines

	def run(self, lines = []):
		new_lines = []
		for line in lines:
			total_result = []
			offset = 0
			matches = self.compiled_regex.finditer(line)
			for match in matches:
				total_match = match.group(0)

				# caption
				caption = match.group(1)

				# Get table text
				result = self.get_table_lines(match.group(2), caption)

				# Output result to total_result
				if len(result) == 0:
					result = [total_match]
				else:
					total_result = result

			# All replacements are done, copy the rest of the string
			if not total_result:
				total_result.append(line[offset:])
				
			new_lines.extend(total_result)

		return new_lines

class Csv2MdExtension(Extension):
	def __init__(self, *args, **kwargs):

		self.config = {
			'base_path': [
				'.',
				'Base path from where relative paths are calculated.'
			],
			'padding': [
				1,
				'Padding to use in raw formatted markdown table.'
			],
			'delimiter':  [
				",",
				'Delimiter character in CSV file.'
			],
			'quotechar': [
				'"',
				'Quote character in CSV file.'
			],
			'escapechar':  [
				"",
				'Escape character in CSV file.'
			]
		}

		super().__init__(*args, **kwargs)
	
	def extendMarkdown(self, md):
		md.registerExtension(self)
		md.preprocessors.register(Cvs2MdProcessor(md, self.config), 'csv2md', 101)
		

def makeExtension(*args, **kwargs):
	return Csv2MdExtension(*args, **kwargs)
