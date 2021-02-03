"""
HTML Builder
"""
import os.path
from os import path
import re
import json
from datetime import datetime
import shutil


class HtmlBuilder(object):
    def __init__(self):
        print("Hello,")
        self.json_conf = None
        self.html_tmpl_path = None
        self.html_sources_dir = None
        self.html_sources_dist = os.path.dirname(__file__) + "/output"
        self.output_path = self.html_sources_dist + "/out.html"
        self.choose_template()

    def choose_template(self):
        print("please specify template (page_type_1 or page_type_2):")
        template_path = input()

        if template_path is not None and template_path != "":
            self.html_tmpl_path = os.path.dirname(__file__) + "/htmls/" + template_path + "/template.html"
            self.html_sources_dir = os.path.dirname(__file__) + "/htmls/" + template_path + "/"
            if path.exists(self.html_tmpl_path):
                self.choose_json()
                return
            print("Could not find path specified.")
            print("Please specify like: \"page_type_1\" or \"page_type_2\"...")
            self.choose_template()
            return
        self.choose_template()

    def choose_json(self):
        print("please specify config file (page_conf_1 or page_conf_2):")
        json_input = input()
        if json_input is not None and json_input != "":
            json_path = os.path.dirname(__file__) + "/configs/" + json_input + ".json"
            if path.exists(json_path):
                json_file = open(json_path, )
                self.json_conf = json.load(json_file)
                json_file.close()

                now = datetime.now()
                directory = self.html_sources_dist+"/" + now.strftime("%d-%m-%y %H.%M.%S")
                if not os.path.exists(directory):
                    os.makedirs(directory)

                self.html_sources_dist = directory
                self.output_path = self.html_sources_dist + "/out.html"

                self.read_and_parse_html()
                return
            print("Could not find config file with path specified.")
            return
        self.choose_json()

    def read_and_parse_html(self):
        print("parsing" + self.html_tmpl_path)
        with open(self.html_tmpl_path, 'r') as file:
            data = file.read()
            # working_data = data.replace('\n', '')
            working_data = data
            matches = re.findall(r'(?<=\<\!\-\-template\-\-\>)(.*?)(?=\<\!\-\-\/template\-\-\>)', working_data,
                                 flags=re.DOTALL)
            if matches is not None and len(matches) > 0:
                print("OK. Found " + str(len(matches)) + " templates.")
                print("Parsing...")
                for pattern in matches:
                    output_str = ""
                    for item in self.json_conf:
                        match = pattern.replace("$click_path", item["click_url"]).replace("$img_path",
                                                                                          item["image_url"])
                        output_str += match
                    data = re.sub(r'(\<\!\-\-template\-\-\>)(.*?)(\<\!\-\-\/template\-\-\>)', output_str, data, count=1,
                                  flags=re.DOTALL)

                output_file = open(self.output_path, "a")
                output_file.write(data)
                output_file.close()

                self.copy_html_dependencies()
                return
            print("Not templates are found.")
            print("Rendering it as is.")
            self.copy_html_dependencies(True)

    def copy_html_dependencies(self, copy_html_as_is=False):
        src_files = os.listdir(self.html_sources_dir)
        for file_name in src_files:
            full_file_name = os.path.join(self.html_sources_dir, file_name)
            if os.path.isfile(full_file_name):
                if copy_html_as_is:
                    shutil.copy(full_file_name, self.html_sources_dist)
                elif 'template.html' not in full_file_name:
                    shutil.copy(full_file_name, self.html_sources_dist)

        print("Your output is waiting for you here:")
        print(self.output_path)


if __name__ == "__main__":
    HtmlBuilder()
