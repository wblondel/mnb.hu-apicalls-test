# mnb.hu-apicalls-test

[![en](https://img.shields.io/badge/lang-en-red.svg)](./README.md)
[![fr](https://img.shields.io/badge/lang-fr-blue.svg)](./docs/i18n/fr/README.md)

Some test calls to the Hungarian central bank's API (Magyar Nemzeti Bank, "Hungarian National Bank").

The API is a public SOAP API.

## Requirements

- Python >3.9
- [Poetry](https://python-poetry.org)

## Notes, how-tos

### List available operations from the API

First, get an overview of all available operations and their call signatures:
```shell
python -mzeep https://www.mnb.hu/arfolyamok.asmx?wsdl
```

Response:
```
Service: MNBArfolyamServiceSoapImpl
     Port: CustomBinding_MNBArfolyamServiceSoap (Soap11Binding: {http://tempuri.org/}CustomBinding_MNBArfolyamServiceSoap)
         Operations:
            GetCurrencies() -> GetCurrenciesResult: xsd:string
            GetCurrencyUnits(currencyNames: xsd:string) -> GetCurrencyUnitsResult: xsd:string
            GetCurrentExchangeRates() -> GetCurrentExchangeRatesResult: xsd:string
            GetDateInterval() -> GetDateIntervalResult: xsd:string
            GetExchangeRates(startDate: xsd:string, endDate: xsd:string, currencyNames: xsd:string) -> GetExchangeRatesResult: xsd:string
            GetInfo() -> GetInfoResult: xsd:string
```

The `zeep` library use the first defined service by default. Some example calls:
```python
result = client.service.GetCurrencies()
result = client.service.GetInfo()
result = client.service.GetCurrencyUnits('EUR')
```

### Converting the returned data
The `zeep` should convert the XML from the API into a dict but the API somehow returns an invalid/incomplete XML.

I use the `xmltodict` library manages to do it.

I then structure the data the way I want in the `prepare_data()` function.

The data converted into JSON looks like this (extract only):
```json
{
    "date": "2021-09-28",
    "rates": {
        "AUD": {
            "unit": "1",
            "value": "223,72"
        },
        "BGN": {
            "unit": "1",
            "value": "183,76"
        },
        "BRL": {
            "unit": "1",
            "value": "57,06"
        },
        "JPY": {
            "unit": "100",
            "value": "276,48"
        }
    }
}
```

This allows me to access the results this way:
```python
print(final_dict["rates"]["AUD"])
{'unit': '1', 'value': '223,72'}
# 1 AUD = 223,72 HFU

print(final_dict["rates"]["JPY"])
{'unit': '100', 'value': '276,48'}
# 100 JPY = 276,48 HFU
```

The data structure is of course modifiable.
