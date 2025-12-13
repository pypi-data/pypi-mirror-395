"""Common handler utilities for RPC client and service."""

import asyncio
import contextlib
from collections.abc import AsyncGenerator, Callable, Coroutine
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from typing import Any

from .errors import RPCException, create_error
from .types import ErrorCode, PullIteratorRequest, PullIteratorResponse, RPCClient, RPCError, StreamMessage
from .utils import is_async_function, is_async_generator, is_sync_generator


async def handle_stream_request(
    handler: Callable[..., Any],
    args: list[Any],
    stream_subject: str,
    request_id: str,
    client: RPCClient,
    io_pool: ThreadPoolExecutor,
) -> None:
    """Handle streaming request - common logic for client and service."""
    generator: AsyncGenerator[Any, None]

    # Get generator
    if is_async_generator(handler):
        # Handler is an async generator function
        generator = handler(*args)
    elif is_sync_generator(handler):
        # Handler is a sync generator function - convert to async
        sync_gen = handler(*args)

        async def async_wrapper():
            for value in sync_gen:
                yield value

        generator = async_wrapper()
    elif is_async_function(handler):
        # Handler is async function that might return a generator
        result = await handler(*args)
        if hasattr(result, "__aiter__"):
            generator = result
        elif hasattr(result, "__iter__"):
            # Sync generator returned from async function
            async def async_wrapper():
                for value in result:
                    yield value

            generator = async_wrapper()
        else:
            raise create_error(ErrorCode.INTERNAL_ERROR, "Handler must return a generator for stream")
    else:
        # Run sync handler in thread pool
        loop = asyncio.get_event_loop()
        func = partial(handler, *args)
        result = await loop.run_in_executor(io_pool, func)

        if hasattr(result, "__aiter__"):
            generator = result
        elif hasattr(result, "__iter__"):
            # Sync generator returned from sync function
            async def async_wrapper():
                for value in result:
                    yield value

            generator = async_wrapper()
        else:
            raise create_error(ErrorCode.INTERNAL_ERROR, "Handler must return a generator for stream")

    # Verify we have an async iterator
    if not hasattr(generator, "__aiter__"):
        raise create_error(ErrorCode.INTERNAL_ERROR, "Failed to create async generator from handler")

    # Listen for cancellation
    cancelled = False

    async def cancel_handler(_: Any) -> None:
        nonlocal cancelled
        cancelled = True

    cancel_unsub = await client.subscribe(f"{stream_subject}.cancel", cancel_handler)

    # Give client time to set up subscription
    await asyncio.sleep(0)

    # Stream values
    try:
        async for value in generator:
            if cancelled:
                break

            stream_msg: StreamMessage = {
                "id": request_id,
                "type": "data",
                "data": value,
            }
            await client.publish(stream_subject, stream_msg)

        if not cancelled:
            end_msg: StreamMessage = {"id": request_id, "type": "end"}
            await client.publish(stream_subject, end_msg)

    except Exception as e:
        if not cancelled:
            error_msg: StreamMessage = {
                "id": request_id,
                "type": "error",
                "error": e.to_dict()
                if isinstance(e, RPCException)
                else {
                    "code": ErrorCode.STREAM_ERROR.value,
                    "message": str(e),
                },
            }
            await client.publish(stream_subject, error_msg)
    finally:
        await cancel_unsub()
        if hasattr(generator, "aclose"):
            # Ensure generator is closed
            with contextlib.suppress(Exception):
                await generator.aclose()


async def handle_normal_rpc(
    handler: Callable[..., Any],
    params: Any,
    io_pool: ThreadPoolExecutor,
) -> Any:
    """Handle normal RPC call - common logic for client and service."""
    # Ensure params is a list
    if not isinstance(params, list):
        params = [params] if params is not None else []

    # Call the handler
    if is_async_function(handler):
        return await handler(*params)
    else:
        loop = asyncio.get_event_loop()
        func = partial(handler, *params)
        return await loop.run_in_executor(io_pool, func)


def format_error_dict(e: Exception) -> RPCError:
    """Format exception as error dictionary."""
    if isinstance(e, RPCException):
        return e.to_dict()
    else:
        return {
            "code": ErrorCode.INTERNAL_ERROR.value,
            "message": str(e),
        }


async def handle_pull_iterator_request(
    handler: Callable[..., Any],
    args: list[Any],
    iterator_id: str,
    client: RPCClient,
    io_pool: ThreadPoolExecutor,
) -> Callable[[], Coroutine[Any, Any, None]]:
    """Handle pull-based iterator request."""
    generator: AsyncGenerator[Any, None]

    # Get generator
    if is_async_generator(handler):
        # Handler is an async generator function
        generator = handler(*args)
    elif is_sync_generator(handler):
        # Handler is a sync generator function - convert to async
        sync_gen = handler(*args)

        async def async_wrapper():
            for value in sync_gen:
                yield value

        generator = async_wrapper()
    elif is_async_function(handler):
        # Handler is async function that might return a generator
        result = await handler(*args)
        if hasattr(result, "__aiter__"):
            generator = result
        elif hasattr(result, "__iter__"):
            # Sync generator returned from async function
            async def async_wrapper():
                for value in result:
                    yield value

            generator = async_wrapper()
        else:
            raise create_error(ErrorCode.INTERNAL_ERROR, "Handler must return a generator for pull iterator")
    else:
        # Run sync handler in thread pool
        loop = asyncio.get_event_loop()
        func = partial(handler, *args)
        result = await loop.run_in_executor(io_pool, func)

        if hasattr(result, "__aiter__"):
            generator = result
        elif hasattr(result, "__iter__"):
            # Sync generator returned from sync function
            async def async_wrapper():
                for value in result:
                    yield value

            generator = async_wrapper()
        else:
            raise create_error(ErrorCode.INTERNAL_ERROR, "Handler must return a generator for pull iterator")

    # Verify we have an async iterator
    if not hasattr(generator, "__aiter__"):
        raise create_error(ErrorCode.INTERNAL_ERROR, "Failed to create async generator from handler")

    # Set up request/response subjects
    request_subject = f"_rpc.iterator.{iterator_id}.request"
    response_subject = f"_rpc.iterator.{iterator_id}.response"

    # Track if iterator is active
    active = True
    unsub_func = None

    # Subscribe to iterator requests
    async def handle_pull_request(msg: PullIteratorRequest) -> None:
        nonlocal active

        if not active:
            return

        try:
            if msg.get("type") == "cancel":
                active = False
                # Close the generator explicitly
                if hasattr(generator, "aclose"):
                    await generator.aclose()
                response: PullIteratorResponse = {
                    "id": iterator_id,
                    "type": "done",
                }
                await client.publish(response_subject, response)
            elif msg.get("type") == "next":
                try:
                    value = await generator.__anext__()
                    response: PullIteratorResponse = {
                        "id": iterator_id,
                        "type": "value",
                        "value": value,
                    }
                    await client.publish(response_subject, response)
                except StopAsyncIteration:
                    active = False
                    response: PullIteratorResponse = {
                        "id": iterator_id,
                        "type": "done",
                    }
                    await client.publish(response_subject, response)

        except Exception as e:
            active = False
            response: PullIteratorResponse = {
                "id": iterator_id,
                "type": "error",
                "error": format_error_dict(e),
            }
            await client.publish(response_subject, response)

    unsub_func = await client.subscribe(request_subject, handle_pull_request)

    # Return cleanup function
    async def cleanup() -> None:
        nonlocal active
        active = False
        if unsub_func:  # pyright: ignore[reportUnnecessaryComparison]
            await unsub_func()
        # Ensure generator is closed
        if hasattr(generator, "aclose"):
            with contextlib.suppress(Exception):
                await generator.aclose()

    return cleanup
