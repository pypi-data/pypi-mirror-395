import os
import re
import json
import time
import importlib.metadata
import asyncio
from pydantic import Field
from typing import Annotated, Any
from postcode_eu_api_client import Client, PostcodeEuException
from platformdirs import user_cache_dir

class PostcodeEuTools:
    def __init__(self, api_key: str, api_secret: str):
        package_name = 'postcode-eu-ai-tools'
        version = importlib.metadata.version(package_name)
        self._client: Client = Client(api_key, api_secret, f'{package_name}/{version}')

    async def lookup_dutch_address(
        self,
        postcode: Annotated[
            str,
            Field(
                title='Postcode',
                description='Dutch postcode of 4 digits followed by 2 letters. E.g. 1234AB or 6969 xy.'
            )
        ],
        house_number_and_addition: Annotated[
            str,
            Field(
                title='House number and addition',
                description=('House number with optional addition. The house number part should be '
                    'within a range of 1 to 99999. The addition can be 6 characters at most.')
            )
        ]
    ) -> dict[str, Any]:
        """
        Get an address based on its unique combination of postcode, house number and (optionally) house number addition.

        Examples of valid house numbers:
        - "69" → house number 69, no addition
        - "123A" → house number 123, addition "A"
        - "1 101" → house number 1, addition "101"
        - "67 III" → house number 67, addition "III"
        - "3 B 12" → house number 3, addition "B 12"

        In case of an incorrect house number addition, ask the user to specify the correct house number.
        The first few valid house number options are provided as suggestions if the house number was incorrect.
        Assume the list of house number suggestions is incomplete. If it is just one option, ask/suggest using that.
        IMPORTANT: do not modify the returned address values.
        """
        house_number_match = re.match(
            r'^([1-9]\d{0,4})(\D.*)?$',
            house_number_and_addition.strip(),
            re.IGNORECASE
        )

        if house_number_match is None:
            return {'error': 'House number not valid'}

        [house_number, addition] = house_number_match.groups()
        house_number = int(house_number)

        try:
            address = await asyncio.to_thread(
                self._client.dutch_address_by_postcode, postcode, house_number, addition
            )
        except PostcodeEuException as e:
            return {'error': str(e)}

        # Truncate additions, as this list can get long for some addresses.
        address['houseNumberAdditions'] = address['houseNumberAdditions'][:5]

        status = 'valid'
        house_number_suggestions: list[str] = []
        if (((address.get('houseNumberAddition') or '').lower() != (addition or '').lower())
                or (address.get('houseNumberAdditions') and address.get('houseNumberAddition') is None)):
            status = 'houseNumberAdditionIncorrect'

            # Provide only a few house number suggestions to keep the reply short.
            for value in address['houseNumberAdditions']:
                house_number_suggestions.append(f'{house_number} {value}')

        return {
            'address': address,
            'status': status,
            'house_number_suggestions': house_number_suggestions or None,
        }

    async def get_supported_countries(self) -> dict[str, str]:
        """
        List supported countries for which address validation is available.
        """
        countries: dict[str, str] = {}
        cache_dir = user_cache_dir(appname='postcode-eu-ai-tools', appauthor='Postcode.eu')
        cache_file = os.path.join(cache_dir, 'supported-countries.json')
        if os.path.exists(cache_file):
            try:
                with open(cache_file) as f:
                    cache_data = json.load(f)

                if time.time() - cache_data.get('timestamp', 0) < 86400:  # Cache for a day.
                    countries = cache_data['countries']
            except (json.JSONDecodeError, KeyError):
                pass

        if not countries:
            response = await asyncio.to_thread(self._client.international_get_supported_countries)
            countries = {country['iso3']: country['name'] for country in response}
            cache_data = {'timestamp': time.time(), 'countries': countries}
            os.makedirs(cache_dir, exist_ok=True)
            with open(cache_file, 'w') as f:
                json.dump(cache_data, f)

        return countries

    async def is_supported_country(
        self,
        country_iso3: Annotated[
            str,
            Field(
                title='Country ISO3 code',
                description='The ISO3 code of the country to check',
                pattern='[a-zA-Z]{3}'
            )
        ]
    ) -> bool:
        """
        Check if a country is supported for address validation.
        """
        countries = await self.get_supported_countries()
        return country_iso3.upper() in countries

    async def validate_address(
        self,
        country: Annotated[
            str,
            Field(
                title='Country',
                description='Country ISO3 code',
                pattern='[a-zA-Z]{3}'
            )
        ],
        postcode: Annotated[
            str | None,
            Field(
                title='Postcode',
                description='The postcode',
            )
        ] = None,
        locality: Annotated[
            str | None,
            Field(
                title='Locality',
                description='The locality or city/town'
            )
        ] = None,
        street: Annotated[
            str | None,
            Field(
                title='Street',
                description='The street name, without building number or name'
            )
        ] = None,
        building: Annotated[
            str | None,
            Field(
                title='Building',
                description='The full building number, including any additions'
            )
        ] = None,
        region: Annotated[
            str | None,
            Field(
                title='Region',
                description=('The region name. Strictly for province, state, etc.')
            )
        ] = None,
    ) -> dict[str, Any]:
        """
        Validate and correct/complete a full international address using the Postcode.eu API.

        Provide address parts (country is required; others are optional but recommended for accuracy).

        Returns the top validated match if:
        - The country is supported.
        - A match is found.
        - The match was not ambiguous (i.e. there were multiple equally similar matches).
        - The match has high grade (A or B, indicating close correspondence to input).
        - The match is a full address (i.e. has a valid building number).

        IMPORTANT: do not modify the returned address values.
        """
        if not await self.is_supported_country(country):
            return {'error': 'Country not supported'}

        try:
            response = await asyncio.to_thread(
                self._client.validate, country, postcode, locality, street, building, region
            )
        except PostcodeEuException as e:
            return {'error': str(e)}

        if len(response['matches']) == 0:
            return {'error': 'No match found'}

        status = response['matches'][0]['status']

        if (status['isAmbiguous']):
            return {'error': 'The address is ambiguous'}
        elif (status['grade'] >= 'C'):
            return {'error': 'The address has low grade'}
        elif (status['validationLevel'] not in ['Building', 'BuildingPartial']):
            return {'error': 'Not a full address, provide more address parts'}

        return dict(response['matches'][0])
