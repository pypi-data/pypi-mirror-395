#  Copyright (c) 2025 The Eclipse Foundation
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

import logging
import os
import tempfile
from datetime import datetime
from pathlib import Path
from shutil import copy
from urllib.request import pathname2url

from ..dash import report, run

logger = logging.getLogger(__name__)


def dash_processing(config):
    output_report = []
    dash_config = {
        'batch_size': config.get('EclipseDash', 'BatchSize', fallback='500'),
        'confidence_threshold': config.get('EclipseDash', 'ConfidenceThreshold', fallback='60'),
        'output_report': config.getboolean('EclipseDash', 'OutputReport', fallback=True),
    }

    # Set review options, when enabled
    review_opts = []
    if config.has_option('EclipseDash', 'ReviewProjectID'):
        review_opts.extend(['-review', '-token', config.get('General', 'GitlabAuthToken', fallback=None),
                            '-project', config.get('EclipseDash', 'ReviewProjectID', fallback=None)])
    dash_config['review_opts'] = review_opts

    # Get Eclipse Dash runner
    dash_runner = run.Dash(dash_config, logger)

    # Get input file
    input_file = config.get('Dependencies', 'InputFile', fallback='dependencies.txt')

    with tempfile.TemporaryDirectory() as tmpdir:
        # Copy file to Eclipse Dash working directory (supports relative paths)
        filename = os.path.basename(input_file)
        destination_filepath = os.path.join(tmpdir, filename)
        copy(input_file, destination_filepath)

        dash_output = dash_runner.dash_generic([str(destination_filepath)])
        for line in dash_output:
            line['location'] = input_file
            output_report.append(line)

    return output_report


def write_output_report(config, output_report):
    if config.getboolean('EclipseDash', 'OutputReport', fallback=True):
        # Generate output report
        report_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "-ip-report.html"
        if config.has_option('EclipseDash', 'ReviewProjectID'):
            report.render("/", output_report, report_template='review_report', report_filename=report_filename)
        else:
            report.render("/", output_report, report_template='default_report', report_filename=report_filename)

        print("IP Analysis Report written to " + os.path.join(os.getcwd(), report_filename))
        logger.info("IP Analysis Report written to " + os.path.join(os.getcwd(), report_filename))
    if config.getboolean('EclipseDash', 'OutputSummary', fallback=False):
        # Generate output summary
        summary_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "-ip-summary.csv"
        summary_contents = ""
        for e in output_report:
            if e['status'] != 'error':
                summary_contents = (summary_contents + e['name'] + ", " + e['license'] + ", " + e['status'] + ", " +
                                    e['authority'] + "\n")
        with open(summary_filename, 'w') as fp:
            fp.write(summary_contents)

        print("IP Analysis Summary written to " + os.path.join(os.getcwd(), summary_filename))
        logger.info("IP Analysis Summary written to " + os.path.join(os.getcwd(), summary_filename))


def execute(config):
    # Set logging
    log_level = logging.getLevelName(config.get('General', 'LogLevel', fallback='INFO'))
    log_file = config.get('General', 'LogFile', fallback='ip_analysis.log')
    logging.basicConfig(filename=log_file, encoding='utf-8',
                        format='%(asctime)s [%(levelname)s] %(message)s', level=log_level)

    print("Executing IP Analysis of Local Dependencies File")
    logger.info("Starting IP Analysis of Local Dependencies File")

    output_report = []
    results = dash_processing(config)

    # Input file
    input_file = config.get('Dependencies', 'InputFile', fallback='dependencies.txt')

    # Get absolute path in the filesystem
    absolute_path = str(Path(input_file).resolve())

    # Build filesystem URL
    input_file_url = f"file:///{pathname2url(absolute_path)}"

    # Add URL to the results
    for r in results:
        r['base_url'] = input_file_url

    # Add results to the output report
    output_report.extend(results)

    # Write an output report
    write_output_report(config, output_report)

    print("IP Analysis of Local Dependencies File is now complete. Goodbye!")
    logger.info("IP Analysis of Local Dependencies File is now complete. Goodbye!")
