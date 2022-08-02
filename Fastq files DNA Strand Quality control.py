from collections import Counter
import gzip


file_input1, file_input2, file_input3 = input(), input(), input()
total_file_inputs = [file_input1, file_input2, file_input3]
file_info = []
best_file = {}

for file in range(len(total_file_inputs)):
    sequence_average_length = 0
    strands = []
    gc_content = []
    occurrence_counter = []
    n_calc = []
    reads_with_ns = 0
    with gzip.open(total_file_inputs[file], 'r') as f:
        strands = f.read().decode('utf-8').splitlines()[1::4]
        reads_n = len(strands)
    for i in range(len(strands)):
        occurrence_counter.append(Counter(strands[i]))
        sequence_average_length += sum(occurrence_counter[i].values())
        if "N" in occurrence_counter[i]:
            n_calc.append(round((occurrence_counter[i]["N"] / len(strands[i])) * 100,2))
            reads_with_ns += 1
        try:
            gc_content.append((occurrence_counter[i]['G'] + occurrence_counter[i]['C']) / sum(occurrence_counter[i].values()) * 100)

        except KeyError:
            pass
    file_info.append({"filename": total_file_inputs[file],
                      "reads": reads_n,
                      "reads_length": round(sequence_average_length / reads_n),
                      "repeats": len(strands) - len(set(strands)),
                      "reads_with_ns": reads_with_ns,
                     "gc_content_avg": round(sum(gc_content) / reads_n, 2),
                      "ns_per_read": round(sum(n_calc) / len(strands), 2),
                      "sum_repeats": (len(strands) - len(set(strands))) + reads_with_ns})
for i in range(len(file_info)):
    best_file[i] = file_info[i]['sum_repeats']

best = list({k: v for k, v in sorted(best_file.items(), key=lambda item: item[1])})[0]

print(f'Reads in the file = {file_info[best]["reads"]}\n'
      f'Reads sequence average length = {file_info[best]["reads_length"]}\n\n'
      f'Repeats = {file_info[best]["repeats"]}\n'
      f'Reads with Ns = {file_info[best]["reads_with_ns"]}\n\n'
      f'GC content average = {file_info[best]["gc_content_avg"]}%')
if file_info[best]["ns_per_read"] == 0:
    print(f'Ns per read sequence = 0%')
else:
    print(f'Ns per read sequence = {file_info[best]["ns_per_read"]}%')
