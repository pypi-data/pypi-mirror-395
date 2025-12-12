import sys
import asyncio
import contextvars

import IPython
import click
from IPython.terminal.ipapp import load_default_config


@click.command(context_settings=dict(ignore_unknown_options=True))
@click.argument('ipython_args', nargs=-1, type=click.UNPROCESSED)
@click.pass_context
def shell(ctx, ipython_args):
    # Get app from click context without async wrapper
    from quart.cli import ScriptInfo
    info = ctx.ensure_object(ScriptInfo)
    app = info.load_app()

    # Create event loop for Python 3.13 compatibility
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError('Event loop is closed')
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)

    # Python 3.13: Set custom event loop policy
    class ShellEventLoopPolicy(asyncio.DefaultEventLoopPolicy):
        def get_event_loop(self):
            return loop

    asyncio.set_event_loop_policy(ShellEventLoopPolicy())

    # Run startup and get shell context
    loop.run_until_complete(app.startup())
    context = app.make_shell_context()

    # Configure IPython banner
    config = load_default_config()
    env = getattr(app, 'env', 'debug' if app.debug else 'production')
    config.TerminalInteractiveShell.banner1 = """Python %s on %s
IPython: %s
App: %s [%s]
""" % (
        sys.version,
        sys.platform,
        IPython.__version__,
        app.import_name,
        env,
    )

    # Run IPython within app context
    async def run_shell():
        async with app.app_context():
            # Copy context so it's available in the executor thread
            ctx = contextvars.copy_context()

            # Run IPython in executor with copied context
            await loop.run_in_executor(
                None,
                ctx.run,
                lambda: IPython.start_ipython(
                    argv=ipython_args,
                    user_ns=context,
                    config=config,
                )
            )

    loop.run_until_complete(run_shell())
