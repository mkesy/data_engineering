import nbformat
from nbconvert import PythonExporter
import argparse
import re

WEBSERVICE_OUTPUT_PATH = '/var/jenkins_home/workspace/data_engineering/webservice.py'
CONVERTED_OUTPUT_PATH = './converted_notebook.py'
IMPORT_ANNOTATIONS = ["#start_import", "#end_import"]
PREDICTION_ANNOTATIONS = ["#start_prediction", "#end_prediction"]
WEBSERVICE_CODE_TEMPLATE = """
{imports}
from flask import Flask
from flask import request

app = Flask(__name__)

def load_classifier(path):

    return joblib.load(path)


clf = load_classifier('classifier.pkl')

{prediction}

@app.route("/")
def hello():
    return 'This is a service for Data Science'


@app.route('/estimate')
def estimate():

    attr1 = int(request.args.get('attr1'))
    attr2 = int(request.args.get('attr2'))
    attr3 = int(request.args.get('attr3'))
    attr4 = int(request.args.get('attr4'))

    prediction = str(predict(featurize([[attr1, attr2, attr3, attr4]])))

    return prediction


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)

"""


def convert_ipynb_to_py(notebook_path, output_path):
    with open(notebook_path) as fh:
        nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT)

        exporter = PythonExporter()
        source, meta = exporter.from_notebook_node(nb)

    with open(output_path, 'w+') as fh:
        fh.writelines(source.encode('utf-8'))


def generate_rest_service_code(converted_notebook_path):
    def find_code_section(code, section_start, section_end):
        regex_string = r'(?<=' + re.escape(section_start) + r')(.|\n)+(?=' + re.escape(section_end) + r')'
        regex = re.compile(regex_string)
        found = re.search(regex, code)

        return found

    with open(converted_notebook_path, 'r') as converted_notebook:
        converted_notebook_code = converted_notebook.read()

    imports_section = find_code_section(converted_notebook_code, IMPORT_ANNOTATIONS[0], IMPORT_ANNOTATIONS[1]).group()
    prediction_section = find_code_section(converted_notebook_code, PREDICTION_ANNOTATIONS[0], PREDICTION_ANNOTATIONS[1]).group()

    webservice_code = WEBSERVICE_CODE_TEMPLATE.format(imports=imports_section, prediction=prediction_section)

    with open(WEBSERVICE_OUTPUT_PATH, 'w') as webservice:
        webservice.write(webservice_code)


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Parse Jupyter notebook path')
    parser.add_argument('path', metavar='path1', type=str, nargs=1, help='Jupyter notebook path')
    args = parser.parse_args()
    path = args.path[0]

    convert_ipynb_to_py(path, CONVERTED_OUTPUT_PATH)
    generate_rest_service_code(CONVERTED_OUTPUT_PATH)
