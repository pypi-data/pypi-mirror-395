#  Copyright (c) 2024 The Eclipse Foundation
#
#  This program and the accompanying materials are made available under the
#  terms of the Eclipse Public License 2.0 which is available at
#  http://www.eclipse.org/legal/epl-2.0.
#
#  SPDX-License-Identifier: EPL-2.0
#
#  Contributors:
#      asgomes - Initial implementation

__version__ = "0.1.2"

import re
from datetime import date

from jinja2 import Environment, PackageLoader

from ..__init__ import __version__ as version

row_template = '''        <tr>
            <td class="bs-checkbox"></td>
'''


def render(base_url, entries, report_template="default_report", report_filename="", branch=None):
    env = Environment(loader=PackageLoader('ipa', 'templates'))
    template = env.get_template(report_template + '.jinja')

    if report_filename == "":
        report_filename = "ip-report.html"

    trows = ""
    for e in entries:
        trow = row_template

        # Local file
        if base_url == "/":
            e['location'] = ('<a href="' + e['base_url'] + '" target="_blank">' + e['location'] + '</a>')
        # Eclipse Project or GitHub/GitLab
        else:
            # Update location to URL
            if 'base_url' in e:
                base_url = e['base_url']
            if branch:
                e['location'] = ('<a href="' + base_url + '/-/blob/' + branch + e['location'][1:] +
                                 '" target="_blank">' + e['location'][2:] + '</a>')
            else:
                e['location'] = ('<a href="' + base_url + e['location'] + '" target="_blank">' +
                                 re.sub(r'/?-?/blob/.*?/', '/', e['location']) + '</a>')

        # Handle declared license (if not obtained from package repository)
        if report_template.endswith('_dl') and 'declared_license' not in e:
            e['declared_license'] = "-"
        # Set an empty license name to Unknown
        if e['license'] == "" or e['license'] == "unknown":
            e['license'] = "Unknown"
        # Update authority to URL if it's IPLab
        if e['authority'].startswith('#'):
            e['authority'] = ('<a href="https://gitlab.eclipse.org/eclipsefdn/emo-team/iplab/-/issues/' +
                              e['authority'][1:] + '" target="_blank">' + e['authority'] + '</a>')
        # Write all columns for this row
        trow = trow + "            <td>" + e['location'] + "</td>\n"
        trow = trow + "            <td>" + e['name'] + "</td>\n"
        if report_template.endswith('_dl'):
            trow = trow + "            <td>" + e['declared_license'] + "</td>\n"
        trow = trow + "            <td>" + e['license'] + "</td>\n"
        trow = trow + "            <td>" + e['status'] + "</td>\n"
        trow = trow + "            <td>" + e['authority'] + "</td>\n"
        # When automatic IP team review requests are ongoing, report them
        if report_template.startswith("review_report"):
            column = e.get('review', '')
            # Add URL if not empty
            if column != '':
                column = ('<a href="' + column + '" target="_blank">#' + re.search(r'[^/]+$', column).group(0) +
                          '</a>')
            trow = trow + "            <td>" + column + "</td>\n"
        # End row
        trow = trow + "        </tr>\n"
        trows = trows + trow

    with open(report_filename, 'w', encoding="utf-8") as fp:
        print(template.render(trows=trows, year=date.today().year, version=version), file=fp)
