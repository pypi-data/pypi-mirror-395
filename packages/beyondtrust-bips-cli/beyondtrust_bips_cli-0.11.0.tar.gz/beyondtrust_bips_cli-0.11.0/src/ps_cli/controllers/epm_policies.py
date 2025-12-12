from secrets_safe_library import epm_policies, exceptions

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class EPMPolicies(CLIController):
    """
    Beyond Insight EPM Policies functionality.
    Requires EPM Full Control, EPM Policy Full Control
    """

    def __init__(self):
        super().__init__(
            name="epm-policies",
            help="EPM Policies management commands",
        )

    @property
    def class_object(self) -> epm_policies.EPMPolicies:
        if self._class_object is None and self.app is not None:
            self._class_object = epm_policies.EPMPolicies(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("add-app")
    @option(
        "-p",
        "--policy-id",
        help="GUID of the policy to which the application will be added",
        type=str,
        enforce_uuid=True,
        required=True,
    )
    @option(
        "-g",
        "--group-name",
        help="Name of the group to which the application will be added",
        type=str,
        required=True,
    )
    @option(
        "-n",
        "--name",
        help="Name of the application to be added",
        type=str,
        required=True,
    )
    @option(
        "--path",
        help="Path to the application to be added",
        type=str,
        required=True,
    )
    @option(
        "--publisher",
        help="Publisher of the application to be added",
        type=str,
        required=True,
    )
    @option(
        "-c",
        "--children-inherit-token",
        help="If True, children of this application will inherit the token",
        action="store_true",
    )
    def add_application(self, args):
        """
        Edits a policy to add an application, and updates this policy in the
        BeyondInsight database. Touches the LastModifiedDate to indicate that a change
        is made. Updated policy is deployed to agents per the usual process in
        BeyondInsight.
        """
        try:
            self.display.v("Calling add_epm_application function")
            self.class_object.add_epm_application(
                policy_id=args.policy_id,
                group_name=args.group_name,
                name=args.name,
                path=args.path,
                publisher=args.publisher,
                children_inherit_token=args.children_inherit_token,
            )
            success_msg = "Application added successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to add the application to the policy")
