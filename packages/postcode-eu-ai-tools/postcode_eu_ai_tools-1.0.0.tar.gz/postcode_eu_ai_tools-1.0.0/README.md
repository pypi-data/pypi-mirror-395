# Postcode.eu AI Tools

AI tools / MCP server for address validation via the Postcode.eu API. This package provides an MCP (Model Context Protocol) server using FastMCP, exposing tools for Dutch address lookup and international address validation. Can also be used as a library to integrate these tools as you see fit.

## Usage

### As a library

Install the package and its dependencies using uv to use it in your own projects:

```bash
uv add postcode-eu-ai-tools
```

### As an application

To run the MCP server directly, use the `uv tool` interface:

```bash
uvx postcode-eu-ai-tools
```

This starts the server on STDIO transport.

### Connect MCP clients

Use the address validation tools in any client that supports local MCP servers. Just add the `uvx postcode-eu-ai-tools` command to your configuration.

Example configuration for Claude Code:

```json
{
  "mcpServers": {
    "postcode-eu-address-validation": {
      "command": "uvx",
      "args": ["postcode-eu-ai-tools"],
      "env": {
        "POSTCODE_EU_API_KEY": "your_api_key",
        "POSTCODE_EU_API_SECRET": "your_api_secret"
      }
    }
  }
}
```

## Configuration

Provide your Postcode.eu API credentials via one of these methods:

1. **Environment Variables** (recommended):
   ```
   export POSTCODE_EU_API_KEY="your_api_key"
   export POSTCODE_EU_API_SECRET="your_api_secret"
   ```

2. Using a configuration file:
   ```bash
    uvx postcode-eu-ai-tools --save-credentials
    # You will then be asked for your API key and secret.
   ```

Register an account at [account.postcode.eu](https://account.postcode.eu) to get your credentials. You can test our service for free.

## Tools

The MCP server exposes these tools:

### lookup_dutch_address

Look up a Dutch address by postcode (e.g., "1234AB") and house number (e.g., "69" or "123A"). Returns the full address, and provides house number suggestions if the addition is invalid. Otherwise returns an error message describing why the address is invalid.

See https://developer.postcode.eu/documentation/nl/v1/Address/viewByPostcode

**Examples**:

User:
> What is the address for postcode 2012es with house number 30?

Assistant:
>Julianastraat 30  
2012ES Haarlem  
Noord-Holland, Netherlands

User:
>What is the address for 2161AM with house number 166b?

Assistant:
>Stationsweg 166, 2161AM Lisse, Zuid-Holland, Netherlands (house number addition "b" incorrect).  
Valid additions: "" (166) or "A" (166 A). Which one?

User:
>Is the address 1000AA 1 a PO box?

Assistant:
>Yes, Postbus 1, 1000AA Amsterdam, Noord-Holland, Netherlands (addressType: "PO box").

### validate_address

Validate and complete an international address. Returns the first match if valid (meaning it's a full address that closely corresponds to the input). Otherwise returns an error message describing why the address is invalid. Partial addresses are considered invalid.

See https://developer.postcode.eu/documentation/international/v1/Validate/validate

**Examples**:

User:
>Can you validate the address "leystraat 11 2000 antwerpen"?

Assistant:
>Leysstraat 11  
2000 Antwerpen  
Belgium  
Validated (grade B, building level).

User:
>How about "Kirsten Flagstads plass 1" in Oslo?

Assistant:
>Kirsten Flagstads plass 1  
0150 Oslo  
Norway  
Validated (grade A, building level).

### get_supported_countries

List countries that are supported for address validation.

See https://developer.postcode.eu/documentation/international/v1/Autocomplete/getSupportedCountries

**Example**:

User:
>For which countries can you validate addresses?

Assistant:
>Netherlands, Belgium, Germany, Luxembourg, Austria, Switzerland, France, United Kingdom, Spain, Denmark, Norway, Finland, Sweden.

### is_supported_country

Check if a country is supported for address validation.

See https://developer.postcode.eu/documentation/international/v1/Autocomplete/getSupportedCountries

**Example**:

User:
>Could you validate an address from Kazakhstan?

Assistant:
>No, Kazakhstan (KAZ) is not supported.

## Requirements

- Python 3.11+
- A Postcode.eu account. Register your account at [account.postcode.eu](https://account.postcode.eu). You can test our service for free.

## License

The code is available under the Simplified BSD License; see the included LICENSE file.
