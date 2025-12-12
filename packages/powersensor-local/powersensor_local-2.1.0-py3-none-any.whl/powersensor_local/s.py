#pylint: skip-file
import sys
from pathlib import Path
project_root = str(Path(__file__).parents[1])
if project_root not in sys.path:
    sys.path.append(project_root)

import asyncio
from virtual_household import VirtualHousehold
from pprint import pprint

def evhnd(ev: str, obj: dict):
    print('GOT EVENT', ev, obj)

def dump(vh):
    return
    print('----')
    #pprint(vars(vh))
    #pprint(vh._summation)
    #pprint(vh._counters)
    print('solar_summations')
    pprint(vars(vh._solar_summations))
    print('housenet_summations')
    pprint(vars(vh._housenet_summations))
    print('---end----')

vh=VirtualHousehold(True)
vh.subscribe('from_grid_summation', evhnd)
vh.subscribe('to_grid_summation', evhnd)
vh.subscribe('solar_generation_summation', evhnd)
vh.subscribe('home_usage_summation', evhnd)
print('injecting HOUSENET')
hn= {'mac': 'bcddc247d1f5', 'role': 'house-net', 'starttime_utc': 1758762475, 'summation_joules': 33170430, 'summation_resettime_utc': 1758100824, 'via': '246f280487a4'}
t=vh.process_summation_event(hn)
asyncio.run(t)
dump(vh)

print('injecting SOLAR')
so={'mac': 'bcddc247d289', 'role': 'solar', 'starttime_utc': 1758762475, 'summation_joules': -273879464, 'summation_resettime_utc': 1758087294, 'via': 'a4cf1218f158'}
t=vh.process_summation_event(so)
asyncio.run(t)
dump(vh)

print('injecting HOUSENET')
hn= {'mac': 'bcddc247d1f5', 'role': 'house-net', 'starttime_utc': 1758763495, 'summation_joules': 33169631, 'summation_resettime_utc': 1758100824, 'via': '246f280487a4'}
t=vh.process_summation_event(hn)
asyncio.run(t)
dump(vh)

print('injecting SOLAR')
so={'mac': 'bcddc247d289', 'role': 'solar', 'starttime_utc': 1758763495, 'summation_joules': -273889119, 'summation_resettime_utc': 1758087294, 'via': 'a4cf1218f158'}
t=vh.process_summation_event(so)
asyncio.run(t)
dump(vh)

print('injecting HOUSENET')
hn={'mac': 'bcddc247d1f5', 'role': 'house-net', 'starttime_utc': 1758781405, 'summation_joules': 39257646, 'summation_resettime_utc': 1758100824, 'via': '246f280487a4'}
t=vh.process_summation_event(hn)
asyncio.run(t)
dump(vh)

print('injecting SOLAR')
so={'mac': 'bcddc247d289', 'role': 'solar', 'starttime_utc': 1758781405, 'summation_joules': -279410973, 'summation_resettime_utc': 1758087294, 'via': 'a4cf1218f158'}
t=vh.process_summation_event(so)
asyncio.run(t)
dump(vh)

