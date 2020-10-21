import argparse
from io import StringIO

import git
import requests
from unidiff import PatchSet


def main(commit_sha, comments_url, github_token):
    repository = git.Repo()

    uni_diff_text = repository.git.diff(unified=0)

    patch_set = PatchSet(StringIO(uni_diff_text))

    hunks = []
    for patched_file in patch_set:
        file_path = patched_file.path

        for hunk in patched_file:
            hunk_json = {
                "start_line": hunk.source_start,
                "line": hunk.source_start + hunk.source_length - 1,
                "body": comment_body(hunk),
                "path": file_path,
                "commit_id": commit_sha,
                "side": "RIGHT",
                "start_side": "RIGHT",
            }
            hunks.append(hunk_json)

    for hunk in hunks:
        headers = {
            "Authorization": f"token {github_token}",
            "Content-Type": "application/json",
            "Accept": "application/vnd.github.comfort-fade-preview+json",
        }
        if hunk["start_line"] >= hunk["line"]:
            #     Single line comment
            headers.pop("Accept")
            hunk["line"] = hunk.pop("start_line")
        print(f"Making request: {hunk}")
        resp = requests.post(comments_url, json=hunk, headers=headers)
        if resp.status_code >= 400:
            print(f"Error: {resp.content.decode()}")


def comment_body(hunk):
    changes = "".join([str(l)[1:] for l in hunk if l.is_added])
    if changes.endswith("\n"):
        changes = changes[:-1]
    return f"```suggestion \n{changes}\n```"


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "commit_sha",
    )
    parser.add_argument("comments_url")
    parser.add_argument("github_token")
    args = parser.parse_args()
    main(**vars(args))
