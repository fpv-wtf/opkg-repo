"""Fetch ipk files from repositories and validate them."""
import argparse
import json
import tarfile
import urllib
from github import Github
from io import BytesIO

parser = argparse.ArgumentParser(
    description="Fetch ipk's from repositories and validate them")
parser.add_argument("token", metavar="TOKEN", help="Github API token")
parser.add_argument("--config", dest="config_file", metavar="CONFIG",
                    default="./repositories.json", help="Path to config file")
parser.add_argument("--target", dest="ipk_target_dir", metavar="TARGET",
                    default="./build/packages",
                    help="Target dir for ipk downloads")
parser.add_argument("--html", dest="html_output", metavar="HTML",
                    default="./build/packages/index.html",
                    help="Target file for the HTML index file")
parser.add_argument("--template", dest="html_template", metavar="TEMPLATE",
                    default="./index.html",
                    help="Template file for HTML listing")

args = parser.parse_args()

token = args.token
config_file = args.config_file
ipk_target_dir = args.ipk_target_dir
html_output = args.html_output
html_template = args.html_template


def build_html_rows(items):
    """Build rows for the HTML display."""
    rows = ""
    for item in items:
        rows += "<tr>"
        rows += '<td><a href="%s">%s</a></td>' % (item["ipk"], item["Package"])
        rows += '<td>%s</td>' % (item["Architecture"] or '')
        rows += '<td>%s</td>' % (item["Version"] or '')
        rows += '<td>%s</td>' % (item["Description"] or '')
        rows += "</tr>"

    return rows


def convert_to_dict(content):
    """Convert the control content string to a dict."""
    content_dict = {}

    lines = content.splitlines()
    for line in lines:
        key_value = line.split(': ')
        key = key_value[0]
        value = None
        if len(key_value) > 1:
            value = key_value[1]

        content_dict[key] = value

    return content_dict


def validate_ipk(path, names):
    """Check if a given ipk has a valid control file."""
    tar = tarfile.open(path)

    members = tar.getmembers()
    for member in members:
        if member.name == "./control.tar.gz":
            content = tar.extractfile(member).read()
            control_tar = tarfile.open(fileobj=BytesIO(content))

            control_members = control_tar.getmembers()
            for control_member in control_members:
                if control_member.name == "./control":
                    content = control_tar.extractfile(control_member).read()
                    content = content.decode("utf-8")

                    content_dict = convert_to_dict(content)
                    if content_dict['Package'].startswith(tuple(names)):
                        return content_dict

    return None


def write_html_index(template_path, target_path, items):
    """Generate and write the human readable index.html file."""
    items = sorted(items, key=lambda d: d['Package'])

    file = open(html_template)
    html = file.read()
    file.close()

    rows = build_html_rows(items)
    html = html.replace("{%ROWS%}", rows)

    html_file = open(html_output, "w")
    html_file.write(html)
    html_file.close()


github = Github(token)

file = open(config_file)
json = json.load(file)
file.close()

packages = []

for repoEntry in json:
    repo = repoEntry['repo']
    names = repoEntry['names']

    repository = github.get_repo(repo)
    release = repository.get_latest_release()

    assets = release.get_assets()
    for asset in assets:
        name = asset.name
        url = asset.browser_download_url
        if name.startswith(tuple(names)) and name.endswith(".ipk"):
            print("Fetching: %s" % url)
            targetPath = "%s/%s" % (ipk_target_dir, name)
            urllib.request.urlretrieve(url, targetPath)

            control = validate_ipk(targetPath, name)
            if not control:
                print("Invalid package: %s" % url)
                print("Aborting...")
                exit(1)

            control["ipk"] = name
            packages.append(control)

write_html_index(html_template, html_output, packages)
