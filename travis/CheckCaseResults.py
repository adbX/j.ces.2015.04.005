import argparse
import csv
import sys

files_to_check = [ 'abscissa.node0.populationBalance',
                   'abscissa.node1.populationBalance',
                   'sigma.node0.populationBalance',
                   'sigma.node1.populationBalance',
                   'weight.node0.populationBalance',
                   'weight.node1.populationBalance',
                   'moment.0.populationBalance',
                   'moment.1.populationBalance',
                   'moment.2.populationBalance',
                   'moment.3.populationBalance',
                   'moment.4.populationBalance']

tolerance = 1e-10

computed_dir = './case6N2/postProcessing/probes/0'
expected_dir = './travis/case6N2expected'

def load_file_data(filepath):
    data = []
    with open(filepath, "r") as infile:
        content = infile.readlines()
        for line in content:
            stripped_line = line.strip()
            if stripped_line[0] == "#":
                continue
            items = stripped_line.split()
            data.append(float(items[-1]))
    return data

fail = False
for file in files_to_check:
    expected_data = load_file_data('/'.join([expected_dir, file]))
    computed_data = load_file_data('/'.join([computed_dir, file]))
    if len(expected_data) != len(computed_data):
        fail = True
        print("file {} doesn't contain enough data!".format(file))
        continue

    for i in range(len(expected_data)):
        if(abs(computed_data[i]-expected_data[i])/expected_data[i] > tolerance):
            fail = True
            print("Value from {} doesn't match the expected value! Got {} expected {}!".format(file, computed_data[i], expected_data[i]))

if (fail):
    print("Test failed!")
    sys.exit(1)

print("Test passed!")
