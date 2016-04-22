import os
import glob
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
import markdown

class Generator:
    def __init__(self, start_dir=None, template='', source_dir='source', output_dir='output'):
        current_path = os.path.dirname(os.path.abspath(__file__))
        templates_path = 'templates'
        jinja_loader = FileSystemLoader(current_path + '/' + templates_path)

        self.start_dir = start_dir

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

    def _handle_markdown(self, file_name, source):
        file_extension = os.path.splitext(file_name)[1]
        if file_extension == '.md':
            return markdown.markdown(source)
        return source

    def build(self):
        list_of_files = self._files_with_extensions(self.extensions)
        for source in list_of_files:
            templ = self.env.get_template(self.template)
            saved_file = self._get_output_file(source)
            source_content = open(source, 'r').read()
            source_content = self._handle_markdown(source, source_content)
            saved_file.write(templ.render(source=source_content))

    def _create_dir(self, directory):
        if not os.path.isdir(directory):
            os.mkdir(directory)
            return True
        else:
            print 'directory \"' + directory + '" exists'
            return False

    def _defined_or_defaut_dir(self, default, directory):
        if (directory):
            self._create_dir(directory)
        else:
            self._create_dir(default)

    def generate(self, project_name):
        base_path = os.getcwd() + '/' + project_name + '/'
        self._create_dir(project_name)
        self._create_dir(base_path + 'templates')
        self._defined_or_defaut_dir(base_path + 'sources', base_path + self.source_dir)
        self._defined_or_defaut_dir(base_path + 'output', base_path + self.output_dir)



if __name__ == "__main__":
    generator = Generator(
        template='articles/article.html',
        source_dir='sources',
        output_dir='output'
    )
    generator.generate('project')
    generator.build()
