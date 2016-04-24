import os
import glob

import getopt #command line arguments
import sys

import ConfigParser

from jinja2 import FileSystemLoader
from jinja2.environment import Environment
import markdown

def compile_markdown(file_name, source):
    file_extension = os.path.splitext(file_name)[1]
    if file_extension == '.md':
        return markdown.markdown(source)
    return source

def defined_or_defaut_dir(default, directory):
    if directory:
        return directory
    else:
        return default

def create_directories(*directories):
    for directory in directories:
        print directory
        if not os.path.isdir(directory):
            os.mkdir(directory)
        else:
            print 'directory \"' + directory + '" exists'

class Compiler(object):
    def __init__(self, template='', source_dir='source', output_dir='output'):
        current_path = os.path.dirname(os.path.abspath(__file__))
        templates_path = 'templates'
        jinja_loader = FileSystemLoader(current_path + '/' + templates_path)

        self.env = Environment(loader=jinja_loader)
        self.template = template
        self.source_dir = source_dir
        self.output_dir = output_dir
        self.extensions = ('*.txt', '*.md', '*.markdown', '*.html')

    def _get_output_file(self, source):
        file_name = os.path.basename(source)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        return open(self.output_dir + '/' + file_name + '.html', 'w+')

    def _files_with_extensions(self, extensions):
        list_of_files = []
        for extension in extensions:
            list_of_files.extend(glob.glob(self.source_dir + '/' + extension))
        return list_of_files

    def compile(self):
        list_of_files = self._files_with_extensions(self.extensions)
        for source in list_of_files:
            templ = self.env.get_template(self.template)
            saved_file = self._get_output_file(source)
            source_content = open(source, 'r').read()
            source_content = compile_markdown(source, source_content)
            saved_file.write(templ.render(source=source_content))

class Generator(object):
    def __init__(self, source_dir, output_dir):
        self.source_dir = source_dir
        self.output_dir = output_dir

    def create_config(self, base_directory):
        config = ConfigParser.RawConfigParser()
        config.add_section('directories')
        config.set('directories', 'source_directory', self.source_dir)
        config.set('directories', 'output_directory', self.output_dir)
        with open(base_directory + 'config.cfg', 'wb') as configfile:
            config.write(configfile)


    def generate(self, project_name):
        base_path = os.getcwd() + '/' + project_name + '/'
        template_dir = base_path + 'templates'
        source_dir = defined_or_defaut_dir(base_path + 'sources', base_path + self.source_dir)
        output_dir = defined_or_defaut_dir(base_path + 'output', base_path + self.output_dir)
        create_directories(project_name, template_dir, source_dir, output_dir)
        self.create_config(base_path)

def main_generate(argv):
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




if __name__ == "__main__":
    Command = sys.argv[1].lower()
    if Command == 'generate':
        main_generate(sys.argv[2:])
    else:
        print 'need to specify "generate" as the first parameter'
    # main(sys.argv[1:])
