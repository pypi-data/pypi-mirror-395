import logging
import os
import sys

import click

from huayi_mcp_server.tools import ToolSet

logger = logging.getLogger(__name__)


@click.command()
@click.option(
    "--transport",
    default="stdio",
    help="MCP transport: stdio, streamable-http, sse",
)
@click.option(
    "--log-level",
    default="INFO",
    help="Log level: DEBUG, INFO, WARNING, ERROR",
)
def main(transport: str | None, log_level: str | None) -> int:
    """Run the MCP Server."""
    transport = transport if transport else "stdio"
    log_level = log_level if log_level else "INFO"

    logging.basicConfig(
        level=getattr(logging, log_level.upper(), logging.INFO),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    base_url = os.getenv("BASE_URL", None)
    if not base_url:
        raise Exception("BASE_URL is not provided")

    secret = os.getenv("HUAJITONG_SECRET", None)
    if not secret:
        raise Exception("HUAJITONG_SECRET is not provided")

    logger.info("Starting MCP Server")

    toolset = ToolSet(name="Huayi MCP", log_level=log_level, base_url=base_url, secret=secret)
    host = toolset.mcp.settings.host
    port = toolset.mcp.settings.port
    streamable_http_path = toolset.mcp.settings.streamable_http_path
    sse_path = toolset.mcp.settings.sse_path

    try:
        if transport.lower() == "streamable-http":
            logger.info(f"StreamableHTTP endpoint will be: http://{host}:{port}{streamable_http_path}")
            toolset.run_on_streamable_http()

        if transport.lower() == "sse":
            logger.info(f"SSE endpoint will be: http://{host}:{port}{sse_path}")
            toolset.run_on_sse()

        if transport.lower() == "stdio":
            logger.info("MCP Server will run on Stdio")
            toolset.run_on_stdio()

    except KeyboardInterrupt:
        logger.info("received Ctrl-C, shutting down...")
        sys.exit(0)

    return 0


if __name__ == "__main__":
    main()
