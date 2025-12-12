from secrets_safe_library import exceptions, users
from secrets_safe_library.constants.endpoints import (
    GET_USERS,
    GET_USERS_ID,
    GET_USERS_USERGROUPID,
    POST_USERS_AD,
    POST_USERS_APP,
    POST_USERS_BI,
    POST_USERS_LDAP,
    POST_USERS_QUARANTINE,
    POST_USERS_RECYCLE_CLIENT_SECRET,
    POST_USERS_USERGROUPID,
    PUT_USERS_ID_APP,
    PUT_USERS_ID_BI,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.users import fields as users_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class User(CLIController):
    """
    Works with Secrets Safe users - Create, Update, Get, or Delete

    Requires Password Safe Secrets Safe License.
    Requires Password Safe SecretsSafe Read for Get, Read/Write for all others.
    """

    def __init__(self):
        super().__init__(
            name="users",
            help="users management commands",
        )

    @property
    def class_object(self) -> users.User:
        if self._class_object is None and self.app is not None:
            self._class_object = users.User(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    @option(
        "-u",
        "--username",
        help="The User name",
        type=str,
        required=False,
    )
    @option(
        "-i",
        "--include-inactive",
        help="Include inactive users in the list",
        action="store_true",
    )
    def list_users(self, args):
        """
        Returns a list of users to which the current user has access.
        """
        try:
            fields = self.get_fields(GET_USERS, users_fields, Version.DEFAULT)
            self.display.v("Calling list_users function")
            users = self.class_object.get_users(
                username=args.username,
                include_inactive=args.include_inactive,
            )
            self.display.show(users, fields)
            success_msg = "Users listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list users")

    @command
    @aliases("get-by-id")
    @option(
        "-u-id",
        "--user-id",
        help="The User ID",
        type=int,
        required=True,
    )
    def get_user_by_id(self, args):
        """
        Returns a user by ID.
        """
        try:
            fields = self.get_fields(GET_USERS_ID, users_fields, Version.DEFAULT)
            self.display.v("Calling get_user_by_id function")
            user = self.class_object.get_user_by_id(user_id=args.user_id)
            self.display.show(user, fields)
            success_msg = "User retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"It was not possible to get user by ID: {args.user_id}")

    @command
    @aliases("get-by-user-group-id")
    @option(
        "-id",
        "--user-group-id",
        help="The User Group ID",
        type=int,
        required=True,
    )
    def get_users_by_user_group_id(self, args):
        """
        Returns a list of users by User Group ID.
        """
        try:
            fields = self.get_fields(
                GET_USERS_USERGROUPID, users_fields, Version.DEFAULT
            )
            self.display.v("Calling get_users_by_user_group_id function")
            users = self.class_object.get_users_by_usergroup_id(
                usergroup_id=args.user_group_id
            )
            self.display.show(users, fields)
            success_msg = "Users retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to get users by User Group ID: "
                f"{args.user_group_id}"
            )

    @command
    @aliases("create-user-bi")
    @option(
        "-n",
        "--user-name",
        help="The User name",
        type=str,
        required=True,
    )
    @option(
        "-fn",
        "--user-first-name",
        help="The User first name",
        type=str,
        required=True,
    )
    @option(
        "-u-l-na",
        "--user-last-name",
        help="The User last name",
        type=str,
        required=False,
        default=None,
    )
    @option(
        "-u-email",
        "--user-email",
        help="The User email",
        type=str,
        required=True,
    )
    @option(
        "-p",
        "--password",
        help="The User password",
        type=str,
        required=True,
    )
    def create_user_beyond_insight(self, args):
        """
        Creates a new user with UserType "BeyondInsight".
        """
        try:
            fields = self.get_fields(POST_USERS_BI, users_fields, Version.DEFAULT)
            self.display.v("Calling create_user_beyond_insight function")
            user = self.class_object.post_user_beyondinsight(
                user_name=args.user_name,
                first_name=args.user_first_name,
                last_name=args.user_last_name,
                email_address=args.user_email,
                password=args.password,
            )
            self.display.show(user, fields)
            success_msg = "User created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create user in Beyond Insight")

    @command
    @aliases("create-user-ad")
    @option(
        "-u-na",
        "--user-name",
        help="The User name",
        type=str,
        required=True,
    )
    @option(
        "-fo-na",
        "--forest-name",
        help="The Forest name",
        type=str,
        required=False,
    )
    @option(
        "-do-na",
        "--domain-name",
        help="The Domain name",
        type=str,
        required=False,
        default=None,
    )
    @option(
        "-b-user",
        "--bind-user",
        help="The Bind User name",
        type=str,
        required=False,
        default=None,
    )
    @option(
        "-b-pa",
        "--bind-password",
        help="The Bind Password",
        type=str,
        required=False,
        default=None,
    )
    @option(
        "-ssl",
        "--use-ssl",
        help="Use SSL",
        action="store_true",
    )
    def create_user_active_directory(self, args):
        """
        Creates a new user with UserType "ActiveDirectory".
        """
        try:
            fields = self.get_fields(POST_USERS_AD, users_fields, Version.DEFAULT)
            self.display.v("Calling create_user_active_directory function")
            user = self.class_object.post_user_active_directory(
                user_name=args.user_name,
                forest_name=args.forest_name,
                domain_name=args.domain_name,
                bind_user=args.bind_user,
                bind_password=args.bind_password,
                use_ssl=args.use_ssl,
            )
            self.display.show(user, fields)
            success_msg = "User created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create user in Active Directory")

    @command
    @aliases("create-ldap")
    @option(
        "-h-na",
        "--host-name",
        help="The Host name",
        type=str,
        required=True,
    )
    @option(
        "-d-na",
        "--distinguished-name",
        help="The Distinguished Name",
        type=str,
        required=True,
    )
    @option(
        "-a-na-attr",
        "--account-name-attribute",
        help="The LDAP account name attribute",
        type=str,
        required=True,
    )
    @option(
        "-b-user",
        "--bind-user",
        help="The Bind User name",
        type=str,
        required=False,
        default=None,
    )
    @option(
        "-b-pa",
        "--bind-password",
        help="The Bind Password",
        type=str,
        required=False,
        default=None,
    )
    @option(
        "-p",
        "--port",
        help="The Port number",
        type=int,
        required=False,
        default=None,
    )
    @option(
        "-ssl",
        "--use-ssl",
        help="Use SSL",
        action="store_true",
    )
    def create_user_ldap(self, args):
        """
        Creates a new user with UserType "LDAP".
        """
        try:
            fields = self.get_fields(POST_USERS_LDAP, users_fields, Version.DEFAULT)
            self.display.v("Calling create_user_ldap function")
            user = self.class_object.post_user_ldap(
                host_name=args.host_name,
                distinguished_name=args.distinguished_name,
                account_name_attribute=args.account_name_attribute,
                bind_user=args.bind_user,
                bind_password=args.bind_password,
                port=args.port,
                use_ssl=args.use_ssl,
            )
            self.display.show(user, fields)
            success_msg = "User created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create user in LDAP")

    @command
    @aliases("create-app")
    @option(
        "-u-na",
        "--user-name",
        help="The User name",
        type=str,
        required=True,
    )
    @option(
        "-acc-po",
        "--access-policy-id",
        help="The Access Policy ID",
        type=int,
        required=False,
        default=None,
    )
    def create_user_app(self, args):
        """
        Creates a new user with UserType "Application".
        """
        try:
            fields = self.get_fields(POST_USERS_APP, users_fields, Version.DEFAULT)
            self.display.v("Calling create_user_app function")
            user = self.class_object.post_user_application(
                user_name=args.user_name,
                access_policy_id=args.access_policy_id,
            )
            self.display.show(user, fields)
            success_msg = "User created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create user type Application")

    @command
    @aliases("quarantine")
    @option(
        "-u-id",
        "--user-id",
        help="The User ID",
        type=int,
        required=True,
    )
    def quarantine_user(self, args):
        """
        Quarantines a user by ID.
        """
        try:
            fields = self.get_fields(
                POST_USERS_QUARANTINE, users_fields, Version.DEFAULT
            )
            self.display.v("Calling quarantine_user function")
            user = self.class_object.post_user_quarantine(user_id=args.user_id)
            self.display.show(user, fields)
            success_msg = "User quarantined successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to quarantine user")

    @command
    @aliases("create-by-ug-id")
    @option(
        "-u-gr-id",
        "--user-group-id",
        help="The User Group ID",
        type=int,
        required=True,
    )
    @option(
        "-u-n",
        "--user-name",
        help="The User name",
        type=str,
        required=True,
    )
    @option(
        "-u-f-na",
        "--user-first-name",
        help="The User first name",
        type=str,
        required=True,
    )
    @option(
        "-u-l-na",
        "--user-last-name",
        help="The User last name",
        type=str,
        required=False,
        default=None,
    )
    @option(
        "-u-email",
        "--user-email",
        help="The User email",
        type=str,
        required=True,
    )
    @option(
        "-p",
        "--password",
        help="The User password",
        type=str,
        required=True,
    )
    def create_user_by_user_group_id(self, args):
        """
        Creates a new user by User Group ID.
        """
        try:
            fields = self.get_fields(
                POST_USERS_USERGROUPID, users_fields, Version.DEFAULT
            )
            self.display.v("Calling create_user_by_user_group_id function")
            user = self.class_object.post_user_usergroupid(
                user_group_id=args.user_group_id,
                user_name=args.user_name,
                first_name=args.user_first_name,
                last_name=args.user_last_name,
                email_address=args.user_email,
                password=args.password,
            )
            self.display.show(user, fields)
            success_msg = "User created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to create user by User Group ID: "
                f"{args.user_group_id}"
            )

    @command
    @aliases("recycle-secret")
    @option(
        "-u-id",
        "--user-id",
        help="The User ID",
        type=int,
        required=True,
    )
    def recycle_client_secret(self, args):
        """
        Recycles a client secret for a user by ID.
        """
        try:
            fields = self.get_fields(
                POST_USERS_RECYCLE_CLIENT_SECRET, users_fields, Version.DEFAULT
            )
            self.display.v("Calling recycle_client_secret function")
            user = self.class_object.post_user_recycleclient_secret(
                user_id=args.user_id
            )
            self.display.show(user, fields)
            success_msg = (
                f"Client secret recycled successfully for user ID {args.user_id}"
            )
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(
                "It was not possible to recycle client secret for user ID"
                f" {args.user_id}"
            )

    @command
    @aliases("update-user-bi")
    @option(
        "-u-id",
        "--user-id",
        help="The User ID",
        type=int,
        required=True,
    )
    @option(
        "-u-n",
        "--user-name",
        help="The User name",
        type=str,
        required=False,
        default=None,
    )
    @option(
        "-u-f-na",
        "--user-first-name",
        help="The User first name",
        type=str,
        required=False,
        default=None,
    )
    @option(
        "-u-l-na",
        "--user-last-name",
        help="The User last name",
        type=str,
        required=False,
        default=None,
    )
    @option(
        "-u-email",
        "--user-email",
        help="The User email",
        type=str,
        required=False,
        default=None,
    )
    @option(
        "-p",
        "--password",
        help="The User password",
        type=str,
        required=True,
    )
    def update_user_beyond_insight(self, args):
        """
        Updates a user with UserType "BeyondInsight".
        """
        try:
            get_user = self.class_object.get_user_by_id(user_id=args.user_id)
            if not get_user:
                print_it(f"User with ID {args.user_id} was not found")
                return

            fields = self.get_fields(PUT_USERS_ID_BI, users_fields, Version.DEFAULT)
            self.display.v("Calling update_user_beyond_insight function")
            user = self.class_object.put_user_beyondinsight(
                user_id=args.user_id,
                user_name=(
                    args.user_name
                    if args.user_name is not None
                    else get_user["UserName"]
                ),
                first_name=(
                    args.user_first_name
                    if args.user_first_name is not None
                    else get_user["FirstName"]
                ),
                last_name=(
                    args.user_last_name
                    if args.user_last_name is not None
                    else get_user["LastName"]
                ),
                email_address=(
                    args.user_email
                    if args.user_email is not None
                    else get_user["EmailAddress"]
                ),
                password=args.password,
            )
            self.display.show(user, fields)
            success_msg = "User updated successfully"
            self.display.v(success_msg)
        except exceptions.UpdateError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to update user in Beyond Insight")

    @command
    @aliases("update-user-app")
    @option(
        "-u-id",
        "--user-id",
        help="The User ID",
        type=int,
        required=True,
    )
    @option(
        "-u-na",
        "--user-name",
        help="The User name",
        type=str,
        required=True,
    )
    @option(
        "-acc-po",
        "--access-policy-id",
        help="The Access Policy ID",
        type=int,
        required=False,
        default=None,
    )
    def update_user_application(self, args):
        """
        Updates a user with UserType "Application".
        """
        try:
            get_user = self.class_object.get_user_by_id(user_id=args.user_id)
            if not get_user:
                print_it(f"User with ID {args.user_id} was not found")
                return
            if not get_user["AccessPolicyID"]:
                print_it("User is not of type Application")
                return

            fields = self.get_fields(PUT_USERS_ID_APP, users_fields, Version.DEFAULT)
            self.display.v("Calling update_user_application function")
            user = self.class_object.put_user_application(
                user_id=args.user_id,
                user_name=args.user_name,
                access_policy_id=(
                    args.access_policy_id
                    if args.access_policy_id is not None
                    else get_user["AccessPolicyID"]
                ),
            )
            self.display.show(user, fields)
            success_msg = "User updated successfully"
            self.display.v(success_msg)
        except exceptions.UpdateError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to update user type Application")

    @command
    @aliases("delete")
    @option(
        "-u-id",
        "--user-id",
        help="The User ID",
        type=int,
        required=True,
    )
    def delete_user(self, args):
        """
        Deletes a user by ID.
        """
        try:
            self.display.v("Calling delete_user function")
            self.class_object.delete_user(user_id=args.user_id)
            success_msg = f"User with ID {args.user_id} was deleted successfully"
            print_it(success_msg)
            self.display.v(success_msg)
        except exceptions.DeletionError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"It was not possible to delete user with ID: {args.user_id}")
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"User with ID {args.user_id} was not found")
