import requests
import re
import argparse
import logging
import os

# Initialize logging
logging.basicConfig(level=logging.INFO)

# Initialize the parser
parser = argparse.ArgumentParser(description='Fetch the first comment of specified PRs and write them to a file.')
parser.add_argument('input_file', help='The input file containing the list of PR numbers')
parser.add_argument('output_file', help='The output file to write the PR comments to')
parser.add_argument('--token', help='GitHub token for authentication', required=False, default=os.getenv('GITHUB_TOKEN'))
parser.add_argument('--owner', help='Repository owner', required=True)
parser.add_argument('--repo', help='Repository name', required=True)

# Parse the command-line arguments
args = parser.parse_args()

def get_first_pr_comment(owner, repo, pr_number, token):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{pr_number}/comments"
    headers = {"Authorization": f"token {token}"}
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raises stored HTTPError, if one occurred
        comments = response.json()
        return comments[0]['body'] if comments else "No comments found."
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP error occurred: {http_err}")
    except Exception as err:
        logging.error(f"An unexpected error occurred: {err}")
    return "Failed to fetch comments."

def extract_pr_numbers(filename):
    pr_numbers = []
    try:
        with open(filename, 'r') as file:
            for line in file:
                match = re.search(r'\bPR\s*(\d+)\b', line)  # Adjusted regex to '\bPR\s*(\d+)\b'
                if match:
                    pr_number = int(match.group(1))
                    pr_numbers.append(pr_number)
    except FileNotFoundError:
        logging.error(f"The file '{filename}' was not found.")
        exit()
    except Exception as e:
        logging.error(f"An unexpected error occurred while reading '{filename}': {e}")
        exit()
    return pr_numbers

try:
    pr_numbers = extract_pr_numbers(args.input_file)
    with open(args.output_file, "w") as file:
        for pr_number in pr_numbers:
            first_comment = get_first_pr_comment(args.owner, args.repo, pr_number, args.token)
            output = f"PR #{pr_number}\nFirst comment: {first_comment}\n\n"
            file.write(output)
            logging.info(f"Processed PR #{pr_number}")
    logging.info(f"Finished writing comments to {args.output_file}")
except IOError as e:
    logging.error(f"An error occurred while opening or writing to the file: {e}")
except Exception as e:
    logging.error(f"An unexpected error occurred: {e}")
