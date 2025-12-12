<!--
 * Copyright (c) 2024 The Eclipse Foundation
 * 
 * This program and the accompanying materials are made available under the
 * terms of the Eclipse Public License v. 2.0 which is available at
 * http://www.eclipse.org/legal/epl-2.0.
 * 
 * SPDX-FileType: DOCUMENTATION
 * SPDX-FileCopyrightText: 2024 The Eclipse Foundation
 * SPDX-License-Identifier: EPL-2.0
-->

Eclipse IP Analysis
=============
![PyPI - Version](https://img.shields.io/pypi/v/eclipse-ipa)
![PyPI - Python Version](https://img.shields.io/pypi/pyversions/eclipse-ipa)
[![License](https://img.shields.io/badge/License-EPL_2.0-green.svg)](https://www.eclipse.org/legal/epl-2.0/)
[![REUSE status](https://api.reuse.software/badge/gitlab.eclipse.org/eclipse/technology/dash/ip-check)](https://api.reuse.software/info/gitlab.eclipse.org/eclipse/technology/dash/ip-analysis)

# About

Eclipse IP Analysis (IPA) enables seamless third-party dependency analysis in GitLab and GitHub repositories and
groups/organizations using the [Eclipse Dash License Tool](https://github.com/eclipse-dash/dash-licenses).
As default output, it generates a comprehensive HTML report with the results.

_List of currently supported programming languages: Go, Java (Maven and Gradle), JavaScript (NPM and Yarn),
TypeScript (NPM and Yarn), Kotlin (Gradle), Python (PyPi and Conda)._

# Getting Started

## Base Requirements

To run the tool, you must install the base requirements described below.

- Python >=3.10: check your Python version with the command ```python3 --version```. Also, check that you
have the Python Package Manager (pip) installed. Similar to Python, you can run ```pip3 --version```. The resulting line 
should contain your version of Python at its end. If pip is not installed, official documentation can be followed 
[here](https://pip.pypa.io/en/stable/installation/).

- Java JDK 11 or above: the latest version can be safely installed. Check that Java is installed and what's the current
version by running the command ```java --version```.

- Apache Maven: the latest version can be safely installed. Check that Maven is installed and what's the current version
by running the command ```mvn --version```.

- Git CLI: the latest version can be safely installed. Check that Git is installed and what's the current version by
running the command ```git --version```.

## Install

```pip3 install eclipse-ipa```

## Build from Source (Optional)

- Clone this repository using your favorite Git software or the command line. For the command line, please execute:

```git clone https://gitlab.eclipse.org/eclipse/technology/dash/ip-analysis.git```

- Navigate to the directory of the repository that you just cloned.
- Get Hatch to build the tool (https://hatch.pypa.io/latest/install).
- Build and install the tool:

```hatch build```

```pip3 install dist/eclipse_ipa-*.whl```

([back to top](#About))

# Usage

Run the tool with the following command:

```eclipse-ipa [-h] [-ci] [-gh] [--gh-token GH_TOKEN] [-gl GITLAB] [--gl-token GL_TOKEN]```

```            [-b BRANCH] [-c CONFIG] [-df DEPENDENCIES_FILE] [-e ECLIPSE_PROJECT]```

```            [-g GROUP] [-l] [-p PROJECT] [-pf PROJECTS_FILE] [-r [REVIEW]] [-s] [-v]```

The command does not require any of its options. However, a minimum set is needed to execute simple IP analysis if
a configuration file is not specified.

A summary of the options is given below:

```
  -h, --help            show this help message and exit
  -ci, --ci_mode        execute in CI mode
  -gh, --github         execute for GitHub
  --gh-token GH_TOKEN   Github access token for API
  -gl GITLAB, --gitlab GITLAB
                        execute for GitLab URL
  --gl-token GL_TOKEN   Gitlab access token for API/IP review
  -b BRANCH, --branch BRANCH
                        branch to analyze
  -c CONFIG, --config CONFIG
                        config file to use
  -df DEPENDENCIES_FILE, --dependencies-file DEPENDENCIES_FILE
                        file with dependencies to analyze
  -e ECLIPSE_PROJECT, --eclipse-project ECLIPSE_PROJECT
                        execute for Eclipse Project
  -g GROUP, --group GROUP
                        Github Organization/Gitlab Group to analyze
  -l, --declared-licenses
                        get declared licenses from package repositories
  -p PROJECT, --project PROJECT
                        Github/Gitlab project to analyze
  -pf PROJECTS_FILE, --projects-file PROJECTS_FILE
                        file with projects to analyze
  -r [REVIEW], --review [REVIEW]
                        Eclipse Project ID for IP review
  -s, --summary         output is an Eclipse Dash summary file
  -v, --version         show the version and exit
```

To start using the tool, you must provide **one of the following _six_ options**:

1. An Eclipse Project ID (e.g., technology.dash). This is specified with option -e as summarized above.

2. A file with the dependencies to analyze (one per line) using the format supported by Eclipse Dash. 
The full path of this file is specified with option -df as summarized above.

3. A file with the list of GitHub/GitLab Projects to analyze. Each line should contain the GitHub/GitLab project 
complete name with namespace or URL. The full path of this file is specified with option -pf as summarized above.

Example for a GitHub line:

```kubernetes-client/python```

Example for a GitLab line:

```eclipse/technology/dash/ip-analysis```

4. A GitHub Organization, or a GitLab Group. Provide name with namespace or URL. 
This is specified with option -g as summarized above.

5. A GitHub Project, or a GitLab Project. Provide name with namespace or URL. 
This is specified with option -p as summarized above.

6. A configuration file, specified with option -c as summarized above. It allows additional customization, and a sample
is provided in the same folder as the tool with the filename *config.ini.sample*. Parameters within the config file are 
described in the comments.

_Please note that, for GitHub API public access, the API rate limits are very low. It's highly recommended to provide 
an access token in such cases._

## Usage Examples

Run for a GitHub repository:

```eclipse-ipa -gh --gh-token <GitHub Token> -p eclipse-dash/dash-licenses```

Run for a GitHub organization:

```eclipse-ipa -gh --gh-token <GitHub Token> -g eclipse-dash```

_IMPORTANT: It's highly recommended to use a GitHub token to have higher API rate limits for GitHub projects._

Run for a GitLab project:

```eclipse-ipa -gl gitlab.eclipse.org -p eclipse/technology/dash/ip-analysis```

Run for a GitLab group:

```eclipse-ipa -gl gitlab.eclipse.org -g eclipse/technology/dash```

Run for an Eclipse project (can have both GitHub and GitLab projects):

```eclipse-ipa --gh-token <GitHub Token> -e technology.dash```

_IMPORTANT: It's highly recommended to use a GitHub token to have higher API rate limits for GitHub projects._

Run for an Eclipse project and enable Automatic IP Team Review Requests:

```eclipse-ipa --gh-token <GitHub Token> --gl-token <GitLab Token> -e technology.dash -r```

_NOTE: A GitLab token is required for Automatic IP Team Review Requests (-r). For this example, the Eclipse 
Project ID will be re-used from the provided Eclipse Project (-e)._

## How the tool works

If a GitHub Organization/GitLab Group or a list of GitHub/GitLab Projects is provided, the tool fetches the programming
languages for each project and searches for dependency files for each supported programming language. Once a list of
dependency locations is found, it runs Eclipse Dash on those dependencies to analyze their IP approval status.

At the end, and by default, the tool outputs a full report in HTML. Any additional details can be found in the log file
(ip-analysis.log).

([back to top](#About))

# License

This program and the accompanying materials are made available under the terms of the Eclipse Public License 2.0, which 
is available at http://www.eclipse.org/legal/epl-2.0.

([back to top](#About))
