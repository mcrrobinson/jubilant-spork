import requests
import json
from os import path


class Download:
    def __init__(self, har: str, output: str) -> None:
        self.links = []
        self.har_location = har
        self.output_folder = output

    def open_har_file(self) -> dict:
        har_file = open(self.har_location, "r", encoding='utf-8')
        data = json.load(har_file)
        har_file.close()
        return data

    def interpret_har_file(self, json: dict):
        for entry in json["log"]["entries"]:
            if entry["_resourceType"] != "media":
                continue

            link = entry["request"]["url"]
            if link not in self.links:
                self.links.append(link)

    def download(self):
        for link in self.links:
            link = link.strip()
            print(link)
            r = requests.get(link)

            name = link.split("/")[-1]

            if 'Unit' in name:
                name = name[name.index('Unit'):]

            if '?' in name:
                name = name.split('?')[0]

            with open(path.join(self.output_folder, name), "wb") as f:
                f.write(r.content)

    def run(self):
        print("Opening har file...")
        json = self.open_har_file()

        print("Interpreting har file...")
        self.interpret_har_file(json)

        print("Downloading...")
        self.download()


HAR_FILE = "C:\\Users\\Squash\\Downloads\\learn.pimsleur.com.har"
OUTPUT_FOLDER = "C:\\Users\Squash\\jubilant-spork\\output\\Russian"
Download(HAR_FILE, OUTPUT_FOLDER).run()
