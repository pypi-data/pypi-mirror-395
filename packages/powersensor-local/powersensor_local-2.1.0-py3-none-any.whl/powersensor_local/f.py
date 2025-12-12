#pylint: skip-file
import asyncio
from virtual_household import VirtualHousehold
from pprint import pprint

def evhnd(ev: str, obj: dict):
    print('GOT EVENT', ev, obj)

vh=VirtualHousehold(True)
vh.subscribe('from_grid', evhnd)
vh.subscribe('to_grid', evhnd)
vh.subscribe('solar_generation', evhnd)
vh.subscribe('home_usage', evhnd)
hn={'mac': 'bcddc247d1f5', 'role': 'house-net', 'starttime_utc': 1758762475, 'watts': -43, 'duration_s': 30, 'via': '246f280487a4'}
t=vh.process_average_power_event(hn)
asyncio.run(t)
print('----')
pprint(vars(vh))

so={'mac': 'bcddc247d289', 'role': 'solar', 'starttime_utc': 1758763735, 'watts': -322, 'duration_s': 30, 'via': 'a4cf1218f158'}
t=vh.process_average_power_event(so)
asyncio.run(t)
print('----')
pprint(vars(vh))

hn={'mac': 'bcddc247d1f5', 'role': 'house-net', 'starttime_utc': 1758763735, 'watts': -43, 'duration_s': 30, 'via': '246f280487a4'}
t=vh.process_average_power_event(hn)
asyncio.run(t)
print('----')
pprint(vars(vh))
