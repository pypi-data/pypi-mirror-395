# -*- coding: utf-8 -*-
import re
import sys
import requests

from suite_py.lib import logger, metrics
from suite_py.lib.handler import prompt_utils
from suite_py.lib.handler.git_handler import GitHandler, is_branch_name_valid
from suite_py.lib.handler.youtrack_handler import YoutrackHandler


class CreateBranch:
    def __init__(
        self,
        config,
        git_handler: GitHandler,
        youtrack_handler: YoutrackHandler,
    ):
        self._config = config
        self._git_handler = git_handler
        self._youtrack_handler = youtrack_handler

    @metrics.command("create-branch")
    def run(
        self,
        autostash=False,
        branch_name=None,
        card_id=None,
        parent_branch=None,
    ):
        if (
            not self._git_handler.is_detached()
            and self._git_handler.is_dirty()
            and not autostash
        ):
            # Default behaviour is to pull when not detached.
            # Can't do that with uncommitted changes.
            logger.error("You have some uncommitted changes, I can't continue")
            sys.exit(-1)

        try:
            if card_id:
                issue = self._youtrack_handler.get_issue(card_id)
            else:
                issue = self._youtrack_handler.get_issue(self._ask_card_id())
        except Exception:
            logger.error(
                "There was a problem retrieving the issue from YouTrack. Check that the issue number is correct"
            )
            sys.exit(-1)

        self._checkout_branch(issue, autostash, parent_branch, branch_name)

        user = self._youtrack_handler.get_current_user()
        self._youtrack_handler.assign_to(issue["id"], user["login"])

        try:
            self._youtrack_handler.update_state(
                issue["id"], self._config.youtrack["picked_state"]
            )
        except requests.exceptions.HTTPError:
            logger.error(
                "There was a problem moving the issue to the 'picked state' on YouTrack"
            )
            logger.error(
                f"Does your YouTrack board have a state called '{self._config.youtrack['picked_state']}'?"
            )
            sys.exit(-1)

    def _select_card(self, suggestions):
        choices = ["Other..."] + [
            f"{s['idReadable']} {s['summary']}" for s in suggestions
        ]
        selected = prompt_utils.ask_choices(
            "What YouTrack issue do you want to work on?", choices, "Other..."
        )

        return (
            self._prompt_custom_card()
            if selected == "Other..."
            else selected.split(" ")[0]
        )

    def _prompt_custom_card(self):
        return prompt_utils.ask_questions_input(
            "Insert the YouTrack issue number:", self._config.user["default_slug"]
        )

    def _ask_card_id(self):
        suggestions = self._get_card_suggestions()
        user_choice = (
            self._select_card(suggestions)
            if suggestions
            else self._prompt_custom_card()
        )
        return user_choice

    def _get_card_suggestions(self):
        try:
            return self._youtrack_handler.search_issues(
                self._config.user["card_suggest_query"],
                self._config.user["card_suggestions_limit"],
            )
        except Exception:
            logger.warning(
                "No card suggestions (have you set card_suggest_query in your config? Query syntax: https://www.jetbrains.com/help/youtrack/server/Search-and-Command-Attributes.html)"
            )
            return []

    def _checkout_branch(
        self, issue, autostash=False, parent_branch=None, branch_name_template=None
    ):
        default_parent_branch_name = self._config.user.get(
            "default_parent_branch", self._git_handler.current_branch_name()
        )

        parent_branch_name = parent_branch or prompt_utils.ask_questions_input(
            "Enter parent branch: ", default_parent_branch_name
        )

        full_branch_name = ""
        branch_name = _normalize_git_ref_segment(issue["summary"])
        branch_type = _normalize_git_ref_segment(issue["Type"])

        if branch_name_template:
            # Use the template and replace placeholders
            full_branch_name = branch_name_template.format(
                card_id=issue["idReadable"], type=branch_type, summary=branch_name
            )

            if not is_branch_name_valid(full_branch_name):
                logger.error(f"Invalid branch name from template: {full_branch_name}")
                sys.exit(-1)
        else:
            while True:
                branch_name = str(
                    prompt_utils.ask_questions_input("Enter branch name: ", branch_name)
                )

                full_branch_name = f"{issue['idReadable']}/{branch_type}/{branch_name}"
                if is_branch_name_valid(full_branch_name):
                    break

                logger.error(f"Invalid branch name: {full_branch_name}. Try again?")

        self._git_handler.checkout(parent_branch_name, autostash=autostash)

        self._git_handler.checkout(full_branch_name, new=True, autostash=autostash)


# Normalize a string into a valid segment(ie. the part of the branch name between the /)
def _normalize_git_ref_segment(summary):
    return re.sub(r"[^A-Za-z0-9]+", "-", summary).lower().strip("-")
