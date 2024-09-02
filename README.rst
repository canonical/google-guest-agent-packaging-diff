Goal of this project
====================

The goal is to be able to track the differences between Ubuntu packaging of the 4 guest-agents, and the upstream
packaging of said agents.

We need to be able to annotate/exclude some of these differences to that if the differences change we can report and alert.

Usage
-----

.. code-block:: bash

    python3 google_guest_agent_packaging_diff_tool.py --agent-package google-osconfig-agent

The current output is as follows:

.. code-block:: bash

    $ python3 google_guest_agent_packaging_diff_tool.py --agent-package google-guest-agent

    ############## Comparing "Build-Depends" ##############
    "Build-Depends" field in Google upstream:
     debhelper (>= 9.20160709), dh-golang (>= 1.1), golang-go
    [   [   {   'name': 'debhelper',
                'archqual': None,
                'version': ('>=', '9.20160709'),
                'arch': None,
                'restrictions': None}],
        [   {   'name': 'dh-golang',
                'archqual': None,
                'version': ('>=', '1.1'),
                'arch': None,
                'restrictions': None}],
        [   {   'name': 'golang-go',
                'archqual': None,
                'version': None,
                'arch': None,
                'restrictions': None}]]
    ------------
    "Build-Depends" field in ubuntu:
     debhelper-compat (= 12),
                   dh-golang,
                   golang-any
    [   [   {   'name': 'debhelper-compat',
                'archqual': None,
                'version': ('=', '12'),
                'arch': None,
                'restrictions': None}],
        [   {   'name': 'dh-golang',
                'archqual': None,
                'version': None,
                'arch': None,
                'restrictions': None}],
        [   {   'name': 'golang-any',
                'archqual': None,
                'version': None,
                'arch': None,
                'restrictions': None}]]

    ############## Comparing "Depends" ##############
    "Depends" field in Google upstream:
     ${misc:Depends}, google-compute-engine-oslogin (>= 1:20231003)
    "Depends" field in ubuntu:
     ${misc:Depends},
             ${shlibs:Depends},
             google-compute-engine-oslogin (>= 20231004.00-0ubuntu1)

    ############## Comparing "Breaks" ##############
    "Breaks" field not present in Google Upstream
    ------------
    "Breaks" field in ubuntu:
     gce-compute-image-packages (<< 20191115),
            python3-google-compute-engine
    [   [   {   'name': 'gce-compute-image-packages',
                'archqual': None,
                'version': ('<<', '20191115'),
                'arch': None,
                'restrictions': None}],
        [   {   'name': 'python3-google-compute-engine',
                'archqual': None,
                'version': None,
                'arch': None,
                'restrictions': None}]]

    ############## Comparing "Replaces" ##############
    "Replaces" field not present in Google Upstream
    ------------
    "Replaces" field in ubuntu:
     gce-compute-image-packages (<< 20191115)
    [   [   {   'name': 'gce-compute-image-packages',
                'archqual': None,
                'version': ('<<', '20191115'),
                'arch': None,
                'restrictions': None}]]

TODO
----

As we do more and more SRUs independently, we should:

* Create a benchmark for "acceptable" diffs
* Once we have a benchmark, `exit 1` if there are diffs beyond that and warn