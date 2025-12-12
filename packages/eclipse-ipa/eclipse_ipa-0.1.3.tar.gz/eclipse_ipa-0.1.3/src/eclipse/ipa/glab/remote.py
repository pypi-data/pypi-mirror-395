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

import logging
import os
import shutil
import sys
import tempfile
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from subprocess import PIPE, Popen
from time import sleep
from urllib.parse import urlparse
from requests import exceptions

import gitlab

from ..common import utils
from ..dash import report, run

logger = logging.getLogger(__name__)


def get_dependency_locations(gl, config, repositories):
    # Data structure
    # dict -> dict -> list
    dependency_locations = defaultdict(dict)

    # If repositories are directly retrieved for an Eclipse Project
    if repositories is not None:
        line_count = 0
        for repo in repositories:
            # From URL to ID (required by python-gitlab)
            repo = urlparse(repo).path.lstrip('/').removesuffix('.git')
            # Remove any trailing slashes
            repo = repo.rstrip('/')

            dependency_locations[repo] = {}
            line_count = line_count + 1
        print("Read " + str(line_count) + " GitLab project(s) from " + config.get('General', 'EclipseProject',
                                                                                  fallback='technology.dash'))
        logger.info("Read " + str(line_count) + " GitLab project(s) from " + config.get('General', 'EclipseProject',
                                                                                        fallback='technology.dash'))
        return dependency_locations

    # If a list of projects is given, work with that
    if config.getboolean('Projects', 'LoadFromFile', fallback=False):
        input_file = config.get('Projects', 'InputFile', fallback='gitlab-projects.txt')
        line_count = 0
        try:
            with open(input_file, 'r') as fp:
                for line in fp:
                    # Ignore commented lines
                    if not line.startswith('#'):
                        line_count = line_count + 1
                        proj_id = line.strip()
                        # Get rid of base URL, if included (required by python-gitlab)
                        proj_id = urlparse(proj_id).path.lstrip('/').removesuffix('.git')
                        # Remove any trailing slashes
                        proj_id = proj_id.rstrip('/')
                        dependency_locations[proj_id] = {}
            print("Read " + str(line_count) + " project(s) from " + input_file)
            logger.info("Read " + str(line_count) + " project(s) from " + input_file)
        except FileNotFoundError:
            utils.print_error(f"The provided projects file ({input_file}) cannot be found. Exiting...")
            logger.error(f"The provided projects file ({input_file}) cannot be found. Exiting...")
            sys.exit(1)
    # If a group ID is given, get our own list of projects from it
    elif config.has_option('Groups', 'BaseGroupID'):
        # Get rid of base URL, if included in BaseGroupID (required by python-gitlab)
        base_group_id = config.get('Groups', 'BaseGroupID')
        base_group_id = urlparse(base_group_id).path.lstrip('/')
        # Remove any trailing slashes
        base_group_id = base_group_id.rstrip('/')

        try:
            # Set base group ID to work
            base_group = gl.groups.get(base_group_id, lazy=True)
            # Get all projects in group
            projects = base_group.projects.list(include_subgroups=True, all=True, lazy=True)
        except gitlab.exceptions.GitlabAuthenticationError:
            utils.print_error("Invalid GitLab Token provided. Exiting...")
            logger.error("Invalid GitLab Token provided. Exiting...")
            sys.exit(1)
        except (gitlab.exceptions.GitlabGetError, gitlab.exceptions.GitlabListError):
            utils.print_error(f"Invalid GitLab Group was provided ({config.get('Groups', 'BaseGroupID')}). Exiting...")
            logger.error(f"Invalid GitLab Group was provided ({config.get('Groups', 'BaseGroupID')}). Exiting...")
            sys.exit(1)
        except BaseException as e:
            utils.print_error(f"GitLab connection error: {e}. Exiting...")
            logger.error(f"GitLab connection error: {e}. Exiting...")
            sys.exit(1)
        if config.getboolean('Projects', 'Save', fallback=False):
            # Write all projects to a file
            output_file = config.get('Projects', 'OutputFile', fallback='gitlab-projects.txt')
            with open(output_file, 'w') as fp:
                fp.write("#PROJ_NAME\n")
                fp.write("\n".join(proj.path_with_namespace for proj in dependency_locations.keys()))
                logger.info("Wrote " + str(len(projects)) + " project(s) to " + output_file)
            logger.info("Wrote " + str(len(projects)) + " project(s) to " + output_file)
        for proj in projects:
            dependency_locations[proj.path_with_namespace] = {}
    # Work with a single project ID
    elif config.has_option('Projects', 'SingleProjectID'):
        # Get rid of base URL, if included (required by python-gitlab)
        repo = urlparse(config.get('Projects', 'SingleProjectID')).path.lstrip('/').removesuffix('.git')
        # Remove any trailing slashes
        repo = repo.rstrip('/')
        dependency_locations[repo] = {}
    else:
        # No valid option provided, exit
        utils.print_error(f"Insufficient parameters provided. Exiting...")
        logger.error(f"Insufficient parameters provided. Exiting...")
        sys.exit(1)

    return dependency_locations


def analyze_dependencies(gl, config, dependency_locations):
    # If dependency check with Eclipse Dash is enabled, proceed
    if config.getboolean('General', 'AnalyzeDependencies', fallback=True):
        output_report = []
        proj_count = 0
        print("Handling dependency location(s) for " + str(len(dependency_locations)) + " Gitlab project(s)")
        logger.info("Handling dependency location(s) for " + str(len(dependency_locations)) + " Gitlab project(s)")
        # For all projects to be processed
        for proj in dependency_locations.keys():
            proj_count = proj_count + 1
            print("Handling Gitlab project " + str(proj_count) + "/" + str(len(dependency_locations)))
            logger.info("Handling Gitlab project " + str(proj_count) + "/" + str(len(dependency_locations)))

            # Get project details
            max_attempts = int(config.get('General', 'APIConnectionAttempts', fallback=3))
            for i in range(max_attempts):
                try:
                    p_details = gl.projects.get(proj)
                    logger.info("Project full path: " + str(p_details.path_with_namespace))
                    break
                except (exceptions.ConnectionError, gitlab.GitlabGetError) as e:
                    # Default values
                    is_retryable = False
                    error_message = ""
                    wait_time = 2 ** (i + 1)

                    if isinstance(e, exceptions.ConnectionError):
                        # Connection errors are always treated as retryable network issues
                        error_message = str(e)
                        is_retryable = True
                    elif isinstance(e, gitlab.GitlabGetError):
                        # GitlabGetErrors are only retryable if they are 5xx server errors
                        response_code = e.response_code
                        error_message = e.error_message
                        if 500 <= response_code < 600:
                            is_retryable = True

                    # Max attempts reached or not retryable (e.g. 404)
                    if i == max_attempts - 1 or not is_retryable:
                        if not is_retryable:
                            utils.print_error(f"Got {error_message} attempting to fetch project {proj}. Exiting...")
                            logger.error(f"Got {error_message} attempting to fetch project {proj}. Exiting...")
                            sys.exit(1)
                        utils.print_error(f"Got {error_message} after {max_attempts} "
                                          f"attempts to fetch project {proj}. Exiting...")
                        logger.error(f"Got {error_message} after {max_attempts} "
                                     f"attempts to fetch project {proj}. Exiting...")
                        sys.exit(1)

                    utils.print_warning(f"Got {error_message} while attempting to fetch project {proj}. "
                        f"Retrying in {wait_time} seconds (Attempt {i + 1}/{max_attempts}).")
                    logger.warning(f"Got {error_message} while attempting to fetch project {proj}. "
                        f"Retrying in {wait_time} seconds (Attempt {i + 1}/{max_attempts}).")
                    sleep(wait_time)

            # User did not provide dependencies for the project
            if len(dependency_locations[proj]) == 0:
                logger.info("No dependencies given for project. Attempting to find them.")

                # Get programming languages of the project
                p_langs = p_details.languages()
                logger.info("Project programming languages: " + str(p_langs))

                # Get a list of files in the project repository
                files = []
                try:
                    files = p_details.repository_tree(
                        ref=config.get('General', 'Branch', fallback=p_details.default_branch),
                        recursive=True, all=True)
                except gitlab.exceptions.GitlabGetError:
                    utils.print_warning(f"Unable to get repository tree for {p_details.path_with_namespace}. "
                                        f"Skipping...")
                    logger.warning(f"Unable to get repository tree for {p_details.path_with_namespace}. "
                                   f"Skipping...")
                    continue

                # Define a set to track the dependency paths that have been processed
                processed_paths = set()

                # Attempt to find dependency files for supported programming languages
                if 'Go' in p_langs and config.getboolean('Go', 'Enabled', fallback=True):
                    dependency_paths = utils.find_dependencies_gitlab(config, logger, 'Go', files,
                                                                      default_filenames='go.sum')
                    # Only add unique paths (avoid duplication among certain programming languages)
                    new_dependency_paths = dependency_paths - processed_paths
                    processed_paths.update(new_dependency_paths)
                    utils.add_gldep_locations(dependency_locations, p_details, 'Go', list(new_dependency_paths))
                if 'Java' in p_langs and config.getboolean('Java', 'Enabled', fallback=True):
                    dependency_paths = utils.find_dependencies_gitlab(config, logger, 'Java', files,
                                                                      default_filenames='pom.xml, build.gradle.kts')
                    # Only add unique paths (avoid duplication among certain programming languages)
                    new_dependency_paths = dependency_paths - processed_paths
                    processed_paths.update(new_dependency_paths)
                    utils.add_gldep_locations(dependency_locations, p_details, 'Java', list(new_dependency_paths))
                if 'JavaScript' in p_langs and config.getboolean('JavaScript', 'Enabled', fallback=True):
                    dependency_paths = utils.find_dependencies_gitlab(config, logger, 'JavaScript', files,
                                                                      default_filenames='package-lock.json, '
                                                                                        'yarn.lock, pnpm-lock.yaml')
                    # Only add unique paths (avoid duplication among certain programming languages)
                    new_dependency_paths = dependency_paths - processed_paths
                    processed_paths.update(new_dependency_paths)
                    utils.add_gldep_locations(dependency_locations, p_details, 'JavaScript', list(new_dependency_paths))
                if 'TypeScript' in p_langs and config.getboolean('TypeScript', 'Enabled', fallback=True):
                    dependency_paths = utils.find_dependencies_gitlab(config, logger, 'TypeScript', files,
                                                                      default_filenames='package-lock.json, '
                                                                                        'yarn.lock, pnpm-lock.yaml')
                    # Only add unique paths (avoid duplication among certain programming languages)
                    new_dependency_paths = dependency_paths - processed_paths
                    processed_paths.update(new_dependency_paths)
                    utils.add_gldep_locations(dependency_locations, p_details, 'TypeScript', list(new_dependency_paths))
                if 'Kotlin' in p_langs and config.getboolean('Kotlin', 'Enabled', fallback=True):
                    dependency_paths = utils.find_dependencies_gitlab(config, logger, 'Kotlin', files,
                                                                      default_filenames='build.gradle.kts')
                    # Only add unique paths (avoid duplication among certain programming languages)
                    new_dependency_paths = dependency_paths - processed_paths
                    processed_paths.update(new_dependency_paths)
                    utils.add_gldep_locations(dependency_locations, p_details, 'Kotlin', list(new_dependency_paths))
                if 'Python' in p_langs and config.getboolean('Python', 'Enabled', fallback=True):
                    dependency_paths = utils.find_dependencies_gitlab(config, logger, 'Python', files,
                                                                      default_filenames='requirements.txt, '
                                                                                        'pyproject.toml')
                    # Only add unique paths (avoid duplication among certain programming languages)
                    new_dependency_paths = dependency_paths - processed_paths
                    processed_paths.update(new_dependency_paths)
                    utils.add_gldep_locations(dependency_locations, p_details, 'Python', list(new_dependency_paths))

            # Dash Analysis
            for lang in dependency_locations[proj].keys():
                if config.getboolean(lang, 'Enabled', fallback=True):
                    print("Processing " + str(len(dependency_locations[proj][lang])) +
                          " dependency location(s) for " + lang + " in project " + p_details.path_with_namespace)
                    logger.info("Processing " + str(len(dependency_locations[proj][lang])) +
                                " dependency location(s) for " + lang + " in project " + p_details.path_with_namespace)
                    output_report.extend(dash_processing(config, p_details, dependency_locations[proj][lang], lang))

        return output_report
    return None


def dash_processing(config, project, filepaths, lang):
    effective_count = 0
    total_count = 0
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
                            '-repo', project.web_url, '-project',
                            config.get('EclipseDash', 'ReviewProjectID', fallback=None)])
    dash_config['review_opts'] = review_opts

    dash_runner = run.Dash(dash_config, logger)

    for fpath in filepaths:
        total_count = total_count + 1
        print("Processing " + lang + " dependency location " + str(total_count) + "/" + str(len(filepaths)))
        logger.info("Processing " + lang + " dependency location " + str(total_count) + "/" + str(len(filepaths)))

        # Make relative path for processing
        fpath = fpath.replace(project.path_with_namespace + "/", "")
        location = project.path_with_namespace + "/-/blob/" + config.get('General', 'Branch',
                                                                         fallback=project.default_branch) + "/" + fpath
        # Java (Maven Only)
        if lang == 'Java' and 'gradle' not in fpath:
            # Git clone repo for Maven
            with tempfile.TemporaryDirectory() as tmpdir:
                p_git = Popen([shutil.which('git'), 'clone', '-b',
                               config.get('General', 'Branch', fallback=project.default_branch), '--single-branch',
                               '--depth', '1', project.http_url_to_repo, tmpdir], stdout=PIPE, stderr=PIPE)
                stdout, stderr = p_git.communicate()
                # If errors from Git clone
                if p_git.returncode != 0:
                    logger.warning(
                        f"Error Git cloning repository for dependency file ({project.path_with_namespace}/{fpath}). "
                        f"Please see the details below:")
                    error_log = stdout.decode().splitlines()
                    error_log.extend(stderr.decode().splitlines())
                    for line in error_log:
                        if line.strip() != '':
                            logger.warning(line)
                    output_report.append(
                        utils.add_error_report(dash_config, location,
                                               "Error Git cloning repository for the dependency file"))
                    continue
                # Create dependency list with Maven
                fpath_normalized = fpath.replace(project.path_with_namespace, "").replace('/', os.sep)
                relative_path = os.path.join(tmpdir, fpath_normalized)

                dash_output = dash_runner.dash_java([str(relative_path)])
                for line in dash_output:
                    if 'error' in line['status']:
                        logger.warning(
                            f"Error running Maven for dependency file ({project.path_with_namespace}/{fpath}). "
                            f"Please see the details below:")
                        logger.warning(line['name'])
                        output_report.append(
                            utils.add_error_report(dash_config, location,
                                                   "Error running Maven for the dependency file"))
                        continue
                    else:
                        line['location'] = (project.path_with_namespace + "/-/blob/" +
                                            config.get('General', 'Branch', fallback=project.default_branch) +
                                            "/" + fpath)
                        output_report.append(line)
        # Java or Kotlin using Gradle
        elif 'gradle' in fpath:
            with tempfile.TemporaryDirectory() as tmpdir:
                # Get raw version of build.gradle.kts
                if tmpfile := get_file_gitlab(config, project, fpath, tmpdir):
                    dash_output = dash_runner.dash_java([str(tmpfile)])
                    for line in dash_output:
                        line['location'] = (project.path_with_namespace + "/-/blob/" +
                                            config.get('General', 'Branch', fallback=project.default_branch) +
                                            "/" + fpath)
                        output_report.append(line)
                else:
                    output_report.append(
                        utils.add_error_report(dash_config, location, "Error obtaining dependency file from Gitlab"))
                    continue
        # Python
        elif lang == 'Python':
            with tempfile.TemporaryDirectory() as tmpdir:
                # Get raw version of requirements.txt
                if tmpfile := get_file_gitlab(config, project, fpath, tmpdir):
                    declared_licenses = config.get('General', 'DeclaredLicenses', fallback=False)
                    dash_output = dash_runner.dash_python([str(tmpfile)],
                                                          declared_licenses=declared_licenses)
                    for line in dash_output:
                        line['location'] = (project.path_with_namespace + "/-/blob/" +
                                            config.get('General', 'Branch', fallback=project.default_branch) +
                                            "/" + fpath)
                        output_report.append(line)
                else:
                    output_report.append(
                        utils.add_error_report(dash_config, location, "Error obtaining dependency file from Gitlab"))
                    continue
        # Go, Javascript (or others directly supported)
        else:
            with tempfile.TemporaryDirectory() as tmpdir:
                # Get raw version of file
                if tmpfile := get_file_gitlab(config, project, fpath, tmpdir):
                    # Only NPM is supported for now
                    if lang == 'JavaScript' or lang == 'TypeScript':
                        declared_licenses = config.get('General', 'DeclaredLicenses', fallback=False)
                    else:
                        declared_licenses = False
                    dash_output = dash_runner.dash_generic([str(tmpfile)],
                                                           declared_licenses=declared_licenses)
                    for line in dash_output:
                        line['location'] = (project.path_with_namespace + "/-/blob/" +
                                            config.get('General', 'Branch', fallback=project.default_branch) +
                                            "/" + fpath)
                        output_report.append(line)
                else:
                    output_report.append(
                        utils.add_error_report(dash_config, location, "Error obtaining dependency file from Gitlab"))
                    continue
        effective_count += 1

    return output_report


def get_file_gitlab(config, project, fpath, tmpdir):
    max_attempts = int(config.get('General', 'APIConnectionAttempts', fallback=3))
    for i in range(max_attempts):
        try:
            wpath = Path(f'{os.path.join(tmpdir, os.path.basename(fpath))}')
            with open(wpath, 'w+b') as f:
                project.files.raw(file_path=fpath,
                                  ref=config.get('General', 'Branch', fallback=project.default_branch),
                                  streamed=True, action=f.write, timeout=30)
            return wpath
        except (exceptions.ConnectionError, gitlab.GitlabGetError) as e:
            # Default values
            is_retryable = False
            error_message = ""
            wait_time = 2 ** (i + 1)

            if isinstance(e, exceptions.ConnectionError):
                # Connection errors are always treated as retryable network issues
                error_message = str(e)
                is_retryable = True
            elif isinstance(e, gitlab.GitlabGetError):
                # GitlabGetErrors are only retryable if they are 5xx server errors
                response_code = e.response_code
                error_message = e.error_message
                if 500 <= response_code < 600:
                    is_retryable = True

            # Max attempts reached or not retryable (e.g. 404)
            if i == max_attempts - 1 or not is_retryable:
                if not is_retryable:
                    utils.print_error(f"Got {error_message} attempting to obtain file "
                                      f"({project.path_with_namespace}/{fpath}) from GitLab. Skipping...")
                    logger.error(f"Got {error_message} attempting to obtain file "
                                      f"({project.path_with_namespace}/{fpath}) from GitLab. Skipping...")
                    return None
                utils.print_error(f"Got {error_message} after {max_attempts} "
                                  f"attempts to obtain file {project.path_with_namespace}/{fpath}. Skipping...")
                logger.error(f"Got {error_message} after {max_attempts} "
                                  f"attempts to obtain file {project.path_with_namespace}/{fpath}. Skipping...")
                return None

            utils.print_warning(f"Got {error_message} while attempting to obtain file "
                                f"{project.path_with_namespace}/{fpath}. Retrying in {wait_time} seconds "
                                f"(Attempt {i + 1}/{max_attempts}).")
            logger.warning(f"Got {error_message} while attempting to obtain file "
                                f"{project.path_with_namespace}/{fpath}. Retrying in {wait_time} seconds "
                                f"(Attempt {i + 1}/{max_attempts}).")
            sleep(wait_time)
    return None


def write_output(config, dependency_locations, output_report):
    if config.getboolean('EclipseDash', 'OutputReport', fallback=True):
        base_url = config.get('General', 'GitlabURL', fallback='https://gitlab.eclipse.org') + "/"

        # Generate output report
        report_filename = datetime.now().strftime("%Y%m%d_%H%M%S") + "-ip-report.html"
        # Default report template
        report_template = 'default_report'
        if config.has_option('EclipseDash', 'ReviewProjectID'):
            report_template = 'review_report'
        if config.get('General', 'DeclaredLicenses', fallback=False):
            report_template = report_template + '_dl'
        report.render(base_url, output_report, report_template=report_template, report_filename=report_filename)

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


def execute(config, repositories=None):
    # Set logging
    log_level = logging.getLevelName(config.get('General', 'LogLevel', fallback='INFO'))
    log_file = config.get('General', 'LogFile', fallback='ip_analysis.log')
    logging.basicConfig(filename=log_file, encoding='utf-8',
                        format='%(asctime)s [%(levelname)s] %(message)s', level=log_level)

    print("Executing IP Analysis of Gitlab Projects")
    logger.info("Starting IP Analysis of Gitlab Projects")

    # Gitlab instance
    gl = gitlab.Gitlab(url=config.get('General', 'GitlabURL', fallback='https://gitlab.eclipse.org'),
                       private_token=config.get('General', 'GitlabAuthToken', fallback=None))

    # Get dependency locations
    dependency_locations = get_dependency_locations(gl, config, repositories)

    # Analyze dependencies
    output_report = analyze_dependencies(gl, config, dependency_locations)

    # Write output
    write_output(config, dependency_locations, output_report)

    print("IP Analysis of Gitlab Projects is now complete. Goodbye!")
    logger.info("IP Analysis of Gitlab Projects is now complete. Goodbye!")
