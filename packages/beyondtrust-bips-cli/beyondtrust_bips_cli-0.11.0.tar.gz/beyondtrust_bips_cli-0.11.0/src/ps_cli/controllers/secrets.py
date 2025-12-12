import argparse

from secrets_safe_library import exceptions, folders, secrets_safe
from secrets_safe_library.constants.endpoints import (
    GET_SECRETS_SAFE_SECRETS,
    GET_SECRETS_SAFE_SECRETS_SECRETID,
    GET_SECRETS_SAFE_SECRETS_SECRETID_FILE,
    GET_SECRETS_SAFE_SECRETS_SECRETID_TEXT,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.secrets import fields as secret_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Secret(CLIController):
    """
    Works with Secrets Safe Secrets- Create, Update, Get, or Delete

    Requires Password Safe Secrets Safe License.
    Requires Password Safe SecretsSafe Read for Get, Read/Write for all others.

    For both "create" and "update" functionality, this tool will auto-detect
    if you have a 'file', 'text', 'password' or 'passwordrule' type of secret
    based on the options you pass:
        --path <path to existing file>
        --text '<multi-line text>'
        --newpassword <secret>
        --passwordrule <ruleid>
    and it will do the right thing.
    """

    def __init__(self):
        super().__init__(
            name="secrets",
            help="Secrets management commands",
        )

    _folder_object: folders.Folder = None

    @property
    def class_object(self) -> secrets_safe.SecretsSafe:
        if self._class_object is None and self.app is not None:
            self._class_object = secrets_safe.SecretsSafe(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @property
    def folder_object(self) -> folders.Folder:
        if self._folder_object is None and self.app is not None:
            self._folder_object = folders.Folder(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._folder_object

    @command
    @aliases("list")
    @option(
        "-p", "--path", help="The full path to the secret", type=str, required=False
    )
    @option(
        "-s",
        "--separator",
        help="The separator used in the path above. Default is /",
        type=str,
        required=False,
        default="/",
    )
    @option(
        "-t", "--title", help="The full title of the secret", type=str, required=False
    )
    @option(
        "-ad",
        "--afterdate",
        help="Filter by modified or created on, after, or equal to the given date. Must"
        "be in the following UTC format: yyyy-MM-ddTHH:mm:ssZ",
        type=str,
        required=False,
    )
    @option(
        "-l",
        "--limit",
        help="Limit the results. Default is 1000",
        type=int,
        required=False,
        default=1000,
    )
    @option(
        "-o",
        "--offset",
        help="Skip the first (offset) number of secrets",
        type=int,
        required=False,
    )
    def list_secrets(self, args):
        """
        Returns a list of secrets with the option to filter the list using provided
        options.
        """
        try:
            fields = self.get_fields(GET_SECRETS_SAFE_SECRETS, secret_fields)
            secrets = self.class_object.list_secrets(
                path=args.path,
                separator=args.separator,
                title=args.title,
                afterdate=args.afterdate,
                limit=args.limit,
                offset=args.offset,
            )
            self.display.show(secrets, fields)
            success_msg = "Secrets listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            print_it("It was not possible to list secrets")
            self.log.error(e)

    @command
    @aliases("get")
    @option(
        "-id",
        "--secret-id",
        help="Search by secret ID (GUID)",
        type=str,
        required=False,
        enforce_uuid=True,
    )
    @option(
        "-t",
        "--title",
        help="Search using exact secret title",
        type=str,
        required=False,
    )
    @option(
        "-p",
        "--path",
        help="Optional. The full path to the secret",
        type=str,
        required=False,
    )
    def get_secret(self, args):
        """
        Returns a secret by ID or Title.
        """
        try:
            if args.secret_id:
                fields = self.get_fields(
                    GET_SECRETS_SAFE_SECRETS_SECRETID, secret_fields
                )
                secret = self.class_object.get_secret_by_id(args.secret_id)
                self.display.show(secret, fields)
                success_msg = "Secret retrieved successfully"
                self.display.v(success_msg)
            elif args.title:
                secrets = self.class_object.list_secrets(
                    title=args.title,
                    path=args.path,
                )

                if secrets:
                    secret = secrets[0]
                    secret_type = secret.get("SecretType", "").lower()

                    match secret_type:
                        case "credential":
                            fields = self.get_fields(
                                GET_SECRETS_SAFE_SECRETS_SECRETID, secret_fields
                            )
                        case "text":
                            fields = self.get_fields(
                                GET_SECRETS_SAFE_SECRETS_SECRETID_TEXT, secret_fields
                            )
                        case "file":
                            fields = self.get_fields(
                                GET_SECRETS_SAFE_SECRETS_SECRETID_FILE, secret_fields
                            )
                        case _:
                            print_it(f"Unexpected secret type: {secret_type}")

                    self.display.show(secrets, fields)
                    success_msg = "Secrets retrieved successfully"
                    self.display.v(success_msg)
                else:
                    message = (
                        f"No secret was found for title: {args.title}"
                        f"{' and Path ' + args.path if args.path else ''}"
                    )
                    print_it(message)
                    self.log.warning(message)
            else:
                print_it("No secret ID or title was provided")
        except exceptions.LookupError as e:
            self.display.v(e)
            print_it(f"It was not possible to get a secret for ID: {args.secret_id}")
            self.log.error(e)

    @command
    @aliases("download")
    @option(
        "-id",
        "--secret-id",
        help="The secret ID (GUID)",
        type=str,
        required=True,
        enforce_uuid=True,
    )
    @option("-s", "--save-to-path", help="Save the file to this path", type=str)
    def download_secret_file(self, args):
        """
        Gets secret file as an attachment based on secretId.
        If save-to-path is provided, then the file will be saved in that location.
        """
        try:
            self.display.v("Trying to get file contents")
            secret_file = self.class_object.get_file_secret_data(args.secret_id)
            if args.save_to_path:
                self.display.v("Trying to write file to specified path")
                try:
                    with open(args.save_to_path, "wb") as f:
                        f.write(secret_file.encode("utf-8"))
                    success_msg = f"File saved to {args.save_to_path}"
                    print_it(success_msg)
                    self.log.info(success_msg)
                except IOError:
                    self.log.error(f"Could not write to {args.save_to_path}!")
            else:
                self.display.v("No path provided to save file, showing file")
                print_it(secret_file)
            success_msg = "File retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            print_it(
                f"It was not possible to get a secret file for ID: {args.secret_id}"
            )
            self.log.error(e)

    @command
    @aliases("create")
    @option(
        "-fid",
        "--folder-id",
        help=(
            "ID of the Folder where secret is being created (either folder ID or name "
            "is required)"
        ),
        type=str,
        enforce_uuid=True,
    )
    @option(
        "-fn",
        "--folder-name",
        help=(
            "Name of the Folder where secret is being created (either folder ID or "
            "name is required)"
        ),
        type=str,
    )
    @option(
        "-t", "--title", help="The full title of the secret", type=str, required=True
    )
    @option(
        "-d",
        "--description",
        help="Secret description",
        type=str,
        required=False,
        default="",
    )
    @option(
        "-u",
        "--username",
        help="Secret username",
        type=str,
        required=False,
    )
    @option("-p", "--password", help="Secret password", type=str, required=False)
    @option("--text", help="Secret text", type=str, required=False)
    @option("-fp", "--file-path", help="Secret file path", type=str, required=False)
    @option(
        "-ot",
        "--owner-type",
        help="The type of the owner [User|Group]",
        type=str,
        required=True,
        choices=["User", "Group"],
    )
    @option(
        "-o",
        "--owners",
        help="Space separated list of owner IDs",
        type=str,
        required=True,
        nargs="*",
    )
    @option(
        "-pri",
        "--password-rule-id",
        help="Password rule ID",
        type=int,
        required=False,
    )
    @option("-n", "--notes", help="Secret notes", type=str, required=False)
    @option(
        "--urls",
        help=(
            "Comma separated list of URLs in this format: "
            "'{'Id': GUID, 'CredentialId': GUID, 'Url': string}' for both request body "
            "V3.0 and V3.1"
        ),
        type=str,
        required=False,
        nargs="*",
    )
    def create_secret(self, args):
        """
        Creates a secret in the specified folder by ID (--folder-id) or folder name
        (--folder-name).
        """
        try:
            if args.folder_id:
                folder_id = args.folder_id
                self.display.v(f"folder_id was provided: {args.folder_id}")
            else:
                self.display.v(f"Searching folder by name {args.folder_name}")
                folders = self.folder_object.list_folders(folder_name=args.folder_name)
                if len(folders) == 1:
                    folder_id = folders[0]["Id"]
                    self.display.v(f"Found exactly 1 folder: {folder_id}")
                else:
                    print_it(
                        "Can't continue since multiple folders matched name "
                        f"{args.folder_name}"
                    )
                    return

            # User needs to provide username & password, text or file path
            if not any(
                [all([args.username, args.password]), args.text, args.file_path]
            ):
                print_it(
                    "Can't continue, since no username (--username) and password "
                    "(--password), text (--text) or file path (--file-path) was "
                    "provided"
                )
                return

            owners = self._format_owners_list(args.owners, args.owner_type)

            if owners is False:
                print_it(
                    "Can't create the secret, owners can only contain valid integer "
                    "values"
                )
                return

            self.display.v("Calling create_secret")
            secret = self.class_object.create_secret(
                title=args.title,
                folder_id=folder_id,
                description=args.description,
                username=args.username,
                password=args.password,
                text=args.text,
                file_path=args.file_path,
                owner_type=args.owner_type,
                owners=owners,
                password_rule_id=args.password_rule_id,
                notes=args.notes,
                urls=args.urls,
            )

            required_fields_key, _ = self._get_required_fields_key(args)

            fields = self.get_fields(required_fields_key, secret_fields)
            self.display.show(secret, fields)
            success_msg = "Secret created successfully"
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            print_it(e)
            print_it("It was not possible to create the secret")
            self.log.error(e)
        except FileNotFoundError as e:
            print_it(f"Requested file was not found {args.file_path}")
            self.display.v(e)
            self.log.error(e)

    @command
    @aliases("delete")
    @option(
        "-id",
        "--secret-id",
        help="Specific secret by ID (GUID), Optional.",
        type=str,
        enforce_uuid=True,
    )
    @option("-p", "--path", help="Secret path", type=str)
    @option("-t", "--title", help="Secret title, use it instead of secret ID", type=str)
    def delete_secret(self, args):
        """
        Deletes a Secrets Safe Secret by ID or using its path and title.
        """
        try:
            if args.secret_id:
                # Directly delete secret using its ID
                self.display.v(f"Deleting secret by ID {args.secret_id}")
                self.class_object.delete_secret_by_id(args.secret_id)
                print_it(f"Secret deleted successfully: {args.secret_id}")
            elif args.title:
                # Try to search by secret's title before deleting it
                self.display.v(f"Searching by title {args.title}")
                secrets = self.class_object.list_secrets(
                    path=args.path, title=args.title
                )
                secrets_len = len(secrets)
                self.display.v(f"Found {secrets_len} secrets")
                if secrets_len == 1:
                    self.display.v("Trying to delete the secret")
                    secret_id = secrets[0]["Id"]
                    self.class_object.delete_secret_by_id(secret_id)
                    self.log.info(f"Secret deleted {secret_id}")
                    print_it(f"Secret deleted successfully: {secret_id}")
                else:
                    message = f"No secret found for '{args.title}'"
                    print_it(message)
                    self.log.info(message)
            else:
                print_it("No secret ID or title was provided")
        except exceptions.DeletionError as e:
            self.display.v(e)
            if args.secret_id:
                print_it(
                    f"It was not possible to delete a secret for ID: {args.secret_id}"
                )
            elif args.title:
                print_it(
                    f"It was not possible to delete a secret with title: {args.title}"
                )

            print_it("Does secret exist and provided data is valid?")
            self.log.error(e)

    @command
    @aliases("update")
    @option(
        "-sid",
        "--secret-id",
        help=("GUID of the Secret to be updated"),
        required=True,
        type=str,
    )
    @option(
        "-fid",
        "--folder-id",
        help="ID of the Folder where secret is being updated",
        type=str,
    )
    @option(
        "-fn",
        "--folder-name",
        help=(
            "Name of the Folder where secret is being updated (either folder ID or "
            "name is required)"
        ),
        type=str,
    )
    @option(
        "-t", "--title", help="The full title of the secret", type=str, required=True
    )
    @option(
        "-d",
        "--description",
        help="Secret description",
        type=str,
        required=False,
        default="",
    )
    @option(
        "-u",
        "--username",
        help="Secret username",
        type=str,
        required=False,
    )
    @option("-p", "--password", help="Secret password", type=str, required=False)
    @option("--text", help="Secret text", type=str, required=False)
    @option("-fp", "--file-path", help="Secret file path", type=str, required=False)
    @option(
        "-ot",
        "--owner-type",
        help="The type of the owner [User|Group]",
        type=str,
        required=True,
        choices=["User", "Group"],
    )
    @option(
        "-o",
        "--owners",
        help="Space separated list of owner IDs",
        type=str,
        required=True,
        nargs="*",
    )
    @option(
        "-pri",
        "--password-rule-id",
        help="Password rule ID",
        type=int,
        required=False,
    )
    @option("-n", "--notes", help="Secret notes", type=str, required=False)
    @option(
        "--urls",
        help=(
            "Comma separated list of URLs in this format: "
            "'{'Id': GUID, 'CredentialId': GUID, 'Url': string}' for both request body "
            "V3.0 and V3.1"
        ),
        type=str,
        required=False,
        nargs="*",
    )
    def update_secret(self, args):
        """
        Updates a secret.
        """
        try:
            # User needs to provide username & password, text or file path
            if not any(
                [all([args.username, args.password]), args.text, args.file_path]
            ):
                print_it(
                    "Can't continue, since no username (--username) and password "
                    "(--password), text (--text) or file path (--file-path) was "
                    "provided"
                )
                return

            owners = self._format_owners_list(args.owners, args.owner_type)

            if owners is False:
                print_it(
                    "Can't update the secret, owners can only contain valid integer "
                    "values"
                )
                return

            # First confirm the secret exists
            try:
                secret_dict = self.class_object.get_secret_by_id(args.secret_id)
            except exceptions.LookupError:
                print_it("Secret not found")
                self.log.error(f"Secret ID {args.secret_id} was not found")
                return

            self.display.v("Calling update_secret")
            secret = self._call_update_secret(args, secret_dict, owners)

            required_fields_key, is_file = self._get_required_fields_key(args)
            fields = self.get_fields(required_fields_key, secret_fields)

            if not is_file:
                self.display.show(secret, fields)
            print_it("Secret updated successfully")
        except exceptions.UpdateError as e:
            print_it("It was not possible to update the secret")
            self.display.v(e)
            self.log.error(e)
        except FileNotFoundError as e:
            print_it(f"Requested file was not found: {args.file_path}")
            self.display.v(e)
            self.log.error(e)

    def _get_required_fields_key(self, args: argparse.Namespace):
        is_file = False
        if args.username:
            required_fields_key = GET_SECRETS_SAFE_SECRETS_SECRETID
            self.display.v("Showing a credential secret")
        elif args.text:
            required_fields_key = GET_SECRETS_SAFE_SECRETS_SECRETID_TEXT
            self.display.v("Showing a text secret")
        else:
            # Should be a file secret
            required_fields_key = GET_SECRETS_SAFE_SECRETS_SECRETID_FILE
            self.display.v("Showing a file secret")
            is_file = True

        return required_fields_key, is_file

    def _call_update_secret(
        self, args: argparse.Namespace, secret_dict: dict, owners: list
    ):
        # All arguments should be provided to avoid PUT request
        # to clean data by ommiting it
        secret = self.class_object.update_secret(
            secret_id=args.secret_id,
            title=args.title or secret_dict.get("Title"),
            folder_id=args.folder_id or secret_dict.get("FolderId"),
            description=args.description or secret_dict.get("Description"),
            username=args.username or secret_dict.get("Username"),
            password=args.password or secret_dict.get("Password"),
            text=args.text or secret_dict.get("Text"),
            file_path=args.file_path,
            owner_type=args.owner_type or secret_dict.get("OwnerType"),
            owners=owners or secret_dict.get("Owners"),
            password_rule_id=args.password_rule_id or secret_dict.get("PasswordRuleID"),
            notes=args.notes or secret_dict.get("Notes"),
            urls=args.urls or secret_dict.get("Urls"),
        )

        return secret

    def _format_owners_list(self, owners: list, owner_type: str) -> list:
        """
        Formats a list of owners based on the API version and owner type.

        This function processes a list of owner IDs and converts them into a list of
        dictionaries with appropriate keys based on the API version and owner type.
        For API version 3.0, the key is `owner_id`. For API version 3.1, the key is
        either `user_id` or `group_id`, depending on the `owner_type`.

        Args:
            owners (list): A list of owner IDs to be formatted.
            owner_type (str): The type of owner, either "User" or "Group".

        Returns:
            list: A list of dictionaries with formatted owner information.
            bool: Returns `False` if an exception occurs during conversion.

        Notes:
            - For API version 3.0, the key in the dictionary is `owner_id`.
            - For API version 3.1, the key is determined by `owner_type`:
            - `"User"` maps to `user_id`.
            - `"Group"` maps to `group_id`.
        """
        try:
            if self.app.api_version == Version.V3_0.value:
                owners = [{"owner_id": int(owner_id)} for owner_id in owners]
                self.display.v("Using API Version 3.0 for owners")
            else:
                # In version 3.1 instead of owner_id, either "group_id" or "user_id"
                # must be provided
                self.display.v("Using API Version 3.1 for owners")
                self.display.vv(f"Using {owner_type} owner_type")
                owner_type_key = "user_id" if owner_type == "User" else "group_id"
                owners = [{owner_type_key: int(owner_id)} for owner_id in owners]
            return owners
        except (ValueError, TypeError, OverflowError):
            return False
