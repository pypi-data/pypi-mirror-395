import functools
import inspect
import signal
import anyio
from typing import Any, Callable, Generic, Literal, TypeVar


F = TypeVar("F", bound=Callable[..., Any])

type Group = Literal["enter", "loop", "exit"]


class Registration(Generic[F]):

    def __init__(self, function: F, group: Group):
        self.function: F = function
        self.group = group


def enter(func: F) -> Registration[F]:
    return Registration(func, group="enter")

def exit(func: F) -> Registration[F]:
    return Registration(func, group="exit")

def loop(func: F) -> Registration[F]:
    return Registration(func, group="loop")


class Concurrentor:
    def __init__(self):
        self.enters = []
        self.loops = []
        self.exits = []
        for name, registration in inspect.getmembers(
            self.__class__, predicate=lambda x: isinstance(x, Registration)
        ):
            self.__setattr__(name, registration.function)
            if registration.group == "enter":
                self.enters.append(registration.function)
            elif registration.group == "loop":
                self.loops.append(registration.function)
            elif registration.group == "exit":
                self.exits.append(registration.function)
            else:
                pass


    async def _signal_handler(self, scope: anyio.CancelScope):
        with anyio.open_signal_receiver(signal.SIGINT, signal.SIGTERM) as signals:
            async for _ in signals:
                scope.cancel()
                return

    async def _main(self):
        async with anyio.create_task_group() as enters:
            for function in self.enters:
                enters.start_soon(function, self)
        
        async with anyio.create_task_group() as loops:
            loops.start_soon(self._signal_handler, loops.cancel_scope)
            for function in self.loops:
                async def _looper(_function=function):
                    while True:
                        await _function(self)
                loops.start_soon(_looper)
        
        async with anyio.create_task_group() as exits:
            for function in self.exits:
                exits.start_soon(function, self)


    def run(self):
        anyio.run(self._main)