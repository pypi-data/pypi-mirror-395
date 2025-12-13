from __future__ import annotations

from eventry.asyncio.event import Event
from eventry.asyncio.router import DefaultRouter
from eventry.asyncio.dispatcher import DefaultDispatcher


dp = DefaultDispatcher()
r = DefaultRouter(name='hui')
dp.connect_router(r)



async def handler_middleware():
    print('handler middleware')
    yield
    print('handler_middleware finalizer')


def inner_middleware():
    print('Inner middleware')
    yield
    print('Inner middleware finalizer')


def outer_middleware():
    print('Outer middleware')
    yield
    print('Outer middleware finalizer')


def manger_innder_middleware():
    print('Manager inner middleware')
    yield
    print('Manager inner middleware finalizer')


def manger_outer_middleware():
    print('Manager outer middleware')
    yield
    print('Manager outer middleware finalizer')


def handling_process_middleware():
    print('Handling process middleware')
    try:
        yield
    except Exception as e:
        print(e)
        raise
    print('Handling process middleware finalizer')

def handling_process_middleware2():
    print('Handling process middleware2')
    yield
    print('Handling process middleware2 finalizer')
    raise Exception('Error in handling process middleware')


dp.on_event.manager_inner_middleware(manger_innder_middleware)
dp.on_event.manager_outer_middleware(manger_outer_middleware)
dp.on_event.outer_middleware(outer_middleware)
dp.on_event.inner_middleware(inner_middleware)
dp.on_event.handling_process_middleware(handling_process_middleware)
dp.on_event.handling_process_middleware(handling_process_middleware2)


def some_filter():
    print("R filter returns False")
    return False


r.on_event.set_filter(some_filter)


@dp.on_event(middlewares=[handler_middleware])
def handle():
    print('event')


@r.on_event()
def handle2():
    print('event2')


async def main():
    await dp.event_entry(Event())


if __name__ == '__main__':
    import asyncio

    asyncio.run(main())
