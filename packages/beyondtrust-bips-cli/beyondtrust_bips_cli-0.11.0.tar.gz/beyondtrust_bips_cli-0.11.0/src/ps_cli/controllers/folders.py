from secrets_safe_library import exceptions, folders
from secrets_safe_library.constants.endpoints import (
    GET_SECRETS_SAFE_FOLDERS,
    GET_SECRETS_SAFE_FOLDERS_FOLDERID,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.folders import fields as folder_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class Folder(CLIController):
    """
    Works with Secrets Safe Folders - Create, Update, Get, or Delete

    Requires Password Safe Secrets Safe License.
    Requires Password Safe SecretsSafe Read for Get, Read/Write for all others.
    """

    def __init__(self):
        super().__init__(
            name="folders",
            help="Folders management commands",
        )

    @property
    def class_object(self) -> folders.Folder:
        if self._class_object is None and self.app is not None:
            self._class_object = folders.Folder(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    @option(
        "-n", "--name", help="The partial name of the folder", type=str, required=False
    )
    @option("-p", "--path", help="The folder path", type=str, required=False)
    @option(
        "-s",
        "--include-subfolders",
        help="Indicate whether to include the subfolder",
        action="store_true",
    )
    @option(
        "-ro",
        "--root-only",
        help="The results only include those folders at the root level",
        action="store_true",
    )
    @option(
        "-oi",
        "--owner-id",
        help="Filter results by the folders which are owned by the given owner ID",
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
        help="Skip the first (offset) number of folders",
        type=int,
        required=False,
    )
    def list_folders(self, args):
        """
        Returns a list of Secrets Safe folders to which the current user has access.
        """
        try:
            fields = self.get_fields(
                GET_SECRETS_SAFE_FOLDERS, folder_fields, Version.DEFAULT
            )
            self.display.v("Calling list_folders function")
            folders = self.class_object.list_folders(
                folder_name=args.name,
                folder_path=args.path,
                include_subfolders=args.include_subfolders,
                root_only=args.root_only,
                folder_owner_id=args.owner_id,
                limit=args.limit,
                offset=args.offset,
            )
            self.display.show(folders, fields)
            success_msg = "Folders listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list folders")

    @command
    @aliases("get")
    @option(
        "-id",
        "--folder-id",
        help="To get a folder by ID (GUID)",
        type=str,
        enforce_uuid=True,
    )
    @option(
        "-n",
        "--folder-name",
        help="To get a folder by name, if several folders match the name, then a list"
        "is returned",
        type=str,
    )
    def get_folder(self, args):
        """
        Returns a Secrets Safe folder by ID or folder name.
        """
        try:
            fields = self.get_fields(
                GET_SECRETS_SAFE_FOLDERS_FOLDERID, folder_fields, Version.DEFAULT
            )
            if args.folder_id:
                # Directly get folder information using its ID
                self.display.v(f"Searching by ID {args.folder_id}")
                folder = self.class_object.get_by_id(args.folder_id)
                self.display.show(folder, fields)
            elif args.folder_name:
                # Try to search by folder name
                self.display.v(f"Searching by name {args.folder_name}")
                folders = self.class_object.list_folders(folder_name=args.folder_name)
                if len(folders) == 1:
                    self.display.show(folders[0], fields)
                else:
                    self.display.show(folders, fields)
            else:
                print_it("No folder ID or name was provided")
                return
            success_msg = "Folder retrieved successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it(f"It was not possible to get a folder for ID: {args.folder_id}")

    @command
    @aliases("create")
    @option("-n", "--name", help="The name of the folder", type=str, required=True)
    @option(
        "-d",
        "--description",
        help="The description of the folder",
        type=str,
        required=False,
    )
    @option(
        "-pid",
        "--parent-id",
        help="The parent folder/safe ID (GUID)",
        type=str,
        required=False,
        enforce_uuid=True,
    )
    @option(
        "-pn",
        "--parent-name",
        help="The parent folder name, used if no Parent ID is provided",
        type=str,
        required=False,
    )
    @option("-uid", "--user-group-id", help="User/group ID", type=int, required=False)
    def create_folder(self, args):
        """
        Creates a new Secrets Safe folder for the given user group.
        """
        try:
            self.display.v("Calling create_folder function")
            parent_id = args.parent_id

            if not parent_id and not args.parent_name:
                print_it("Please provider either Parent ID (-pid) or Name (-pn)")
                return

            if args.parent_name and not args.parent_id:
                self.display.v(f"Searching parent folder by name {args.parent_name}")
                folders = self.class_object.list_folders(folder_name=args.parent_name)
                if len(folders) == 1:
                    self.display.v(
                        f"Found exactly 1 folder matching {args.parent_name}"
                    )
                    parent_id = folders[0]["Id"]
                else:
                    print_it("Multiple folders match provided parent name:")
                    self.display.show(folders)
                    print_it("Cannot continue with folder creation")
                    return

            folder = self.class_object.create_folder(
                name=args.name,
                parent_id=parent_id,
                description=args.description,
                user_group_id=args.user_group_id,
            )
            self.display.show(folder)
            success_msg = "Folder created successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to find the parent folder")
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to create the folder")

    @command
    @aliases("delete")
    @option(
        "-id",
        "--folder-id",
        help="To delete a folder by ID (GUID)",
        type=str,
        enforce_uuid=True,
    )
    @option(
        "-n",
        "--folder-name",
        help="To delete a folder by name, if several folders match the name, then a "
        "operation cannot be completed",
        type=str,
    )
    def delete_folder(self, args):
        """
        Deletes a Secrets Safe folder by ID or folder name.
        """
        try:
            if args.folder_id:
                # Directly delete folder using its ID
                self.display.v(f"Deleting folder by ID {args.folder_id}")
                self.class_object.delete_by_id(args.folder_id, expected_status_code=200)
                self.display.v(f"Folder deleted successfully {args.folder_id}")
            elif args.folder_name:
                # Try to search by folder name before deleting it
                self.display.v(f"Searching by name {args.folder_name}")
                folders = self.class_object.list_folders(folder_name=args.folder_name)
                folders_len = len(folders)
                self.display.v(f"Found {folders_len} folders")
                if folders_len == 1:
                    self.display.v(f"Found a single folder matching {args.folder_name}")
                    self.display.v("Trying to delete the folder")
                    self.class_object.delete_by_id(
                        folder_id=folders[0]["Id"], expected_status_code=200
                    )
                    self.display.v(f"Folder deleted successfully {args.folder_name}")
                elif folders_len > 1:
                    print_it(
                        f"Multiple folders match provided name: {args.folder_name}"
                    )
                    self.display.show(folders)
                    print_it("Cannot continue with folder deletion")
                    return
                else:
                    print_it(f"No folder found for '{args.folder_name}'")
                    return
            else:
                print_it("No folder ID or name was provided")
        except exceptions.DeletionError as e:
            self.display.v(e)
            if args.folder_id:
                print_it(
                    f"It was not possible to delete a folder for ID: {args.folder_id}"
                )
            print_it("Does folder exist and provided ID is valid?")
            self.log.error(e)
