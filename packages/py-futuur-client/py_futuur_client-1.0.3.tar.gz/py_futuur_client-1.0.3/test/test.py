from py_futuur_client.client import Client


client = Client(public_key='430058a405272c58ba6c53c487a4f1b850523624', private_key='ce1596ca1a904fc7960f9c35ca3260f0da63c6e4')

#print(client.market.get(id=227601))
#print(client.market.get_order_book(id=227601, params={'currency_mode': 'play_money'}))
#print(client.market.get_related_markets(id=227601))
"""
print(client.market.suggest_market(payload={
  "title": "string",
  "description": "string",
  "category": "string",
  "end_bet_date": "2019-08-24T14:15:22Z",
  "outcomes": [
    {
      "title": "string",
      "price": 0.01
    },
    {
      "title": "string",
      "price": 0.01
    }
  ]
}))
"""
#print(client.bets.purchase(payload={'outcome': 554342, 'shares': 0.4, 'currency': 'OOM', 'position': 'l'}))
#print(client.bets.detail(id=879249))
#print(client.limit_order.create(payload={'outcome': 550045, 'currency': 'OOM', 'shares': 0.2, 'shares_requested': 0.2, 'side': 'bid', 'position': 'l'}))
#print(client.limit_order.cancel(id=5877601))
print(client.limit_order.get_user_orders(params={'currency': 'OOM', 'question': 222751, 'outcome': 550045, 'side': 'bid', 'amount': 10}))