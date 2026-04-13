users = [
    {"id":1 , "name": "John", "total_price": 20, "coupon": "New York"},
    {"id":2 , "name": "Jane", "total_price": 21, "city": "Los Angeles"},
    {"id":3 , "name": "Jim", "total_price": 22, "coupon": "Chicago"},
    {"id":4 , "name": "Jill", "total_price": 23, "city": "Houston"},
    {"id":5 , "name": "Jack", "total_price": 24, "coupon": "Miami"},
    {"id":6 , "name": "Jill", "total_price": 25, "city": "San Francisco"},
    {"id":7 , "name": "Ohil", "total_price": 26, "coupon": "Seattle"},
    {"id":8 , "name": "Phil", "total_price": 27, "city": "Boston"},
    {"id":9 , "name": "Jones", "total_price": 28, "coupon": "Washington D.C."},
    {"id":10 , "name": "Hill", "total_price": 29, "city": "Atlanta"},
]

discount_coupons = {
    "New York": (10,0),
    "Los Angeles": (15,0),
    "Chicago": (20,0),
    "Miami": (25,10),
    "San Francisco": (30,20),
    "Seattle": (35,0),
    "Boston": (40,30),
    "Washington D.C.": (45,40),
    "Atlanta": (50,50),
}

for user in users:
    percent_discount, fixed_discount = discount_coupons.get(user.get("coupon"), (0,0))
    discount = percent_discount * user["total_price"] + fixed_discount
    print(user , discount)