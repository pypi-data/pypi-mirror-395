import json
import locale as locale_module
import logging
import re
import subprocess
import time
from pathlib import Path
from typing import Dict, List, Optional, Sequence

from .i18n import _


class AutolandError(Exception):
    """Base class for errors that occur during autoland processing"""


class AutolandService:
    """
    Service layer that implements the flow for automatically correcting and merging GitHub PRs.
    """

    LONG_HTML_COMMENT_PATTERN = re.compile(r'<!--.{100,}?-->')

    GH_COMMAND = "gh"

    AGENT_CONFIGS = {
        "codex": {
            "command": "codex",
            "args": ["exec", "--dangerously-bypass-approvals-and-sandbox", "-"],
        },
        "claude": {
            "command": "claude",
            "args": ["--print", "--dangerously-skip-permissions"],
        },
        "gemini": {
            "command": "gemini",
            "args": ["--yolo"],
        },
    }

    def load_prompt(self, filename: str) -> str:
        """
        Load a prompt file from the contents directory.
        """
        prompt_path = Path(__file__).parent / "contents" / filename
        try:
            return prompt_path.read_text(encoding="utf-8").strip()
        except FileNotFoundError as exc:
            raise AutolandError(_("Prompt file not found") + f": {prompt_path}") from exc

    def __init__(
        self,
        *_args,
        agent: str = "codex",
        polling_interval: Optional[int] = None,
        locale: Optional[str] = None,
        repo: Optional[str] = None,
        verbose: bool = False,
        create_issue: bool = True,
        **_kwargs
    ) -> None:
        level = logging.DEBUG if verbose else logging.INFO
        logging.basicConfig(
            level=level,
            format="%(asctime)s [%(levelname)s] %(message)s",
        )
        self.logger = logging.getLogger("autoland")

        self.agent = agent
        self.polling_interval = polling_interval
        self.repo = repo
        self.create_issue = create_issue

        if locale:
            locale_module.setlocale(locale_module.LC_ALL, locale)

        loc, _ = locale_module.getlocale()
        if loc is None or loc == "C":
            loc = "en_US"
        self.locale = loc

        self.authenticated_user = None

    def log_pr(self, level: int, pr_number: int, msg: str, *args) -> None:
        """
        Log a message with PR number prefix.

        Args:
            level: Logging level (logging.INFO, logging.ERROR, etc.)
            pr_number: PR number to include in prefix
            msg: Translatable message string
            *args: Arguments for string formatting
        """
        self.logger.log(level, f"PR #{pr_number}: " + msg, *args)

    def execute(self) -> None:
        """
        CLI entry point. Explores open PRs and progresses the automatic correction flow.
        """
        pr_number = self.fetch_oldest_open_pr_number()
        if pr_number is None:
            self.logger.info(_("No open pull requests found. Terminating process."))
            return

        # Flow 1: Fetch PR data and checkout branch (once only)
        initial_pr_data = self.fetch_pr_data(pr_number)
        if not initial_pr_data:
            raise AutolandError(_("Could not retrieve information for PR #{number}").format(number=pr_number))

        self.checkout_pr(pr_number)

        project_instructions = self.load_project_instructions()
        if project_instructions:
            self.log_pr(logging.INFO, pr_number, _("Loaded project instructions from AUTOLAND.md"))

        while True:
            self.log_pr(logging.INFO, pr_number, _("Starting to wait for checks completion"))
            self.wait_for_checks_completion(pr_number)

            pr_data = self.fetch_pr_data(pr_number)
            timeline = self.format_pr_timeline(pr_data)

            context_blocks = []
            if project_instructions:
                context_blocks.append(
                    "IMPORTANT: Follow these project-specific instructions:\n\n"
                    + project_instructions
                    + "\n\n--- END OF PROJECT INSTRUCTIONS ---"
                )
            context_blocks.append(timeline)

            self.log_pr(logging.INFO, pr_number, _("Sending review correction prompt to %s (this may take some time)"), self.agent)
            agent_response = self.invoke_agent_with_prompt(
                prompt_body=self.load_prompt("review_correction.txt"),
                context_blocks=context_blocks,
            )

            if agent_response is None:
                raise AutolandError(_("Could not get response from {agent}").format(agent=self.agent))

            # Parse agent response in format "NUMBER|CONTENT"
            response_parts = agent_response.strip().split('|', 1)
            response_code = response_parts[0].strip()
            content = response_parts[1].strip() if len(response_parts) > 1 else ""

            if response_code not in ["0", "1"]:
                msg = _("Received unexpected response from %s") + ": %s"
                self.logger.warning(msg, self.agent, agent_response.strip())
                return

            # Post agent report as comment
            if content:
                self.gh_post_comment(pr_number, content)
            else:
                self.log_pr(logging.WARNING, pr_number, _("Agent returned empty content, skipping comment"))

            if response_code == "0":
                # No corrections needed, proceed with merge
                self.log_pr(logging.INFO, pr_number, _("Agent indicates no corrections needed. Proceeding with merge"))
                self.merge_pr(pr_number)
                return

            # Corrections were made (response_code == "1"), push changes and continue loop
            has_changes = self.push_if_needed()
            if has_changes:
                self.log_pr(logging.INFO, pr_number, _("Pushed changes"))
                self.log_pr(logging.INFO, pr_number, _("Waiting %s seconds after push before starting checks completion wait"), self.polling_interval)
                time.sleep(self.polling_interval)
            else:
                self.log_pr(logging.WARNING, pr_number, _("Agent indicated corrections but no changes detected"))
                # Continue loop anyway to let agent reassess

    def execute_watch(self, interval: int = 300) -> None:
        """
        Execute autoland process continuously, monitoring for new PRs.

        Args:
            interval: Interval in seconds between PR processing attempts
        """
        consecutive_failures = 0
        max_consecutive_failures = 10

        while True:
            try:
                self.execute()
                consecutive_failures = 0
                self.logger.info(_("Waiting %s seconds before searching for next PR"), interval)
            except KeyboardInterrupt:
                break
            except Exception as error:  # pylint: disable=broad-exception-caught
                consecutive_failures += 1

                if consecutive_failures >= max_consecutive_failures:
                    self.logger.error(_("Too many consecutive failures. Manual intervention required."))
                    raise

                self.logger.error("%r", error)
                self.logger.error(_("Waiting %s seconds before retry."), interval)

            time.sleep(interval)

    def fetch_oldest_open_pr_number(self) -> Optional[int]:
        """
        Get the minimum numbered PR from the list of open PRs.
        """
        result = subprocess.run(
            [self.GH_COMMAND, "pr", "list", "--state", "open", "--json", "number", "--limit", "1", "--search", "-is:draft sort:created-asc"],
            capture_output=True,
            text=True,
            check=True,
        )

        prs = json.loads(result.stdout)

        if not prs:
            return None
        return prs[0]["number"]

    def get_authenticated_user(self) -> Optional[str]:
        """
        Get the login of the authenticated user (with caching).
        """
        if self.authenticated_user is not None:
            return self.authenticated_user

        result = subprocess.run(
            [self.GH_COMMAND, "api", "user", "--jq", ".login"],
            capture_output=True,
            text=True,
            check=True,
        )
        self.authenticated_user = result.stdout.strip()
        return self.authenticated_user

    def fetch_pr_data(self, pr_number: int) -> Dict:
        """
        Fetch basic PR information, comments, and commits in JSON format.
        """
        basic_data = self.fetch_basic_pr_data(pr_number)
        if not basic_data:
            return {}

        issue_comments = self.fetch_issue_comments(pr_number)
        review_comments = self.fetch_review_comments(pr_number)

        all_comments = self.merge_comments(issue_comments, review_comments)
        basic_data['comments'] = all_comments

        return basic_data

    def fetch_basic_pr_data(self, pr_number: int) -> Dict:
        """
        Fetch basic PR information (excluding comments).
        """
        cmd = [
            self.GH_COMMAND,
            "pr",
            "view",
            str(pr_number),
            "--json",
            "title,body,commits,author,createdAt,headRefName,mergeable",
        ]
        if self.repo:
            cmd.extend(["--repo", self.repo])

        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    def fetch_issue_comments(self, pr_number: int) -> List[Dict]:
        """
        Fetch issue comments for the PR.
        """
        cmd = [self.GH_COMMAND, "api", f"repos/{self.get_repo_name()}/issues/{pr_number}/comments"]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True,
        )
        return json.loads(result.stdout)

    def fetch_review_comments(self, pr_number: int) -> List[Dict]:
        """
        Fetch review comments for the PR (excluding resolved comments).
        """
        repo_name = self.get_repo_name()
        owner, repo = repo_name.split('/')

        # Fetch review threads including resolution status via GraphQL API
        # Cannot be retrieved with regular API
        # ref: https://github.com/orgs/community/discussions/9175
        graphql_query = f'''
        query {{
          repository(owner: "{owner}", name: "{repo}") {{
            pullRequest(number: {pr_number}) {{
              reviewThreads(first: 100) {{
                nodes {{
                  id
                  isResolved
                  comments(first: 50) {{
                    nodes {{
                      id
                      databaseId
                      createdAt
                      body
                      path
                      line
                      author {{
                        login
                      }}
                    }}
                  }}
                }}
              }}
            }}
          }}
        }}
        '''

        result = subprocess.run(
            [self.GH_COMMAND, "api", "graphql", "-f", f"query={graphql_query}"],
            capture_output=True,
            text=True,
            check=True,
        )

        data = json.loads(result.stdout)
        review_threads = data.get("data", {}).get("repository", {}).get("pullRequest", {}).get("reviewThreads", {}).get("nodes", [])

        # Extract only unresolved comments
        unresolved_comments = []
        for thread in review_threads:
            if not thread.get("isResolved", False):
                for comment in thread.get("comments", {}).get("nodes", []):
                    # Convert to REST API format
                    formatted_comment = {
                        "id": comment.get("databaseId"),
                        "created_at": comment.get("createdAt"),
                        "body": comment.get("body", ""),
                        "path": comment.get("path", ""),
                        "line": comment.get("line"),
                        "user": {"login": comment.get("author", {}).get("login", "unknown")}
                    }
                    unresolved_comments.append(formatted_comment)

        return unresolved_comments

    def get_repo_name(self) -> str:
        """
        Get the repository name. If the --repo option is not specified, infer from the current directory.
        """
        if self.repo:
            return self.repo

        result = subprocess.run(
            [self.GH_COMMAND, "repo", "view", "--json", "nameWithOwner", "--jq", ".nameWithOwner"],
            capture_output=True,
            text=True,
            check=True,
        )
        return result.stdout.strip()

    def load_project_instructions(self) -> Optional[str]:
        """
        Load project-specific instructions from AUTOLAND.md in the repository root.
        """
        autoland_path = Path("AUTOLAND.md")
        if not autoland_path.exists():
            return None

        try:
            content = autoland_path.read_text(encoding="utf-8").strip()
        except OSError as error:  # pragma: no cover - filesystem error handling
            self.logger.warning(_("Could not read %s: %s"), str(autoland_path), error)
            return None

        if not content:
            return None

        return content

    def merge_comments(self, issue_comments: List[Dict], review_comments: List[Dict]) -> List[Dict]:
        """
        Merge issue comments and review comments in chronological order with unified format.
        """
        unified_comments = []

        # Convert issue comments to unified format
        for comment in issue_comments:
            unified_comments.append({
                "id": str(comment.get("id", "")),
                "createdAt": comment.get("created_at", ""),
                "author": {"login": comment.get("user", {}).get("login", "unknown")},
                "body": comment.get("body", ""),
                "type": "issue_comment"
            })

        # Convert review comments to unified format
        for comment in review_comments:
            unified_comments.append({
                "id": str(comment.get("id", "")),
                "createdAt": comment.get("created_at", ""),
                "author": {"login": comment.get("user", {}).get("login", "unknown")},
                "body": comment.get("path", "") + comment.get("body", ""),
                "type": "review_comment",
                "path": comment.get("path", ""),
                "line": comment.get("line")
            })

        # Sort chronologically
        unified_comments.sort(key=lambda x: x["createdAt"])

        return unified_comments

    def wait_for_checks_completion(self, pr_number: int) -> None:
        """
        Wait for PR checks to complete
        """
        # Set check=False because non-zero is returned even when checks fail (tests not passing)
        subprocess.run([
            self.GH_COMMAND, "pr", "checks", str(pr_number),
            "--watch", "--interval", str(self.polling_interval)
        ], check=False, timeout=3600)
        self.log_pr(logging.INFO, pr_number, _("All checks completed"))

    def invoke_agent_with_prompt(
        self,
        prompt_body: str,
        context_blocks: Sequence[str],
    ) -> Optional[str]:
        """
        Send a prompt to the specified agent CLI and get a response.
        """
        payload_lines = [
            f"Regardless of the language of this prompt, you must respond in the language specified by this locale: {self.locale}.",
            "",
        ]

        if self.create_issue:
            payload_lines.extend([
                "AUTHORIZATION: You are authorized to create GitHub issues using `gh issue create` when you identify out-of-scope problems that require follow-up in separate PRs.",
                "",
            ])
        else:
            payload_lines.extend([
                "AUTHORIZATION: You are NOT authorized to create GitHub issues. Do not use `gh issue create` command.",
                "",
            ])

        payload_lines.append(prompt_body)
        for block in context_blocks:
            if block:
                payload_lines.append("")
                payload_lines.append("---")
                payload_lines.append("")
                payload_lines.append(block)
        payload = "\n".join(payload_lines)

        if self.agent not in self.AGENT_CONFIGS:
            raise AutolandError(_("Unknown agent: %s") % self.agent)

        agent_config = self.AGENT_CONFIGS[self.agent]
        command = [agent_config["command"]] + agent_config["args"]

        result = subprocess.run(
            command,
            input=payload,
            capture_output=True,
            text=True,
            check=True,
        )
        output = result.stdout.strip()
        self.logger.debug("agent stdout:\n%s", output)
        self.logger.debug("agent stderr:\n%s", result.stderr)

        return output

    def push_output_indicates_change(self, push_output: str) -> bool:
        """
        Determine if actual updates were made from git push --porcelain output.
        """
        change_flags = {" ", "+", "-", "*"}

        for raw_line in push_output.splitlines():
            if not raw_line.strip():
                continue

            flag = raw_line[0]
            if flag == "!":
                msg = _("git push was rejected") + ": %s"
                self.logger.error(msg, raw_line)
                raise AutolandError(_("git push was rejected"))
            if flag in change_flags:
                return True

        return False

    def push_if_needed(self) -> bool:
        """
        Push repository changes.

        Returns:
            bool: Whether push was actually performed
        """
        result = subprocess.run(
            ["git", "push", "--porcelain", "--force-with-lease"],
            capture_output=True,
            text=True,
            check=True
        )

        has_changes = self.push_output_indicates_change(result.stdout)

        return has_changes

    def gh_post_comment(self, pr_number: int, body: str) -> None:
        """
        Post a comment to the PR.
        """
        if not body or not body.strip():
            raise ValueError(f"Empty comment body for PR #{pr_number}")

        subprocess.run([
            self.GH_COMMAND,
            "pr",
            "comment",
            str(pr_number),
            "--body",
            body,
        ], check=True)
        self.log_pr(logging.INFO, pr_number, _("Posted report comment"))

    def format_pr_timeline(self, pr_data: Dict) -> str:
        """
        Format PR information chronologically (common for correction requests and merge decisions).

        Note: The output of this method is sent to coding agents, so
        strings are kept in English without translation.
        """
        if not pr_data:
            return ""

        lines = []
        authenticated_user = self.get_authenticated_user()

        # Basic PR information
        title = pr_data.get("title", "")
        body = pr_data.get("body", "")
        author = pr_data.get("author", {}).get("login", "unknown")
        created_at = pr_data.get("createdAt", "")

        lines.append(f"# {title}")
        lines.append(f"Author: {author} ({created_at})")

        mergeable = pr_data["mergeable"]
        if mergeable == "CONFLICTING":
            lines.append("ERROR: This branch has conflicts that must be resolved")

        lines.append("")
        if body:
            lines.append("## Description")
            lines.append(body)
            lines.append("")

        # Chronological events (comments + commits)
        timeline_items = []

        # Add comments
        comments = pr_data.get("comments", [])
        for comment in comments:
            if self.filter_comment(comment):
                comment_author = comment.get("author", {}).get("login", "unknown")
                comment_type = comment.get("type", "comment")

                timeline_items.append({
                    "type": comment_type,
                    "timestamp": comment.get("createdAt", ""),
                    "author": comment_author,
                    "content": comment.get("body", ""),
                    "path": comment.get("path"),
                    "line": comment.get("line")
                })

        # Add commits
        commits = pr_data.get("commits", [])
        for commit in commits:
            commit_sha = commit.get("oid", "")
            commit_message = commit.get("messageHeadline", "")

            timeline_items.append({
                "type": "commit",
                "timestamp": commit.get("committedDate", ""),
                "author": "",
                "content": f"{commit_sha[:8]} {commit_message}" if commit_sha else commit_message
            })

        # Sort chronologically
        timeline_items.sort(key=lambda x: x["timestamp"])

        if timeline_items:
            lines.append("## Timeline")
            for item in timeline_items:
                if item["type"] in ["comment", "issue_comment"]:
                    author_display = item["author"]
                    if authenticated_user and item["author"] == authenticated_user:
                        author_display += " (you)"
                    lines.append(f"### {item['timestamp']} - Comment by {author_display}")
                elif item["type"] == "review_comment":
                    author_display = item["author"]
                    if authenticated_user and item["author"] == authenticated_user:
                        author_display += " (you)"
                    path_line = f" ({item['path']}:{item['line']})" if item.get("path") and item.get("line") else ""
                    lines.append(f"### {item['timestamp']} - Review comment by {author_display}{path_line}")
                else:
                    lines.append(f"### {item['timestamp']} - Commit")
                lines.append(item["content"])
                lines.append("")

        return "\n".join(lines)

    def filter_comment(self, comment) -> bool:
        body = comment.get("body")
        if not body:
            return False

        if "This is an auto-generated comment: skip review by coderabbit.ai" in body:
            return False

        comment["body"] = self.LONG_HTML_COMMENT_PATTERN.sub('', body)
        return True

    def checkout_pr(self, pr_number: int) -> None:
        """
        Checkout the branch corresponding to the PR. Abort on failure.
        """
        self.log_pr(logging.INFO, pr_number, _("Checking out branch"))

        subprocess.run([
            self.GH_COMMAND,
            "pr",
            "checkout",
            str(pr_number)
        ], check=True, capture_output=True, text=True)

        self.log_pr(logging.INFO, pr_number, _("Checkout completed"))

    def merge_pr(self, pr_number: int) -> None:
        """
        Merge the PR using gh CLI.
        """
        subprocess.run([
            self.GH_COMMAND,
            "pr",
            "merge",
            str(pr_number),
            "--auto",
            "--squash",
        ], check=True)
        self.log_pr(logging.INFO, pr_number, _("Executed merge process"))
