from example import util
import json
import os
import sys
from absl import flags, app

FLAGS = flags.FLAGS

flags.DEFINE_string(name="file_path", default="", help="file path which is contained ids")


def main(argv):
    cached_url = "url.json"
    if os.path.isfile(cached_url):
        with open(cached_url, "r") as f:
            text = f.read()
            urls = json.loads(text)
    else:
        ids_file = FLAGS.file_path

        ids = []
        with open(ids_file, "r") as f:
            for index, line in enumerate(f):
                if index == 0:
                    continue
                ids.append(line.split()[0])

        urls = util.get_url(ids=ids)

        with open(cached_url, "w") as f:
            f.write(json.dumps(urls))

    print("N_ids: {}".format(len(urls.items())))

    result = {}

    for index, (key, value) in enumerate(urls.items()):
        sys.stdout.write("\rProcess: {} {}/{}".format(key, index, len(urls.items())))
        result[key] = []
        for url in value:
            uniprot_ids = util.get_uniprot_ids(url=url)
            result[key].append(uniprot_ids)

    with open("result.json", "w") as f:
        f.write(json.dumps(result))

    print("DONE")
    pass


class Virtual:
    def __init__(self):
        self.current_focus = "HIHI_HAHA"
        return

    def execute(self, func):
        func(current_focus=self.current_focus)
        return


if __name__ == "__main__":
    app.run(main)
