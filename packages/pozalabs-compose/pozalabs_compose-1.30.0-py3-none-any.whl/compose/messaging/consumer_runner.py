import asyncio
import logging
import signal
import threading
import time
import types
from collections.abc import Callable

from .consumer import MessageConsumer
from .signal_handler import SignalHandler, ThreadSignalHandler

logger = logging.getLogger("compose")


class ThreadMessageConsumerRunner:
    def __init__(
        self,
        message_consumer_factory: Callable[[], MessageConsumer],
        signal_handler_factory: Callable[[], SignalHandler] = ThreadSignalHandler,
    ):
        self.message_consumer_factory = message_consumer_factory
        self.signal_handler_factory = signal_handler_factory

        self._received_signal = False
        self._consumers: list[MessageConsumer] = []

        for signum in (signal.SIGINT, signal.SIGTERM):
            signal.signal(signum, self.handle_signal)

    def run(self, num_workers: int = 1) -> None:
        threads = []

        for _ in range(num_workers):
            t = threading.Thread(target=self._run_in_thread)
            t.start()
            threads.append(t)

        while not self._received_signal:
            time.sleep(0.5)

        for consumer in self._consumers:
            consumer.shutdown()

        for t in threads:
            t.join()

    def _run_in_thread(self) -> None:
        with asyncio.Runner() as runner:
            runner.run(self._run_consumer())

    async def _run_consumer(self) -> None:
        message_consumer = self.message_consumer_factory()
        self._consumers.append(message_consumer)
        await message_consumer.run()

    def handle_signal(self, signum: int, _: types.FrameType) -> None:
        logger.info(f"Received {signal.Signals(signum).name}, exiting gracefully")
        self._received_signal = True
