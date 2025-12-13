from GSpreadPlus import Spreadclient

client = Spreadclient('test-creds.json')

client.connect_document('1CFViEMEGkuhBz8ylhgpo6NoRi-QG94p3X8jmAduuaB8')
client.connect_sheet('Array 0')

# # data = client.get_rows_by_func(lambda r:'GEM' in r[client.get_header_index('Relations')])
data = client.commit_new_row([
    "Kendra",
    "5/13",
    'TMJC,22S301'
],offset=2)
client.refresh_sheet()
print(data)
