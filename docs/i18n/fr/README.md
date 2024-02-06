# mnb.hu-apicalls-test

[![en](https://img.shields.io/badge/lang-en-red.svg)](../../../README.md)
[![fr](https://img.shields.io/badge/lang-fr-blue.svg)](./README.md)

Quelques essais d'appels de l'API de la banque centrale hongroise (Magyar Nemzeti Bank, "Banque nationale hongroise").

L'API est une API publique SOAP.

## Pré-requis

- Python ^3.8
- [Poetry](https://python-poetry.org)

## Notes

### Lister les opérations de l'API

D'abord, je liste les opérations disponibles de l'API ainsi que leur signature:
```shell
python -mzeep https://www.mnb.hu/arfolyamok.asmx?wsdl
```

Réponse:
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

La librairie `zeep` utilise le premier service défini par défault. Quelques exemples d'appels :
```python
result = client.service.GetCurrencies()
result = client.service.GetInfo()
result = client.service.GetCurrencyUnits('EUR')
```

### Conversion des données
La librairie `zeep` se charge normalement de convertir la réponse XML de l'API en un dictionnaire Python, mais l'API a l'air de renvoyer un XML non valide.

J'utilise la librairie `xmltodict` pour effectuer cette tâche.

Ensuite, je structure les données de la manière voulue dans la fonction `prepare_data()`.

Les données converties JSON ressemblent à ceci (extrait seulement) :
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

Cela me permet d'accéder aux résultats de cette manière :
```python
print(final_dict["rates"]["AUD"])
{'unit': '1', 'value': '223,72'}
# 1 AUD = 223,72 HFU

print(final_dict["rates"]["JPY"])
{'unit': '100', 'value': '276,48'}
# 100 JPY = 276,48 HFU
```

La structure des données est bien sûr modifiable.
