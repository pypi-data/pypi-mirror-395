from a2a_acl.agent.server_utils import run_server
from sample_agents.ping.pingable import (
    PingableAgentExecutor,
    my_card,
)
from a2a_acl.utils.url import build_url

my_port = 9999
the_host = "127.0.0.1"
my_url = build_url(the_host, my_port)


async def main() -> None:
    run_server(
        PingableAgentExecutor(my_card, build_url(the_host, my_port)), the_host, my_port
    )


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
    input("Press Enter to exit...\n")
