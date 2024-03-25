Goal of this project
====================

The goal is to be able to track the differences between Ubuntu packaging of google-guest-agent and the upstream
packaging of google-guest-agent.

We need to be able to annotate/exclude some of these differences to that if the differences change we can report and alert.

Usage
-----

.. code-block:: bash

    wget --output-document=upstream-control "https://raw.githubusercontent.com/GoogleCloudPlatform/guest-agent/main/packaging/debian/control"
    wget --output-document=ubuntu-control "https://git.launchpad.net/ubuntu/+source/google-guest-agent/plain/debian/control?h=applied/ubuntu/noble-devel"
    python3 google_guest_agent_packaging_diff_tool.py --upstream-control-file ./upstream-control --ubuntu-control-file ./ubuntu-control

TODO
----

This project is very much in progress and is currently in POC stage. The following are the things that need to be done:

* Currently the differences are printed to stdout. We need to add a way to annotate the differences so that we can track them.
* Report on annotated differences as well as unannotated differences.
* Exit 1 if there are differences that are not annotated/expected.

The current output is as follow:

.. code-block:: bash

    ❯ python3 google_guest_agent_packaging_diff_tool.py --upstream-control-file ./upstream-control --ubuntu-control-file ./ubuntu-control
    Build-Depends
    [[{'name': 'debhelper', 'archqual': None, 'version': ('>=', '9.20160709'), 'arch': None, 'restrictions': None}], [{'name': 'dh-golang', 'archqual': None, 'version': ('>=', '1.1'), 'arch': None, 'restrictions': None}], [{'name': 'golang-go', 'archqual': None, 'version': None, 'arch': None, 'restrictions': None}]]
            upstream: debhelper ('>=', '9.20160709')
            upstream: dh-golang ('>=', '1.1')
            upstream: golang-go None
    [[{'name': 'debhelper-compat', 'archqual': None, 'version': ('=', '12'), 'arch': None, 'restrictions': None}], [{'name': 'dh-golang', 'archqual': None, 'version': None, 'arch': None, 'restrictions': None}], [{'name': 'golang-any', 'archqual': None, 'version': None, 'arch': None, 'restrictions': None}]]
            ubuntu: debhelper-compat ('=', '12')
            ubuntu: dh-golang None
            ubuntu: golang-any None
    Depends
    cannot parse package relationship "${misc:Depends}", returning it raw
    [[{'name': '${misc:Depends}', 'archqual': None, 'version': None, 'arch': None, 'restrictions': None}], [{'name': 'google-compute-engine-oslogin', 'archqual': None, 'version': ('>=', '1:20231003'), 'arch': None, 'restrictions': None}]]
            upstream: ${misc:Depends} None
            upstream: google-compute-engine-oslogin ('>=', '1:20231003')
    cannot parse package relationship "${misc:Depends}", returning it raw
    cannot parse package relationship "${shlibs:Depends}", returning it raw
    [[{'name': '${misc:Depends}', 'archqual': None, 'version': None, 'arch': None, 'restrictions': None}], [{'name': '${shlibs:Depends}', 'archqual': None, 'version': None, 'arch': None, 'restrictions': None}], [{'name': 'google-compute-engine-oslogin', 'archqual': None, 'version': ('>=', '20231004.00-0ubuntu1'), 'arch': None, 'restrictions': None}]]
            ubuntu: ${misc:Depends} None
            ubuntu: ${shlibs:Depends} None
            ubuntu: google-compute-engine-oslogin ('>=', '20231004.00-0ubuntu1')
    Breaks
            upstream: None
            ubuntu: None
    Replaces
            upstream: None
            ubuntu: None
