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

from fnmatch import translate
from re import match

from colorama import Fore, Style
from requests import exceptions, get


def find_dependencies_gitlab(config, logger, lang, files, default_filenames):
    # Attempt to find dependency files
    filepaths = set()
    for pattern in config.get(lang, 'DependencySearch', fallback=default_filenames).split(','):
        # Pattern to regex
        regex = translate(pattern.strip())
        for f in files:
            if match(regex, f['name']):
                filepaths.add(f['path'])
    # print(filepaths)
    logger.info(f"Dependency filepaths for {lang}: {str(filepaths)}")
    return filepaths


def find_dependencies_github(config, logger, lang, files, default_filenames):
    # Attempt to find dependency files
    filepaths = set()
    for pattern in config.get(lang, 'DependencySearch', fallback=default_filenames).split(','):
        # Pattern to regex
        regex = translate(pattern.strip())
        for f in files:
            if match(regex, f.name):
                filepaths.add(f.path)
    # print(filepaths)
    logger.info(f"Dependency filepaths for {lang}: {str(filepaths)}")
    return filepaths


def add_gldep_locations(dependency_locations, proj, lang, paths):
    for path in paths:
        try:
            dependency_locations[proj.path_with_namespace][lang].append(str(proj.path_with_namespace) + '/' + path)
        except KeyError:
            dependency_locations[proj.path_with_namespace][lang] = []
            dependency_locations[proj.path_with_namespace][lang].append(str(proj.path_with_namespace) + '/' + path)


def add_ghdep_locations(dependency_locations, proj, lang, paths):
    for path in paths:
        try:
            dependency_locations[proj][lang].append(path)
        except KeyError:
            dependency_locations[proj][lang] = []
            dependency_locations[proj][lang].append(path)


def _fetch_pypi_metadata(package_name):
    pypi_url = "https://pypi.org/pypi"
    json_url = f"{pypi_url}/{package_name}/json"

    try:
        # Make the request to the PyPI API with a timeout
        response = get(json_url, timeout=30)

        # Raise an exception for bad status codes (4xx or 5xx)
        response.raise_for_status()

        return response.json()
    except exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"Package '{package_name}' not found on PyPI.") from e
        raise ValueError(
            f"Failed to retrieve data from PyPI. Status: {e.response.status_code}"
        ) from e
    except exceptions.RequestException as e:
        # Handle network-related errors like timeouts or connection issues
        raise ValueError(f"Request to PyPI failed: {e}") from e


def get_pypi_latest_version(package_name):
    data = _fetch_pypi_metadata(package_name)

    # Extract the latest version
    try:
        latest_version = data["info"]["version"]
        return latest_version
    except KeyError:
        raise ValueError(f"Could not find 'info' or 'version' in PyPI response for {package_name}.")


def get_pypi_package_license(package_name, version):
    data = _fetch_pypi_metadata(package_name)

    # Check if the requested version exists
    if version not in data.get("releases", {}):
        raise ValueError(
            f"Version '{version}' not found for package '{package_name}'."
        )

    # Use version-specific metadata first
    release_metadata_list = data["releases"][version]

    # If the release list is empty, we cannot find version-specific license information
    if release_metadata_list:
        # Use the first uploaded file's metadata for this release
        release_metadata = release_metadata_list[0]

        # Check explicit 'license' field in the version-specific metadata
        license_value_version = release_metadata.get("license")
        explicit_license_version = ""
        if license_value_version is not None:
            explicit_license_version = str(license_value_version).strip()

        if explicit_license_version and explicit_license_version != "UNKNOWN" and len(explicit_license_version) < 100:
            return explicit_license_version

        # Check classifiers in the version-specific metadata
        classifiers_version = release_metadata.get("classifiers", [])
        license_classifiers_version = [
            c for c in classifiers_version if c.startswith("License ::") and "OSI Approved" in c
        ]

        if license_classifiers_version:
            license_string = license_classifiers_version[0].replace("License :: OSI Approved :: ", "")
            return license_string

    # Fallback to global package metadata (info block)
    info = data.get("info", {})

    # Check explicit 'license' field in the global info block
    license_value_global = info.get("license")
    explicit_license_global = ""
    if license_value_global is not None:
        explicit_license_global = str(license_value_global).strip()

    if explicit_license_global and explicit_license_global != "UNKNOWN" and len(explicit_license_global) < 100:
        return explicit_license_global

    # Check classifiers in the global info block
    classifiers_global = info.get("classifiers", [])
    license_classifiers_global = [
        c for c in classifiers_global if c.startswith("License ::") and "OSI Approved" in c
    ]

    if license_classifiers_global:
        license_string = license_classifiers_global[0].replace("License :: OSI Approved :: ", "")
        return license_string

    return "Unknown"


def _fetch_npm_metadata(package_name):
    npm_url = "https://registry.npmjs.org"
    json_url = f"{npm_url}/{package_name}"

    try:
        response = get(json_url, timeout=30)
        response.raise_for_status()
        return response.json()
    except exceptions.HTTPError as e:
        if e.response.status_code == 404:
            raise ValueError(f"Package '{package_name}' not found on npm registry.") from e
        raise ValueError(
            f"Failed to retrieve data from npm registry. Status: {e.response.status_code}"
        ) from e
    except exceptions.RequestException as e:
        raise ValueError(f"Request to npm registry failed: {e}") from e


def get_npm_package_license(package_name, version):
    # Handle the non-scoped prefix
    if package_name.startswith('-/'):
        package_name = package_name[2:]

    data = _fetch_npm_metadata(package_name)

    # Check if the requested version exists
    versions = data.get("versions", {})
    if version not in versions:
        raise ValueError(
            f"Version '{version}' not found for package '{package_name}'."
        )

    # Get metadata for the specific version
    version_metadata = versions[version]

    # Extract the license, which is usually directly available as a string or object.
    license_value = version_metadata.get("license")

    explicit_license = ""
    if license_value is not None:
        # Convert the value to a clean string
        explicit_license = str(license_value).strip()

    # The license should be explicit in npm metadata
    if explicit_license and explicit_license.upper() not in ["UNKNOWN", "NOASSERTION"] and len(explicit_license) < 100:
        return explicit_license

    # Fallback to the top-level 'license' field if version-specific info is missing or generic
    top_level_license_value = data.get("license")

    top_level_license = ""
    if top_level_license_value is not None:
        top_level_license = str(top_level_license_value).strip()

    if top_level_license and top_level_license.upper() not in ["UNKNOWN", "NOASSERTION"] and len(
            top_level_license) < 100:
        return top_level_license

    return "Unknown"


def add_error_report(config, location, error):
    if config['output_report']:
        return {'location': location, 'name': error, 'declared_license': '-', 'license': '', 'status': 'error',
                'authority': '-', 'review': ''}
    return {}


def print_error(message):
    print(f"{Fore.RED}[ERROR] {message}{Style.RESET_ALL}")


def print_warning(message):
    print(f"{Fore.YELLOW}[WARNING] {message}{Style.RESET_ALL}")
