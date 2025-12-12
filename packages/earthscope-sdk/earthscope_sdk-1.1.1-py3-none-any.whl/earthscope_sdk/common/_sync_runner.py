import abc
import asyncio
import functools
import sys
from typing import Any, Callable, Coroutine, TypeVar

if sys.version_info >= (3, 10):
    from typing import ParamSpec
else:
    from typing_extensions import ParamSpec

T_Retval = TypeVar("T_Retval")
T_ParamSpec = ParamSpec("T_ParamSpec")


class SyncRunner(abc.ABC):
    """
    Facilitates running async functions in a synchronous manner
    """

    @property
    def is_closed(self) -> bool:
        """
        The async runner is closed and no more synchronous invocations may occur.
        """
        return False

    @abc.abstractmethod
    def stop(self):
        """
        Stop the async runner (i.e. clean up any allocated resources).

        Methods created via `.syncify()` may not work after stopping this runner.
        """

    @abc.abstractmethod
    def syncify(
        self,
        async_function: Callable[T_ParamSpec, Coroutine[Any, Any, T_Retval]],
    ) -> Callable[T_ParamSpec, T_Retval]:
        """
        Create a synchronous version of an async function
        """


class SimpleSyncRunner(SyncRunner):
    """
    Runs async functions in a dedicated event loop in the same thread as the caller.

    This is a simple light-weight option, but does not work when an EventLoop already
    exists in the calling thread.
    """

    def __init__(self):
        self._loop = asyncio.new_event_loop()

    @property
    def is_closed(self):
        return self._loop.is_closed()

    def stop(self):
        # implements abstract method
        self._loop.stop()
        self._loop.close()

    def syncify(
        self,
        async_function: Callable[T_ParamSpec, Coroutine[Any, Any, T_Retval]],
    ) -> Callable[T_ParamSpec, T_Retval]:
        # implements abstract method

        @functools.wraps(async_function)
        def wrapper(*args: T_ParamSpec.args, **kwargs: T_ParamSpec.kwargs) -> T_Retval:
            partial_f = functools.partial(async_function, *args, **kwargs)

            # run_until_complete() only runs the event loop until partial_f() has finished.
            # - The loop does not continue running in the background.
            # - This method will throw a RuntimeError if there is already an event loop
            #   running in the calling thread.
            return self._loop.run_until_complete(partial_f())

        return wrapper


class BackgroundSyncRunner(SyncRunner):
    """
    Runs async functions in a dedicated event loop in a background thread.

    This has the overhead of spawning a dedicated daemon thread.
    """

    def __init__(self):
        # lazy import
        import threading

        self._lock = threading.Lock()
        self._loop = asyncio.new_event_loop()
        self._running = False
        self._thread = threading.Thread(target=self._run_loop, daemon=True)

    @property
    def is_closed(self):
        return self._loop.is_closed() and not self._thread.is_alive()

    def start(self):
        with self._lock:
            if not self._thread.is_alive():
                self._thread.start()

    def stop(self):
        # implements abstract method
        with self._lock:
            if self._running:
                self._loop.call_soon_threadsafe(self._loop.stop)
                self._thread.join()

    def syncify(
        self,
        async_function: Callable[T_ParamSpec, Coroutine[Any, Any, T_Retval]],
    ) -> Callable[T_ParamSpec, T_Retval]:
        # implements abstract method

        # start the thread (if necessary) for running sync functions created here
        self.start()

        @functools.wraps(async_function)
        def wrapper(*args: T_ParamSpec.args, **kwargs: T_ParamSpec.kwargs) -> T_Retval:
            partial_f = functools.partial(async_function, *args, **kwargs)
            fut = asyncio.run_coroutine_threadsafe(partial_f(), self._loop)
            return fut.result()

        return wrapper

    def _run_loop(self):
        asyncio.set_event_loop(self._loop)
        self._running = True
        try:
            self._loop.run_forever()
        finally:
            self._loop.close()
            self._running = False
