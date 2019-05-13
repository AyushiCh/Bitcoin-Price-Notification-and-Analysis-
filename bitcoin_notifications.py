import requests
import time
from datetime import datetime

bc_price_thres = 5259 #To be updated as per convenience
bc_api_weblink = 'https://api.coinmarketcap.com/v1/ticker/bitcoin/'
ifttt_wh_weblink = 'https://maker.ifttt.com/trigger/{}/with/key/dFIvnK9qKedzh56y2opC3E'

def get_updated_bc_prc():
  resp = requests.get(bc_api_weblink)
  resp_json = resp.json()
  return float(resp_json[0]['price_usd'])

def ifttt_wh_post(event, value):
  req_data = {'value1': value}
  ifttt_event_weblink = ifttt_wh_weblink.format(event)
  requests.post(ifttt_event_weblink, json = req_data)

def format_bitcoin_history(bc_hist):
  rows = []
  for bc_price in bc_hist:
      date = bc_price['date'].strftime('%d.%m.%Y %H:%M:%S')
      price = bc_price['price']
      row = '{}: $<b>{}</b>'.format(date, price)
      rows.append(row)
  return '<br>'.join(rows)

def main():
  bc_hist = []
  while True:
     price = get_updated_bc_prc()
     date=datetime.now()
     bc_hist.append({'date': date, 'price': price})

     if price < bc_price_thres:
            ifttt_wh_post('emergency_bitcoin_coin', price)

     if len(bc_hist) == 5:
            ifttt_wh_post('updated_bitcoin_price', format_bitcoin_history(bc_hist))
            bc_hist = []

     time.sleep(5)


if __name__ == '__main__':
	main()


