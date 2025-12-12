import asyncio

import fastapi
import websockets
from websockets.asyncio.client import connect


async def send_text(conn: websockets.ServerConnection | fastapi.WebSocket, data: str):
    if isinstance(conn, websockets.ServerConnection):
        await conn.send(data)
    elif isinstance(conn, fastapi.WebSocket):
        await conn.send_text(data)
    else:
        raise NotImplementedError(
            f"send_text not implemented for this connection type: {type(conn)}"
        )


def get_close_code(conn: websockets.ServerConnection | fastapi.WebSocket):
    if isinstance(conn, websockets.ServerConnection):
        return conn.close_code
    elif isinstance(conn, fastapi.WebSocket):
        return None


def parse_client_info(connection: websockets.ServerConnection | fastapi.WebSocket):
    """
    从连接中解析客户端ip、port等信息
    """
    if isinstance(connection, websockets.ServerConnection):
        client_ip, client_port = connection.transport.get_extra_info("peername")
    elif isinstance(connection, fastapi.WebSocket):
        client_ip, client_port = connection.client.host, connection.client.port
    else:
        client_ip, client_port = None, None
    return client_ip, client_port


def get_write_buffer_size(connection: websockets.ServerConnection | fastapi.WebSocket):
    """
    获取连接的写缓冲区大小
    """
    if isinstance(connection, websockets.ServerConnection):
        return connection.transport.get_write_buffer_size()
    else:
        raise NotImplementedError(
            "get_write_buffer_size not implemented for this connection type"
        )


def get_write_buffer_limits(
    connection: websockets.ServerConnection | fastapi.WebSocket,
):
    """
    获取连接的写缓冲区可用大小
    """
    if isinstance(connection, websockets.ServerConnection):
        return connection.transport.get_write_buffer_limits()
    else:
        raise NotImplementedError(
            "get_write_buffer_limits not implemented for this connection type"
        )


async def interactive_client():
    url = input("input websocket server url: ").strip()
    url = url if url.startswith("ws://") or url.startswith("wss://") else f"ws://{url}"
    async with connect(url) as conn:
        # 创建一个任务来接收消息
        async def receive_messages():
            while True:
                try:
                    msg = await conn.recv()
                    print(f"\nReceived: {msg}")
                    print("Enter message (or 'quit' to exit): ", end="", flush=True)
                except websockets.exceptions.ConnectionClosed:
                    print("\nConnection closed by server")
                    return

        # 创建一个任务来发送消息
        async def send_messages():
            while True:
                try:
                    message = await asyncio.get_event_loop().run_in_executor(
                        None, input, "Enter message (or 'quit' to exit): "
                    )
                    if message.lower() == "quit":
                        print("Closing connection...")
                        await conn.close()
                        return
                    await conn.send(message)
                except websockets.exceptions.ConnectionClosed:
                    print("\nConnection closed")
                    return

        # 同时运行接收和发送任务
        receive_task = asyncio.create_task(receive_messages())
        send_task = asyncio.create_task(send_messages())

        # 等待任一任务完成
        done, pending = await asyncio.wait(
            [receive_task, send_task], return_when=asyncio.FIRST_COMPLETED
        )

        # 取消未完成的任务
        for task in pending:
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass


def start_interactive_client():
    asyncio.run(interactive_client())


if __name__ == "__main__":
    start_interactive_client()
