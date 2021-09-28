from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport
import xmltodict
import json


def prepare_data(temp_dict: dict) -> dict:
    final_dict = {'date': temp_dict['Day']['@date'], 'rates': {}}

    for item in temp_dict['Day']['Rate']:
        final_dict['rates'][item['@curr']] = {
            'unit': item['@unit'],
            'value': item['#text']
        }

    return final_dict


def main():
    cache = SqliteCache(path='sqlite.db', timeout=60)
    transport = Transport(cache=cache)
    # noinspection HttpUrlsUsage
    client = Client(
        'http://www.mnb.hu/arfolyamok.asmx?singleWsdl',  # API doesn't support HTTPS
        transport=transport
    )

    with client.settings(strict=True, raw_response=False):
        response_from_api = client.service.GetCurrentExchangeRates()

        temp_dict = xmltodict.parse(response_from_api)['MNBCurrentExchangeRates']
        final_dict = prepare_data(temp_dict)
        print(json.dumps(final_dict, indent=4))


if __name__ == '__main__':
    main()
