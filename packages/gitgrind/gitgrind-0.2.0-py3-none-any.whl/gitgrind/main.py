#!/usr/bin/env python3
import pygit2
import os
import argparse
import logging

# import subprocess
import re
import sys



class GitGrind:
    """
    Find
    """

    def __init__(self, repo, details = False, verbose = False, logger = logging.getLogger(__name__)):
        self.repo = repo
        self.details = details
        self.verbose = verbose
        self.logger = logger

    def get_files_from_tree(repo, tree, path=""):
        """
        Recursively walks a pygit2 Tree object and yields all file paths.

        Args:
            repo (pygit2.Repository): The repository object.
            tree (pygit2.Tree): The current tree object to walk.
            path (str): The current path prefix for files within the tree.

        Yields:
            str: The full path of each file found in the tree.
        """
        for entry in tree:
            entry_path = os.path.join(path, entry.name)
            if entry.type == pygit2.GIT_OBJECT_TREE:
                # If it's a subtree, recursively call the function
                subtree = repo[entry.id]
                yield from GitGrind.get_files_from_tree(repo, subtree, entry_path)
            elif entry.type == pygit2.GIT_OBJECT_BLOB:
                # If it's a blob (a file), yield its path
                yield entry_path

    @staticmethod
    def diff_files(diff):
        for patch in diff:
            yield patch.delta.new_file.path

    def show_commit_changes(self, diff, expression, data):
        """
        Shows the changes introduced by a specific commit in a pygit2 repository.

        Args:
            repo_path (str): The path to the Git repository.
            commit_id (str): The SHA-1 hash or a reference to the commit.
        """
        try:

            for patch in diff:
                data2 = data.copy()
                data2["files"] = [patch.delta.new_file.path, patch.delta.old_file.path]
                if self.logic_match(expression, data2):
                    for hunk in patch.hunks:
                        print(
                            f"@@ -{hunk.old_start},{hunk.old_lines} +{hunk.new_start},{hunk.new_lines} @@"
                        )
                        for line in hunk.lines:
                            # 'origin' indicates the type of line (added, deleted, context)
                            if line.origin == "+":  # pygit2.GIT_DIFF_LINE_ADD:
                                print(f"+{line.content.strip()}")
                            elif line.origin == "-":  # pygit2.GIT_DIFF_LINE_DEL:
                                print(f"-{line.content.strip()}")
                            else:  # Context line
                                print(f" {line.content.strip()}")
                else:
                    if self.verbose:
                        print("changed ", patch.delta.new_file.path)

        except Exception as e:
            print(f"An error occurred: {e}")

    def logic_match(self, search_term, data):
        """
        execute logic statement user specified and get the truth value
        """
        try:
            cmd = f"result={search_term}"
            exec(cmd, globals(), data)
            result = data["result"]
        except Exception as e:
            self.logger.error(e)
            self.logger.error("Command: %s\nVariables: %s\nException: %s\n", cmd, data,e )
            raise e
        return result


    def check_match(self, matching_commits, commit, search_term, search_by):
        """
        Run the user specified matching rules in the commit
        """
        self.logger.debug("Commit %s - searchby %s", commit.id, search_by)

        if not commit.parents:
            self.logger.info(
                f"Commit {commit.id} is the initial commit and has no parent to compare against."
            )
            return

        parent_commit = commit.parents[0]
        diff = self.repo.diff(parent_commit.tree, commit.tree)
        data = {
            "message": commit.message.lower().strip(),
            "author": commit.author.name.lower(),
            "email": commit.author.email.lower(),
            "files": [x for x in self.diff_files(diff)],
        }

        if search_by == "logic":
            self.logger.debug("check for match: %s %s", data, search_term)
            try:

                result = self.logic_match(search_term, data)
            except BaseException as e:
                self.logger.error(e)
            if result:
                self.logger.debug("MATCH: %s %s", data, search_term)
                matching_commits.append(commit)
                if self.details:
                    # result = subprocess.run(['git', 'show', '-p', commit.id], capture_output=True, text=True, check=True)
                    # print(result.stdout)
                    print(f"Changes for commit {commit.id}:")
                    self.show_commit_changes(diff, search_term, data)
            else:
                self.logger.debug("Not a match: %s %s", data, search_term)

        elif search_by == "message":
            if search_term.lower() in commit.message.lower():
                matching_commits.append(commit)
        elif search_by == "author":
            if (
                search_term.lower() in commit.author.name.lower()
                or search_term.lower() in commit.author.email.lower()
            ):
                matching_commits.append(commit)
        elif search_by == "file":
            for file_path in self.get_files_from_tree(self.repo, commit.tree):
                # Check if the entry is a blob (representing a file)
                if search_term.lower() in file_path.lower():
                    if self.details:
                        # result = subprocess.run(['git', 'show', '-p', commit.id], capture_output=True, text=True, check=True)
                        # print(result.stdout)
                        self.show_commit_changes(diff, search_term, data)
                    matching_commits.append(commit)
        else:
            print(f"Invalid search_by option: {search_by}. Use 'message' or 'author'.")
            return []

    def search_commits(self, repo, search_term, search_by):
        """
        Searches for commits in a pygit2 repository.

        Args:
            repo_path (str): The path to the Git repository.
            search_term (str): The string to search for.
            search_by (str): 'message' to search in commit messages, 
                            'author' to search in author names/emails.
        
        Returns:
            list: A list of pygit2.Commit objects that match the search criteria.
        """


        matching_commits = []
        # Start walking from the HEAD of the repository
        head_commit_id = repo.head.target
        
        for commit in repo.walk(head_commit_id, pygit2.GIT_SORT_TIME):
            self.check_match(matching_commits, commit, search_term, search_by)
        return matching_commits

    @staticmethod
    def isdupe(commit_id, found):
        """
        check for duplicate commits in already found commits
        """
        for t, v in found.items():
            ids = [it.id for it in v]
            if commit_id in ids:
                return True
        return False

    def search_stash(self, matching_commits, repo, search_term, search_by, found):
        """
        Enumerate stashs to find commmits
        """
        for stash_commit in repo.listall_stashes():
            if not GitGrind.isdupe(stash_commit.commit_id, found):
                commit = repo.revparse_single(str(stash_commit.commit_id))
                self.check_match(matching_commits, commit, search_term, search_by)

    @staticmethod
    def find_dangling_commits(repo):
        """
        Finds and returns a list of Oids for dangling commits in a git repository.
        """

        # 1. Collect all reachable objects
        reachable_objects = set()

        # Iterate over all references (heads, tags, remotes)
        for ref in repo.references:
            try:
                # Get the Oid the reference points to
                ref_oid = repo.references[ref].target
                # Walk the history from this Oid
                for commit in repo.walk(ref_oid, pygit2.GIT_SORT_TIME):
                    reachable_objects.add(commit.id)
                    # Add all objects associated with this commit (tree and blobs)
                    tree = commit.tree
                    reachable_objects.add(tree.id)
                    for entry in tree:
                        reachable_objects.add(entry.id)

            except pygit2.GitError:
                # Some references might be broken, skip them
                continue

        # 2. Iterate over all objects in the ODB
        all_objects = set()
        # Iterating the repository object (repo) calls git_odb_foreach internally
        for oid in repo:
            all_objects.add(oid)

        # 3. Identify dangling commits (objects present in all_objects but not reachable_objects)
        dangling_oids = all_objects - reachable_objects
        dangling_commits = []

        for oid in dangling_oids:
            # Check if the object is actually a commit
            try:
                obj = repo[oid]
                if obj.type == pygit2.GIT_OBJECT_COMMIT:
                    dangling_commits.append(oid)
            except KeyError:
                continue  # Object might have been packed/garbage collected during iteration

        return dangling_commits

    def search_dangle(self, matching_commits, repo, search_term, search_by, found):
        """
        search for dangling commits 
        """
        dangling = GitGrind.find_dangling_commits(repo)

        self.logger.info(f"Found {len(dangling)} dangling commits:")
        for oid in dangling:
            commit = repo.revparse_single(str(oid))
            if not GitGrind.isdupe(commit.id, found):
                self.check_match(matching_commits, commit, search_term, search_by)

        for stash_commit in repo.listall_stashes():
            if not GitGrind.isdupe(str(stash_commit.commit_id), found):
                commit = repo.revparse_single(str(stash_commit.commit_id))
                self.check_match(matching_commits, commit, search_term, search_by)

    def grind(self, value, _type):
        """
        Scans all commit types and returns segmented results
        """
        found_normal = self.search_commits(self.repo, value, _type)
        found_stash = []
        found_dangle = []
        found = {"normal": found_normal, "stash": found_stash, "dangle": found_dangle}
        self.search_stash(found_stash, self.repo, value, _type, found)
        self.search_dangle(found_dangle, self.repo, value, _type, found)

        found = {"normal": found_normal, "stash": found_stash, "dangle": found_dangle}
        return found


def main_function():
    """
    for command line execution
    """
    parser = argparse.ArgumentParser(
        prog="gitgrind",
        description="searches one or more repos for commits based on file content, author, commit msg",
        epilog="""

Commit context variables:
=========================
author - author name
email - author email
message - full commit message
files - array of filenames touched

Example:
========
'message': commit.message.lower(),
'author': commit.author.name.lower(),
'email': commit.author.email.lower(),
        'files': [x for x in diff_files(diff)]

gitgrind -r * --condition "'username' in author and 'some feature' in message"


""",
    )

    parser.add_argument(
        "-f",
        "--find",
        required=True,
        help="quoted python condition statement using commit context variables",
    )
    parser.add_argument(
        "-r",
        "--recursive",
        action="store_true",
        help="search subdirectories for repositories",
    )
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )
    parser.add_argument(
        "-b", "--batch", action="store_true", help="show commit changes (diffs)"
    )
    parser.add_argument(
        "-d", "--details", action="store_true", help="show commit changes (diffs)"
    )
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(
            level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
        )
    else:
        logging.basicConfig(level=logging.WARNING, format="%(message)s")

    logger = logging.getLogger(__name__)

    # Create a dummy repository for demonstration if it doesn't exist
    repo_dir = "."
    try:
        repo = pygit2.Repository(repo_dir)
    except pygit2.GitError as e:
        print(f"Error opening repository: {e}")
        sys.exit(1)

    grind = GitGrind(repo, details=args.details, verbose=args.verbose, logger=logger)

    # do the work
    found = grind.grind(args.find, "logic")

    # display the results
    for t, v in found.items():
        for commit in v:
            if args.batch:
                print(commit.id)
            else:
                print(
                    f"{t}:  Commit ID: {commit.id}, Author: {commit.author} Message: {commit.message.strip()}"
                )

    sys.exit(0 if found['normal'] else 1)


if __name__ == "__main__":
    # This block only executes when the script is run directly.
    # It calls the main function to start the program's execution.
    main_function()
