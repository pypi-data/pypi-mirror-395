import asyncio
from dotenv import load_dotenv
from .commands import SpoonAICLI


def main_async():
    load_dotenv(override=True)
    cli = SpoonAICLI()
    return cli.run()


def cli():
    asyncio.run(main_async())

if __name__ == "__main__":
    cli()
