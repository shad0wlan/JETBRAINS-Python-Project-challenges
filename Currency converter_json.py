import requests

rates = {}
# write your code here!
return_money = None
usd = requests.get(f'http://www.floatrates.com/daily/usd.json').json()
eur = requests.get(f'http://www.floatrates.com/daily/eur.json').json()
# write your code here!
rates['usd'] = float(usd['eur']['rate'])
rates['eur'] = float(eur['usd']['rate'])

currency = input().lower().strip()
while True:
    currency_to = input().lower().strip()
    if currency_to == "":
        break
    money = int(input())
    print("Checking the cache...")

    # Dealing with beginning if the rates USD and EUR are already there

    if currency == "USD".lower() and currency_to == "EUR".lower():
        print('Oh! It is in the cache!')
        return_money = round(float(rates[currency]) * money, 2)
        print(f'Your received {return_money} {currency_to.upper()}.')
        continue

    # Getting currency rates if source rate isnt there
    if currency not in rates.keys():
        get_url = requests.get(f'http://www.floatrates.com/daily/{currency}.json').json()
        rates['usd'] = float(get_url['usd']['rate'])
        rates['eur'] = float(get_url['eur']['rate'])
        rates[currency] = float(get_url[currency_to]['rate'])
        return_money = round(float(rates[currency]) * money, 2)

    # Continuing calculations for rates already there
    if currency in rates.keys() and currency_to in rates.keys():
        print('Oh! It is in the cache!')
        return_money = round(float(rates[currency]) * money, 2)

    # Getting target rates for source rate
    if currency_to not in rates.keys():
        print("Sorry, but it is not in the cache!")
        get_url = requests.get(f'http://www.floatrates.com/daily/{currency}.json').json()
        rates[currency_to] = get_url[currency_to]['rate']
    return_money = round(float(rates[currency_to]) * money, 2)

    print(f'Your received {return_money} {currency_to.upper()}.')