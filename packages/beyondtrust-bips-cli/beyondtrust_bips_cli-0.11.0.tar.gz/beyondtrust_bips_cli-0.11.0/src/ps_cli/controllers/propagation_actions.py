from secrets_safe_library import exceptions, propagation_actions
from secrets_safe_library.constants.endpoints import (
    GET_MANAGED_ACCOUNTS_PROPAGATION_ACTIONS,
    GET_PROPAGATION_ACTIONS,
    GET_PROPAGATION_ACTIONS_ID,
    POST_MANAGED_ACCOUNT_PROPAGATION_ACTIONS,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.propagation_actions import (
    fields as propagation_actions_fields,
)

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class PropagationActions(CLIController):
    """
    Controller for managing Propagation Actions.

    Requires Password Safe Secrets Safe License.
    Requires Password Safe SecretsSafe Read for Get, Read/Write for all others.
    """

    def __init__(self) -> None:
        super().__init__(
            name="propagation-actions",
            help="Propagation Actions management commands",
        )

    @property
    def class_object(self) -> propagation_actions.PropagationActions:
        if self._class_object is None and self.app is not None:
            self._class_object = propagation_actions.PropagationActions(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_propagation_actions(self, args):
        """
        Lists all Propagation Actions.
        """
        try:
            fields = self.get_fields(
                GET_PROPAGATION_ACTIONS,
                propagation_actions_fields,
                Version.DEFAULT,
            )
            self.display.v("Calling list_propagation_actions function")
            actions = self.class_object.list()
            self.display.show(actions, fields)
            success_msg = "Propagation Actions listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list Propagation Actions")

    @command
    @aliases("get")
    @option(
        "-id",
        "--action-id",
        help="To get a propagation action by ID",
        type=int,
        required=True,
    )
    def get_propagation_action_by_id(self, args):
        """
        Gets a Propagation Action by ID.
        """
        try:
            fields = self.get_fields(
                GET_PROPAGATION_ACTIONS_ID,
                propagation_actions_fields,
                Version.DEFAULT,
            )
            self.display.v("Calling get_propagation_action_by_id function")
            action = self.class_object.get_by_id(object_id=args.action_id)
            self.display.show(action, fields)
            success_msg = (
                f"Propagation Action with ID {args.action_id} retrieved successfully"
            )
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to get the Propagation Action by "
                f"ID: {args.action_id}"
            )

    @command
    @aliases("get-by-managed-account")
    @option(
        "-id",
        "--managed-account-id",
        help="To get a propagation action by Managed Account ID",
        type=int,
        required=True,
    )
    def get_propagation_action_by_managed_account_id(self, args):
        """
        Gets a Propagation Action by Managed Account ID.
        """
        try:
            fields = self.get_fields(
                GET_MANAGED_ACCOUNTS_PROPAGATION_ACTIONS,
                propagation_actions_fields,
                Version.DEFAULT,
            )
            self.display.v(
                "Calling get_propagation_action_by_managed_account_id function"
            )
            actions = self.class_object.get_managed_account_propagation_actions(
                managed_account_id=args.managed_account_id
            )
            self.display.show(actions, fields)
            success_msg = (
                f"Propagation Actions for Managed Account ID "
                f"{args.managed_account_id} retrieved successfully"
            )
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to get the Propagation Action by "
                f"Managed Account ID: {args.managed_account_id}"
            )

    @command
    @aliases("post-to-managed-account")
    @option(
        "-id",
        "--managed-account-id",
        help="To post a propagation action to a Managed Account by ID",
        type=int,
        required=True,
    )
    @option(
        "-pa",
        "--propagation-action-id",
        help="The ID of the Propagation Action to associate with the Managed Account.",
        type=int,
        required=True,
    )
    @option(
        "-s-r-id",
        "--smart-rule-id",
        help="The ID of the Smart Rule to associate with the Propagation Action.",
        type=int,
        required=False,
    )
    def post_propagation_action_to_managed_account(self, args):
        """
        Assigns a propagation action to the managed account referenced by ID.
        """
        try:
            fields = self.get_fields(
                POST_MANAGED_ACCOUNT_PROPAGATION_ACTIONS,
                propagation_actions_fields,
                Version.DEFAULT,
            )
            self.display.v(
                "Calling post_propagation_action_to_managed_account function"
            )
            action = self.class_object.post_managed_account_propagation_action_by_id(
                managed_account_id=args.managed_account_id,
                propagation_action_id=args.propagation_action_id,
                smart_rule_id=args.smart_rule_id,
            )
            self.display.show(action, fields)
            success_msg = (
                f"Propagation Action successfully posted to the "
                f"Managed Account ID: {args.managed_account_id}"
            )
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to post the Propagation Action to the "
                f"Managed Account ID: {args.managed_account_id}"
            )

    @command
    @aliases("delete-from-managed-account")
    @option(
        "-id",
        "--managed-account-id",
        help="To delete a propagation action from a Managed Account by ID",
        type=int,
        required=True,
    )
    def delete_propagation_action_from_managed_account(self, args):
        """
        Unassigns all propagation actions from the managed account by ID.
        """
        try:
            self.display.v(
                "Calling delete_propagation_action_from_managed_account function"
            )
            self.class_object.delete_managed_account_propagation_action(
                managed_account_id=args.managed_account_id,
            )
            success_msg = (
                "Propagation Actions successfully deleted from the "
                f"Managed Account ID: {args.managed_account_id}"
            )
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to delete the Propagation Actions from the "
                f"Managed Account ID: {args.managed_account_id}"
            )

    @command
    @aliases("delete-from-managed-account-by-action-id")
    @option(
        "-id",
        "--managed-account-id",
        help="To delete a propagation action from a Managed Account by ID",
        type=int,
        required=True,
    )
    @option(
        "-pa",
        "--propagation-action-id",
        help="The ID of the Propagation Action to delete from the Managed Account.",
        type=int,
        required=True,
    )
    def delete_propagation_action_from_managed_account_by_action_id(self, args):
        """
        Unassigns a propagation action from the managed account by ID.
        """
        try:
            self.display.v(
                "Calling delete_propagation_action_from_managed_account_by_action_id "
                "function"
            )
            self.class_object.delete_managed_account_propagation_action_by_id(
                managed_account_id=args.managed_account_id,
                propagation_action_id=args.propagation_action_id,
            )
            success_msg = (
                "Propagation Action successfully deleted from the "
                f"Managed Account ID: {args.managed_account_id}"
            )
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to delete the Propagation Action from the "
                f"Managed Account ID: {args.managed_account_id}"
            )
