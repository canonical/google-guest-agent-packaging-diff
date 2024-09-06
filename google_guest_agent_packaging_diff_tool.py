import os
import click
import pprint
import requests
import sys
import warnings

from dataclasses import dataclass
from debian import deb822
from debian.deb822 import Deb822

UBUNTU_CONTROL_FILENAME = "ubuntu_control.file"
GOOGLE_CONTROL_FILENAME = "gce_control.file"

FIELDS_TO_COMPARE = ["Build-Depends", "Depends", "Recommends",
                     "Suggests", "Breaks", 'Conflicts',
                     'Replaces', 'Provides']

@dataclass
class ArchiveURLS:
    ubuntu_control_url: str
    google_upstream_control_url: str

archives: dict[str, ArchiveURLS]

archive_dict = {
    "gce-compute-image-packages": [
        "https://git.launchpad.net/~ubuntu-core-dev/+git/gce-compute-image-packages/plain/debian/control?h=ubuntu/master",
        "https://raw.githubusercontent.com/GoogleCloudPlatform/guest-configs/master/packaging/debian/control"
    ],
    "google-compute-engine-oslogin": [
        "https://git.launchpad.net/~ubuntu-core-dev/+git/google-compute-engine-oslogin/plain/debian/control?h=ubuntu/master",
        "https://raw.githubusercontent.com/GoogleCloudPlatform/guest-oslogin/master/packaging/debian/control"
    ],
    "google-guest-agent": [
        "https://git.launchpad.net/~ubuntu-core-dev/+git/google-guest-agent/plain/debian/control?h=ubuntu/master",
        "https://raw.githubusercontent.com/GoogleCloudPlatform/guest-agent/main/packaging/debian/control"
    ],
    "google-osconfig-agent": [
        "https://git.launchpad.net/~ubuntu-core-dev/+git/google-osconfig-agent/plain/debian/control?h=ubuntu/master",
        "https://raw.githubusercontent.com/GoogleCloudPlatform/osconfig/master/packaging/debian/control"
    ],
} # type: archives

def clean_up() -> None:
    os.remove(UBUNTU_CONTROL_FILENAME)
    os.remove(GOOGLE_CONTROL_FILENAME)

def parse_control_file(control_file: str | os.PathLike) -> Deb822:
    with open(control_file) as fp:
        control_file_text = fp.read()

    control_file_text_no_blank_lines = os.linesep.join([s for s in control_file_text.splitlines() if s])
    control_fileds = Deb822(control_file_text_no_blank_lines)
    return control_fileds

@click.command()
@click.option('--agent-package', required=True,
              type=click.Choice(["gce-compute-image-packages",
                                        "google-compute-engine-oslogin",
                                        "google-guest-agent",
                                        "google-osconfig-agent"], case_sensitive=False),
              help='The package to inspect')

def main(agent_package: str) -> None:

    url_list = archive_dict[agent_package]

    ubuntu_req = requests.get(url_list[0])
    if ubuntu_req.ok:
        with open(UBUNTU_CONTROL_FILENAME, "w+") as fp:
            fp.write(ubuntu_req.text)
    else:
        sys.exit(f"Error {ubuntu_req.status_code} - is {url_list[0]} still available?")

    google_req = requests.get(url_list[1])
    if google_req.ok:
        with open(GOOGLE_CONTROL_FILENAME, "w+") as fp:
            fp.write(google_req.text)
    else:
        sys.exit(f"Error {google_req.status_code} - is {url_list[1]} still available?")

    ubuntu_control_fields = parse_control_file(UBUNTU_CONTROL_FILENAME)
    upstream_control_fields = parse_control_file(GOOGLE_CONTROL_FILENAME)

    # Compare the control fields
    try:
        for field_name in [field_to_compare for field_to_compare in ubuntu_control_fields.keys() if field_to_compare in FIELDS_TO_COMPARE]:
            with warnings.catch_warnings():
                warnings.filterwarnings("error")
                print(f"\n############## Comparing \"{field_name}\" ##############")
                if field_name in upstream_control_fields.keys():
                    print(f"\"{field_name}\" field in Google upstream:\n {upstream_control_fields[field_name]}")
                    try:
                        upstream_relations = deb822.PkgRelation.parse_relations(upstream_control_fields[field_name])
                        pprint.pprint(upstream_relations, indent=4, sort_dicts=False)
                        print("------------")
                    except Warning:
                        pass
                else:
                    print(f"\"{field_name}\" field not present in Google Upstream\n------------")
                if field_name in ubuntu_control_fields.keys():
                    print(f"\"{field_name}\" field in ubuntu:\n {ubuntu_control_fields[field_name]}")
                    try:
                        ubuntu_relations = deb822.PkgRelation.parse_relations(ubuntu_control_fields[field_name])
                        pprint.pprint(ubuntu_relations, indent=4, sort_dicts=False)
                    except Warning:
                        pass
                else:
                    print(f"\"{field_name}\" field not present in ubuntu")
    except Exception as err:
        sys.exit(f"The following error occurred: {err}")
    finally:
        clean_up()


if __name__ == '__main__':
    main()
