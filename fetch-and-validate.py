"""Fetch ipk files from repositories and validate them."""
import argparse
from src.fetcher import Fetcher
from src.html import HTML

parser = argparse.ArgumentParser(
    description="Fetch ipk's from repositories and validate them")
parser.add_argument("token", metavar="TOKEN", help="Github API token")
parser.add_argument("--config", dest="config_file", metavar="CONFIG",
                    default="./repositories.json", help="Path to config file")
parser.add_argument("--target", dest="ipk_target_dir", metavar="TARGET",
                    default="./build/packages",
                    help="Target dir for ipk downloads")
parser.add_argument("--html", dest="html_output_dir", metavar="HTML",
                    default="./build/packages",
                    help="Target dir for the HTML index file")
parser.add_argument("--template", dest="html_template", metavar="TEMPLATE",
                    default="./index.html",
                    help="Template file for HTML listing")

args = parser.parse_args()

token = args.token
config_file = args.config_file
ipk_target_dir = args.ipk_target_dir
html_output = "%s/index.html" % (args.html_output_dir)
html_template = args.html_template

html_output_prerelease = "%s-prerelease/index.html" % (args.html_output_dir)

# Fetch assets for stable and pre-releases
fetcher = Fetcher(token, config_file, ipk_target_dir)
packages = fetcher.fetch()

html = HTML(html_template)

# Write package index
latestPackages = sorted(packages['latest'], key=lambda d: d['Package'])
html.write(html_output, latestPackages)

# write package index for pre-releases if available
if len(packages['prerelease']) > 0:
    prereleasePackages = sorted(packages['prerelease'],
                                key=lambda d: d['Package'])
    html.write(html_output_prerelease, prereleasePackages)
