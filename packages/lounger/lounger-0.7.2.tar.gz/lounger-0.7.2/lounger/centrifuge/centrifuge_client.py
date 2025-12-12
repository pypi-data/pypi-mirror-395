import pytest
from centrifuge import (
    Client,
    ClientEventHandler,
    DisconnectedContext,
    ErrorContext,
    PublicationContext,
    SubscribedContext,
    SubscriptionErrorContext,
    SubscriptionEventHandler,
)

from lounger.log import log


class CentrifugeClient(Client):
    """
    Extend centrifuge.Client to support custom headers in the connect command.
    The original SDK does not include headers in the initial connect payload,
    so we override _construct_connect_command to inject them.
    """

    def _construct_connect_command(self, cmd_id: int):
        connect = {}

        if self._token:
            connect["token"] = self._token

        if self._data:
            connect["data"] = self._encode_data(self._data)

        if self._name:
            connect["name"] = self._name

        if self._version:
            connect["version"] = self._version

        if self._headers:
            connect["headers"] = self._headers

        subs = {}
        for channel, sub in self._server_subs.items():
            if sub.recoverable:
                subs[channel] = {
                    "recover": True,
                    "offset": sub.offset,
                    "epoch": sub.epoch,
                }
        if subs:
            connect["subs"] = subs

        command = {
            "id": cmd_id,
            "connect": connect,
        }
        return command


# Event handlers (copied from official docs)
class ClientEventLoggerHandler(ClientEventHandler):

    async def on_error(self, ctx: ErrorContext) -> None:
        pytest.fail(f"❌ WebSocket case execution failed: {ctx}")


class SubscriptionEventLoggerHandler(SubscriptionEventHandler):

    async def on_subscribed(self, ctx: SubscribedContext) -> None:
        log.info(f"📌 Subscribed to {ctx.channel}")

    async def on_publication(self, ctx: PublicationContext) -> None:
        log.info(f"📥 Received message: {ctx.pub.data}")

    async def on_error(self, ctx: SubscriptionErrorContext) -> None:
        log.info(f"❌ Subscription error: {ctx}")

    async def on_disconnected(self, ctx: DisconnectedContext):
        log.info(f"🚪 Disconnected! code={ctx.code}, reason={ctx.reason}")
