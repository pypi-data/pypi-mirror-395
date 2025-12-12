import asyncio
import logging

from pydantic import EmailStr

from async_temp_email._core._interfaces import Service
from async_temp_email._core._schemas import Message

log = logging.getLogger(__name__)


class EmailnatorPolling:
    def __init__(self, service: Service):
        self._service = service

        self._email: EmailStr | None = None
        self._poll_interval: float = 10.0
        self._skip_existing: bool = True

        self._queue: asyncio.Queue[Message] = asyncio.Queue()
        self._closed: bool = False
        self._task: asyncio.Task | None = None
        self._old_messages: set[str] = set()

    async def _poll_api(self) -> None:
        first_run = True
        log.info(
            'Started polling for %s (interval=%.1fs, skip_existing=%s)',
            self._email,
            self._poll_interval,
            self._skip_existing,
        )

        try:
            while not self._closed:
                try:
                    messages = await self._service.get_messages(self._email)
                except Exception as exc:
                    log.error('Error while polling messages for %s: %s', self._email, exc, exc_info=True)
                    await asyncio.sleep(self._poll_interval)
                    continue

                new_count = 0
                for message in messages:
                    msg_id = message.message_id
                    if msg_id in self._old_messages:
                        continue

                    self._old_messages.add(msg_id)

                    if first_run and self._skip_existing:
                        continue

                    await self._queue.put(message)
                    new_count += 1

                if new_count:
                    log.info('Delivered %d new message(s) for %s', new_count, self._email)

                first_run = False
                await asyncio.sleep(self._poll_interval)

        except asyncio.CancelledError:
            log.debug('Polling task cancelled for %s', self._email)
        except Exception:
            log.exception('Unexpected error in polling loop for %s', self._email)

    async def __aenter__(self) -> 'EmailnatorPolling':
        if self._email is None:
            raise RuntimeError('Polling must be configured with .__call__(email=...) before entering context')
        self._closed = False
        self._task = asyncio.create_task(self._poll_api())
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        log.info('Stopping polling for %s', self._email)
        self._closed = True
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass

    def __aiter__(self) -> 'EmailnatorPolling':
        return self

    async def __anext__(self) -> Message:
        if self._closed and self._queue.empty():
            raise StopAsyncIteration
        return await self._queue.get()

    def __call__(
        self,
        *,
        email: EmailStr,
        poll_interval: float = 10.0,
        skip_existing: bool = True,
    ) -> 'EmailnatorPolling':
        log.debug('Configuring polling: email=%s, interval=%.1f, skip_existing=%s', email, poll_interval, skip_existing)
        self._email = email
        self._poll_interval = poll_interval
        self._skip_existing = skip_existing
        self._old_messages.clear()

        # clear queue from previous runs
        while not self._queue.empty():
            try:
                self._queue.get_nowait()
            except asyncio.QueueEmpty:
                break

        return self
