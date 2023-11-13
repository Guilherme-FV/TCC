from time import sleep
from modules.location_combinator import LocationCombinator


location_combinator = LocationCombinator()

location_combinator.start()

for i in range(0, 20):
    print(i)
    sleep(1)

location_combinator.stop()

location_combinator.print_locations()

print(location_combinator.combine_locations())