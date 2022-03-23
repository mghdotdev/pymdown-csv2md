import setuptools

def get_description():
	# Get long description.

	with open( 'README.md', 'r' ) as f:
		desc = f.read()
	return desc

def get_requirements( req ):
	# Load list of dependencies.

	install_requires = []
	with open( req ) as f:
		for line in f:
			if not line.startswith( '#' ):
				install_requires.append( line.strip() )
	return install_requires

setuptools.setup(
	name = 'pymdown-csv2md',
	version = '3.0.0',
	author = 'Max Hegler',
	author_email = 'maxghegler@gmail.com',
	description = 'A Python-Markdown extension for converting .csv file to markdown tables inline.',
	long_description = get_description(),
	long_description_content_type = 'text/markdown',
	url = 'https://github.com/mghweb/pymdown-csv2md',
	packages = setuptools.find_packages(),
	license = 'MIT License',
	classifiers = [
		'Intended Audience :: Developers',
		'Programming Language :: Python :: 3',
		'License :: OSI Approved :: MIT License',
		'Operating System :: OS Independent',
		'Topic :: Software Development :: Libraries :: Python Modules',
		'Topic :: Text Processing :: Filters',
		'Topic :: Text Processing :: Markup :: HTML'
	],
	python_requires = '>3.0',
	install_requires = get_requirements( 'requirements.txt' ),
	entry_points = {
		'markdown.extensions': [ 'csv2md = package.csv2md.csv2md:Csv2MdExtension' ]
	}
)