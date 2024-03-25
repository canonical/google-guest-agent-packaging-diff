from pprint import pprint
import os
import click
from debian import deb822

def parse_control_file(control_file):
    control_file_text = control_file.read()
    control_file_text_no_blank_lines = os.linesep.join([s for s in control_file_text.splitlines() if s])
    control_fileds = deb822.Deb822(control_file_text_no_blank_lines)
    return control_fileds


@click.command()
@click.option('--upstream-control-file', type=click.File(), required=True, help='Upstream control files to compare')
@click.option('--ubuntu-control-file', type=click.File(), required=True, help='Ubuntu control files to compare')
def main(upstream_control_file, ubuntu_control_file):
    # wget --output-document=ubuntu-control "https://git.launchpad.net/ubuntu/+source/google-guest-agent/tree/debian/control?h=applied/ubuntu/noble-devel"
    # wget --output-document=ubuntu-control "https://git.launchpad.net/ubuntu/+source/google-guest-agent/plain/debian/control?h=applied/ubuntu/noble-devel"
    ubuntu_control_fields = parse_control_file(ubuntu_control_file)
    upstream_control_fields = parse_control_file(upstream_control_file)
    fields_to_compare = ['Build-Depends', 'Depends', 'Recommends', 'Suggests', 'Breaks', 'Conflicts', 'Replaces', 'Provides']

    # compare the above control fields
    for field_name in [field_to_compare for field_to_compare in ubuntu_control_fields.keys() if field_to_compare in fields_to_compare]:
        print(f'{field_name}')
        if field_name in upstream_control_fields.keys():
            # print(f'\tupstream: {upstream_control_fields[field_name]}')
            relations = deb822.PkgRelation.parse_relations(upstream_control_fields[field_name])
            print(relations)
            for relation in relations:
                for relation_item in relation:
                    print(f'\tupstream: {relation_item["name"]} {relation_item["version"]}')
        else:
            print(f'\tupstream: None')
        if field_name in upstream_control_fields.keys():
            # print(f'\tubuntu: {ubuntu_control_fields[field_name]}')
            relations = deb822.PkgRelation.parse_relations(ubuntu_control_fields[field_name])
            print(relations)
            for relation in relations:
                for relation_item in relation:
                    print(f'\tubuntu: {relation_item["name"]} {relation_item["version"]}')
        else:
            print(f'\tubuntu: None')


if __name__ == '__main__':
    main()
