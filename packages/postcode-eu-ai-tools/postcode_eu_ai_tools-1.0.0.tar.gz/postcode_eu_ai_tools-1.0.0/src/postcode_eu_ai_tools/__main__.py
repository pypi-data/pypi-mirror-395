import argparse
from mcp.server.fastmcp import FastMCP, Icon
from mcp.server.fastmcp.tools import Tool
from postcode_eu_ai_tools import PostcodeEuTools
from postcode_eu_ai_tools.utils import get_api_credentials, save_api_credentials

def main():
    parser = argparse.ArgumentParser()
    _ = parser.add_argument(
        '--save-credentials',
        action='store_true',
        help='Prompt for and save API credentials to config file.'
    )
    args = parser.parse_args()
    if args.save_credentials:
        save_api_credentials()
        exit()

    try:
        credentials = get_api_credentials()
    except ValueError:
        print(
            'Please add your API credentials using one of these methods:\n'
            + '1) Set POSTCODE_EU_API_KEY and POSTCODE_EU_API_SECRET environment vars (recommended).\n'
            + '2) Store credentials in a config file using the --save-credentials option.'
        )
        exit()

    postcode_eu_tools = PostcodeEuTools(*credentials)

    mcp = FastMCP(
        name='Postcode.eu address validation',
        instructions=(
            'Tools for address validation: '
            '- For Dutch addresses with postcode and house number, use lookup_dutch_address.\n'
            '- For other countries or incomplete Dutch addresses, use validate_address.\n'
            '- get_supported_countries lists countries that are supported for address validation.\n'
            '- is_supported_country checks if a single country is supported (returns boolean); '
            'not required before validate_address, as it handles unsupported countries with an error.\n'
            'Do not make repeated tool calls with the same arguments.\n'
            'Report errors to the user and ask for more address information if appropriate.'
        ),
        tools=[
            Tool.from_function(postcode_eu_tools.lookup_dutch_address),
            Tool.from_function(postcode_eu_tools.get_supported_countries),
            Tool.from_function(postcode_eu_tools.is_supported_country),
            Tool.from_function(postcode_eu_tools.validate_address),
        ],
        icons=[Icon(src='icon.svg')],
    )

    mcp.run(transport='stdio')


if __name__ == '__main__':
    main()
