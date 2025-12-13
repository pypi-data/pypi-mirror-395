# coding=utf-8

from applyx.command.base import BaseCommand


class Command(BaseCommand):
    def register(self, subparser):
        parser = subparser.add_parser('mcp', help='run mcp service')
        parser.add_argument(
            '--host',
            type=str,
            dest='host',
            default='0.0.0.0',
            help='specify mcp host',
        )
        parser.add_argument(
            '--port',
            type=int,
            dest='port',
            default=9000,
            help='specify mcp port',
        )
        parser.add_argument(
            '--transport',
            type=str,
            dest='transport',
            default='sse',
            help='specify mcp transport type',
        )

    def invoke(self, args):
        from applyx.mcp.builder import FastMCPBuilder

        mcp_app = FastMCPBuilder.get_app(self.project, args.transport)
        if mcp_app is None:
            return

        mcp_app.run(
            host=args.host,
            port=args.port,
            transport=args.transport,
        )

