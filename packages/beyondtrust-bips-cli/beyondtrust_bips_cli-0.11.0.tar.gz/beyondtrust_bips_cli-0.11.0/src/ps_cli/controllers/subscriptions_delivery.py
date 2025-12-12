from secrets_safe_library import exceptions, subscription_delivery
from secrets_safe_library.constants.endpoints import (
    POST_SUBSCRIPTIONS_DELIVERY_DOWNLOAD,
)
from secrets_safe_library.constants.versions import Version
from secrets_safe_library.mapping.smart_rules import fields as subscription_fields

from ps_cli.core.controllers import CLIController
from ps_cli.core.decorators import aliases, command, option
from ps_cli.core.display import print_it


class SubscriptionDelivery(CLIController):
    """
    Beyond Insight Subscription Delivery functionality.
    """

    def __init__(self):
        super().__init__(
            name="subscriptions-delivery",
            help="Subscriptions delivery management commands",
        )

    @property
    def class_object(self) -> subscription_delivery.SubscriptionDelivery:
        if self._class_object is None and self.app is not None:
            self._class_object = subscription_delivery.SubscriptionDelivery(
                authentication=self.app.authentication, logger=self.log.logger
            )
        return self._class_object

    @command
    @aliases("list")
    def list_subscriptions(self, args):
        """
        Returns a list of IDs for all subscription deliveries that a user has access to.
        Administrators have access to all deliveries while other users only have access
        to deliveries they created.
        """
        try:
            self.display.v("Calling list function")
            subscriptions = self.class_object.list()
            self.display.show(subscriptions)
            success_msg = "Subscriptions deliveries listed successfully"
            self.display.v(success_msg)
        except exceptions.LookupError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to list subscriptions deliveries")

    @command
    @aliases("download")
    @option(
        "-id",
        "--request-id",
        help="ID of the request for which to retrieve the subscription delivery",
        type=int,
        required=True,
    )
    def download_subscription(self, args):
        """
        Returns the subscription delivery for the requested id.
        """
        try:
            self.display.v("Calling download function")

            subscription = self.class_object.download(
                request_id=args.request_id,
            )
            fields = self.get_fields(
                POST_SUBSCRIPTIONS_DELIVERY_DOWNLOAD,
                subscription_fields,
                Version.DEFAULT,
            )
            self.display.show(subscription, fields)
            success_msg = (
                "Subscription delivery with request ID "
                f"{args.request_id} retrieved successfully"
            )
            self.display.v(success_msg)
        except exceptions.CreationError as e:
            self.display.v(e)
            self.log.error(e)
            print_it("It was not possible to retrieve the subscription delivery")
