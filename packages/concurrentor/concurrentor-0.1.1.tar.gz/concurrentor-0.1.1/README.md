# Concurrentor

A simple wrapper class around anyio to help create programs that contain multiple concurrent but interacting parts.

## Usage

```python
from anyio import sleep
from concurrentor import Concurrentor, enter, loop, exit

class Application(Concurrentor):

    @enter
    async def run_once_at_enter(self):
        print("I run only once at the beginning.")

    @exit
    async def run_once_at_exit(self):
        print("I run only once at the end.")

    @loop
    async def run_repeatedly_one(self):
        print("I am called repeatedly.")
        await sleep(2)

    @loop
    async def run_repeatedly_two(self):
        print("I am called repeatedly, too.")
        await sleep(3)


if __name__ == "__main__":
    app = Application()
    app.run()
```
