
data = open('data/day06.txt').read()

start_packet_index = -1
for i in range(4, len(data)):
    start_packet = set(list(data[i-4:i]))
    if len(start_packet) == 4:
        start_packet_index = i
        break

start_message_index = -1
for i in range(14, len(data)):
    start_packet = set(list(data[i-14:i]))
    if len(start_packet) == 14:
        start_message_index = i
        break

print(f"Solution 1: {start_packet_index}")
print(f"Solution 2: {start_message_index}")