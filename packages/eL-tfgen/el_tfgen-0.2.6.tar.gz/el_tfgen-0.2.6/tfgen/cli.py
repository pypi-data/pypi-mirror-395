import asyncio
from .terraform_parser import main

def cli():
    asyncio.run(main()) 