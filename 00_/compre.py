tea_prices = {
    "chai": 10,
    "coffee": 15,
    "tea": 20,
    "coffee": 25,
    "tea": 30,
    "coffee": 35,
    "tea": 40,
    "coffee": 45,
    "tea": 50,
    "coffee": 55,
    "tea": 60,
    "coffee": 65,
    "tea": 70,
    "coffee": 75,
    "tea": 80,
    "coffee": 85,
    "tea": 90,
    "coffee": 95,
    "tea": 100,
}

tea_prices_usd = {chai: price * 0.85 for chai, price in tea_prices.items() if price > 20}
print(tea_prices_usd, " 🚀")