import util
import json
import os
import sys


def run():
    cached_url = "url.json"
    if os.path.isfile(cached_url):
        with open(cached_url, "r") as f:
            text = f.read()
            urls = json.loads(text)
    else:
        ids_file = "Ind-test-From-KEGG-to-DrugBank-to-UniProt.txt"

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


if __name__ == "__main__":
    run()