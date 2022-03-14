from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from mdtable import MDTable
import logging
import re
import os

RE_CSV_FILE_INCLUDE = r'{@csv "([^\s"]+\.csv)"}'

logging.basicConfig()
LOGGER_NAME = 'csv2md'
log = logging.getLogger(LOGGER_NAME)

class Cvs2MdProcessor(Preprocessor):
	def __init__(self, md, config):
		super(Cvs2MdProcessor, self).__init__(md)

		# Compile regex
		self.compiled_regex = re.compile(RE_CSV_FILE_INCLUDE)

		# Set config variables
		self.base_path = config['base_path'][0]
		self.encoding = config['encoding'][0]
	
	def resolve_file_path(self, file_path):
		return os.path.normpath(os.path.join(self.base_path, os.path.expanduser(file_path)))
	
	def get_table_lines(self, file_path):
		table_lines = []
		try:
			file_path = self.resolve_file_path(file_path)
			markdown_table = MDTable(file_path)
			table = markdown_table.get_table()
			table_lines = table.split('\n')
		except Exception as e:
			log.exception('Error: Could not find file: {}'.format(file_path))
		return table_lines

	def run(self, lines = []):
		new_lines = []
		for line in lines:
			total_result = []
			offset = 0
			matches = self.compiled_regex.finditer(line)
			for match in matches:
				start_index, end_index = match.span()
				total_match = match.group(0)

				# Get table text
				result = self.get_table_lines(match.group(1))

				# Output result to total_result
				if len(result) == 0:
					result = [total_match]
				if result:
					# result has at least one element
					if total_result:
						total_result[-1] = ''.join([total_result[-1], line[offset:start_index], result[0] ])
						total_result.extend(result[1:])
					else:
						total_result = [''.join([line[offset:start_index], element]) for element in result]
				else:
					total_result.append(line[offset:start_index])
			# All replacements are done, copy the rest of the string
			if total_result:
				total_result[-1] = ''.join([total_result[-1], line[offset:]])
			else:
				total_result.append(line[offset:])
			new_lines.extend(total_result)

		return new_lines

class Csv2MdExtension(Extension):
	def __init__(self, *args, **kwargs):

		self.config = {
			'base_path': [
				'.',
				'Base path from where relative paths are calculated'
			],
			'encoding': [
				'utf-8',
				'Encoding of the files.'
			]
		}

		super().__init__(*args, **kwargs)
	
	def extendMarkdown(self, md):
		md.registerExtension(self)
		md.preprocessors.register(Cvs2MdProcessor(md, self.config), 'csv2md', 101)
		

def makeExtension(*args, **kwargs):
	return Csv2MdExtension(*args, **kwargs)