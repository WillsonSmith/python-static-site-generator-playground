"""
static site generator
"""

import os
import glob

import getopt #command line arguments
import sys

import ConfigParser

from jinja2 import FileSystemLoader
from jinja2.environment import Environment
import markdown

def compile_markdown(file_name, source):
    """
    takes a file and checks if it is a markdown file, compiles markdown if it is
    """
    file_extension = os.path.splitext(file_name)[1]
    if  file_extension in ('.md', '.markdown'):
        return markdown.markdown(source)
    return source

def defined_or_defaut_dir(default, directory):
    """
    if given a directory it will return that directory, otherwise it returns the default
    """
    if directory:
        return directory
    else:
        return default

def create_directories(*directories):
    """
    accepts as many directories as you give it
    checks if each directory exists, if it does not exist it creates the directory
    """
    for directory in directories:
        if not os.path.isdir(directory):
            os.mkdir(directory)
        else:
            print 'directory \"' + directory + '" exists'


def build(template='', source_dir='source', output_dir='output'):
    """
    handles compiling sources to pages
    """
    print(os.getcwd())
    current_path = os.path.dirname(os.path.abspath(__file__))
    jinja_loader = FileSystemLoader(current_path + '/templates')
    env = Environment(loader=jinja_loader)
    extensions = ('*.txt', '*.md', '*.markdown', '*.html')

    def _get_output_file(source):
        """
        will create directory for the output if doesn't exist, and write your compiled html
        """
        file_name = os.path.basename(source)
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        return open(output_dir + '/' + file_name + '.html', 'w+')

    def _files_with_extensions(extensions):
        """
        will list all files in directory with the given extensions
        """
        list_of_files = []
        for extension in extensions:
            list_of_files.extend(glob.glob(source_dir + '/' + extension))
        return list_of_files

    list_of_files = _files_with_extensions(extensions)
    for source in list_of_files:
        templ = env.get_template(template)
        saved_file = _get_output_file(source)
        source_content = open(source, 'r').read()
        source_content = compile_markdown(source, source_content)
        saved_file.write(templ.render(source=source_content))

class Generator(object):
    """
    this class is used to generate various parts of your static site
    """
    def __init__(self, source_dir, output_dir):
        self.source_dir = source_dir
        self.output_dir = output_dir

    def create_config(self, base_directory):
        """
        if you need a new config you can use this. By default this will be executed
        when you generate your project.
        """
        config = ConfigParser.RawConfigParser()
        config.add_section('directories')
        config.set('directories', 'source_directory', self.source_dir)
        config.set('directories', 'output_directory', self.output_dir)
        with open(base_directory + 'config.cfg', 'wb') as configfile:
            config.write(configfile)


    def generate(self, project_name):
        """
        handles the actual creation of your project folder
        """
        base_path = os.getcwd() + '/' + project_name + '/'
        template_dir = base_path + 'templates'
        source_dir = defined_or_defaut_dir(base_path + 'sources', base_path + self.source_dir)
        output_dir = defined_or_defaut_dir(base_path + 'output', base_path + self.output_dir)
        create_directories(project_name, template_dir, source_dir, output_dir)
        self.create_config(base_path)

def main_generate(argv):
    """
    the function that is called if using the command line to generate your new project
    """
    project_name = None
    source_directory = 'sources'
    output_directory = 'output'

    try:
        opts, args = getopt.getopt(argv, 'hn:i:o:', ['name=', 'sourcedir=', 'outputdir='])
    except getopt.GetoptError:
        print 'problem, try: main.py -s <sourcedir> -o <outputdir>'
        raise SystemExit
    for opt, arg in opts:
        if opt == '-h':
            print 'main.py -i <sourcedir> -o <outputdir>'
            raise SystemExit
        elif opt in ('-n', '--name'):
            project_name = arg
        elif opt in ('-s', '--sourcedir'):
            source_directory = arg
        elif opt in ('-o', '--outputdir'):
            output_directory = arg

    if not project_name:
        print 'you must specify a project name with "-n" or "--name"'
    else:
        Generator(source_directory, output_directory).generate(project_name)
        os.chdir(project_name)

def main_build(argv):
    """
    builds your project based on your configuration file and given template
    """
    #WIP - forces to use /project while building
    os.chdir('project')
    template = 'articles/article.html'
    config = ConfigParser.RawConfigParser()
    config.read('config.cfg')
    source_directory = config.get('directories', 'source_directory')
    output_directory = config.get('directories', 'output_directory')
    build(template=template, source_dir=source_directory, output_dir=output_directory)

if __name__ == "__main__":
    COMMAND = sys.argv[1].lower()
    if COMMAND == 'generate':
        main_generate(sys.argv[2:])
    elif COMMAND == 'build':
        main_build(sys.argv[2:])
    else:
        print 'need to specify "generate" as the first parameter'
