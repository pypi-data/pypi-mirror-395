# Curs valutar BNR pentru RON

Librarie python care poate fi folosita pentru a afla cursul BNR pentru RON la o data specificata sau nu.


## Utilizare

Instaleaza libraria cu:

```py
pip install cursvalutarbnr
```

Poti incepe conversia in felul urmator:

```py

from cursvalutarbnr import Currency, ron_exchange_rate

# Asa faci conversia din EUR in RON

eur_to_ron = ron_exchange_rate(
    amount=1,              # suma pe care vrei sa o convertesti la 'currency'
    currency=Currency.EUR,  # valuta (curency) in care vrei sa fie convertita suma specificata in 'amount' (poate fi si un simplu string ca: "EUR", "USD" etc)
    date="2024-04-25"       # (Optional) poti specifica si data in isoformat pentru care vrei sa fie convertita suma
)

print("eur_to_ron", eur_to_ron)

```

Pentru a nu apela api-ul de la BNR pentru fiecare apelare datele sunt salvate in temporary folder `cache_cursvalutarbnr`.
