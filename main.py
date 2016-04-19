import os
import glob
from jinja2 import FileSystemLoader
from jinja2.environment import Environment
import markdown


class Generator:
    def __init__(self, template='', source_dir='source', output_dir='output'):
        current_path = os.path.dirname(os.path.abspath(__file__))
        templates_path = 'templates'
        jinja_loader = FileSystemLoader(current_path + '/' + templates_path)

        self.env = Environment(loader=jinja_loader)
        self.template = template
        self.source_dir = source_dir
        self.output_dir = output_dir

    def _output_file(self, source):
        file_name = os.path.basename(source)
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        return open(self.output_dir + '/' + file_name + '.html', 'w+')

    def build_template(self):
        sources = glob.glob(self.source_dir + '/*.md')
        for source in sources:
            templ = self.env.get_template(self.template)
            saved_file = self._output_file(source)
            source_content = open(source, 'r').read()
            source_content = markdown.markdown(source_content)
            saved_file.write(templ.render(source=source_content))

if __name__ == "__main__":
    generator = Generator(
        template='articles/article.html',
        source_dir='sources',
        output_dir='output'
    )
    generator.build_template()
