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

__version__ = "0.1.0"

import requests
import json


def get_repositories(project_id, logger):
    api_url = 'https://projects.eclipse.org/api/projects/' + project_id
    try:
        # Make an HTTP GET request to the API URL
        response = requests.get(api_url)

        # Raise an exception for HTTP errors (4xx or 5xx)
        response.raise_for_status()

        # Parse the JSON response
        json_data = response.json()[0]

        repositories = {}

        # GitHub repositories
        if 'github_repos' in json_data:
            repositories['github'] = []
            for repo in json_data['github_repos']:
                repositories['github'].append(repo['url'])

        # GitLab repositories
        if 'gitlab_repos' in json_data:
            repositories['gitlab'] = []
            for repo in json_data['gitlab_repos']:
                repositories['gitlab'].append(repo['url'])

        return repositories
    except requests.exceptions.RequestException as e:
        # Handle any request-related errors (e.g., network issues, invalid URL, HTTP errors)
        logger.error(f"Error fetching data from {api_url}: {e}")
        return None
    except json.JSONDecodeError as e:
        # Handle JSON decoding errors if the response is not valid JSON
        logger.error(f"Error decoding JSON from {api_url}: {e}")
        return None
    except Exception as e:
        # Catch any other unexpected errors
        logger.error(f"An unexpected error occurred: {e}")
        return None
