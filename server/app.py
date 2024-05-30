from flask import Flask, jsonify
from flask_cors import CORS
import requests
import logging
import os
from collections import Counter

app = Flask(__name__)
CORS(app)

# Set up logging
logging.basicConfig(level=logging.DEBUG)

# Get the GitHub token from environment variables
GITHUB_TOKEN = os.getenv('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')
HEADERS = {
    'Authorization': f'token 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'
}

@app.route('/api/user-stats/<username>', methods=['GET'])
def get_user_stats(username):
    app.logger.debug(f'Request received for user: {username}')
    try:
        user_response = requests.get(f'https://api.github.com/users/{username}', headers=HEADERS)
        
        if user_response.status_code != 200:
            return jsonify({'error': 'User not found'}), 404
        
        repos_url = user_response.json().get('repos_url')
        if not repos_url:
            return jsonify({'error': 'Unable to retrieve repos URL'}), 500
        
        repos = []
        page = 1
        total_forks = 0
        total_stargazers = 0
        language_counter = Counter()

        while True:
            repo_response = requests.get(repos_url, headers=HEADERS, params={'page': page, 'per_page': 100})
            app.logger.debug(f'Repos API response: {repo_response.status_code}, Page: {page}, {repo_response.text}')
            
            if repo_response.status_code != 200:
                return jsonify({'error': 'Failed to fetch repos'}), repo_response.status_code
            
            repos_page = repo_response.json()
            if not repos_page:
                break
            repos.extend(repos_page)

            for repo in repos_page:
                language_url = repo.get('languages_url')
                if language_url:
                    language_response = requests.get(language_url, headers=HEADERS)
                    if language_response.status_code == 200:
                        languages = language_response.json()
                        language_counter.update(languages.keys())

            total_forks += sum(repo.get('forks_count', 0) for repo in repos_page)
            total_stargazers += sum(repo.get('stargazers_count', 0) for repo in repos_page)
            if len(repos_page) < 100:
                break
            page += 1

        sorted_languages = language_counter.most_common()

        stats = {
            'totalRepos': len(repos),
            'totalForks': total_forks,
            'languages': sorted_languages,
            'totalStargazers': total_stargazers,
            
        }

        app.logger.debug(f'Stats calculated: {stats}')
        return jsonify(stats)
    except Exception as e:
        app.logger.error(f'Error occurred: {str(e)}')
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)


