import json
import tarfile
import urllib

from github import Github
from io import BytesIO
from typing import Optional


class Fetcher:
    def __init__(self, token, config_file_path, target_dir):
        self.target_dir = target_dir
        self.target_dir_prerelease = "%s-prerelease" % (target_dir)
        self.github = Github(token)

        file = open(config_file_path)
        self.repos = json.load(file)
        file.close()

    def __convert_to_dict(self, item) -> dict:
        control_dict = {}

        lines = item.splitlines()
        for line in lines:
            key_value = line.split(': ')
            key = key_value[0]
            value = None
            if len(key_value) > 1:
                value = key_value[1]

            control_dict[key] = value

        return control_dict

    def __validate_ipk(self, path, names) -> Optional[dict]:
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

                        content_dict = self.__convert_to_dict(content)
                        if content_dict['Package'].startswith(tuple(names)):
                            return content_dict

        return None

    def __fetch_assets(self, assets, names, target_dir) -> list:
        packages = []
        for asset in assets:
            name = asset.name
            url = asset.browser_download_url
            if name.startswith(tuple(names)) and name.endswith(".ipk"):
                print("Fetching: %s" % url)
                targetPath = "%s/%s" % (target_dir, name)
                urllib.request.urlretrieve(url, targetPath)

                control = self.__validate_ipk(targetPath, name)
                if not control:
                    print("Invalid package: %s" % url)
                    print("Aborting...")
                    exit(1)

                control["ipk"] = name
                packages.append(control)

        return packages

    def fetch(self) -> dict:
        latestPackages = []
        prereleasePackages = []

        for repoEntry in self.repos:
            repo = repoEntry['repo']
            names = repoEntry['names']

            repository = self.github.get_repo(repo)
            latestRelease = repository.get_latest_release()

            assets = latestRelease.get_assets()
            packages = self.__fetch_assets(assets, names, self.target_dir)
            latestPackages = latestPackages + packages

            # Fetch pre-release if newer than latest
            releases = repository.get_releases()
            for release in releases:
                if release.prerelease:
                    if release.published_at > latestRelease.published_at:
                        assets = release.get_assets()
                        packages = self.__fetch_assets(
                            assets, names, self.target_dir_prerelease)
                        prereleasePackages = prereleasePackages + packages
                        break

        return {
            'latest': latestPackages,
            'prerelease': prereleasePackages
        }
