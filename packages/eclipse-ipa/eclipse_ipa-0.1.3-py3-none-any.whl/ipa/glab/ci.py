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

__version__ = "0.1.0"

import logging
import os
import fnmatch
import re
import sys
from ..dash import report, run
from glob import glob

logger = logging.getLogger(__name__)


def list_files(path):
    tree = glob(path + '/**/*', recursive=True)
    files = []
    for item in tree:
        # Ignore directories
        if os.path.isdir(item):
            continue
        files.append(item)
    return files


def find_dependencies(files, patterns):
    # Attempt to find dependency files
    dependency_locations = []
    for pattern in patterns:
        regex = fnmatch.translate(pattern.strip())
        for f in files:
            if re.match(regex, os.path.basename(f)):
                dependency_locations.append(f)
    return dependency_locations


def execute():
    # Set logging
    log_level = logging.getLevelName('INFO')
    logging.basicConfig(filename='ip_analysis.log', encoding='utf-8',
                        format='%(asctime)s [%(levelname)s] %(message)s', level=log_level)

    print("Performing IP Analysis")
    logger.info("Performing IP Analysis")

    # Check for programming languages in repository
    if 'CI_PROJECT_REPOSITORY_LANGUAGES' in os.environ:
        p_langs = os.environ['CI_PROJECT_REPOSITORY_LANGUAGES']
    else:
        logger.warning("Unable to get project repository languages from environment")
        # Nothing to do, exit
        sys.exit(1)

    # Get list of files in repository
    files = list_files('.')
    logger.debug("List of repository files: " + str(files))

    # Prepare report contents
    output = []

    # Get Dash runner
    dash_config = {
        'batch_size': '500',
        'confidence_threshold': '60',
        'output_report': True,
    }
    dash_runner = run.Dash(dash_config, logger)

    # Run Eclipse Dash for dependency files of supported programming languages
    if 'go' in p_langs:
        logger.info("Analyzing any Go dependencies")
        dependency_locations = find_dependencies(files, patterns='*.sum')
        output.extend(dash_runner.dash_generic(dependency_locations))
    if 'javascript' in p_langs:
        logger.info("Analyzing any JavaScript dependencies")
        dependency_locations = find_dependencies(files, patterns='package-lock.json, yarn.lock, pnpm-lock.yaml')
        output.extend(dash_runner.dash_generic(dependency_locations))
    if 'typescript' in p_langs:
        logger.info("Analyzing any TypeScript dependencies")
        dependency_locations = find_dependencies(files, patterns='package-lock.json, yarn.lock, pnpm-lock.yaml')
        output.extend(dash_runner.dash_generic(dependency_locations))
    if 'python' in p_langs:
        logger.info("Analyzing any Python dependencies")
        dependency_locations = find_dependencies(files, patterns='requirements*.txt, pyproject.toml')
        output.extend(dash_runner.dash_python(dependency_locations))
    if 'java' in p_langs:
        logger.info("Analyzing any Java dependencies")
        dependency_locations = find_dependencies(files, patterns='pom.xml, build.gradle.kts')
        output.extend(dash_runner.dash_java(dependency_locations))
    if 'kotlin' in p_langs:
        logger.info("Analyzing any Kotlin dependencies")
        dependency_locations = find_dependencies(files, patterns='build.gradle.kts')
        output.extend(dash_runner.dash_kotlin(dependency_locations))

    # Render HTML report
    if 'CI_PROJECT_URL' in os.environ:
        base_url = os.environ['CI_PROJECT_URL']
    else:
        base_url = ""
    if 'CI_COMMIT_BRANCH' in os.environ:
        branch = os.environ['CI_COMMIT_BRANCH']
    else:
        branch = ""

    report.render(base_url, output, branch=branch, report_filename='ip_analysis.html')

    print("IP Analysis complete")
    logger.info("IP Analysis complete")

    sys.exit(0)
