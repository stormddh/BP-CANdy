"""
   CANvas Automotive Network Mapper v1.0
   Source Mapping Component

   Author: Sekar Kulandaivel (github.com/sekarkulandaivel)

   Copyright (c) 2017-2019, Carnegie Mellon University. All rights reserved.
"""

from .include.setup import *
from .include.extractor import *
from .include.classifier import *
from .include.tracker import *
from .include.enumerator import *

DUMP = False

def mapper(file_name):

    # retrieve existing data or save new data
    if os.path.isfile('pickle/dump.dat'):
        with open('pickle/dump.dat', 'rb') as fp:
            if pickle.load(fp) == file_name:
                id_log = pickle.load(fp)
                id_class = pickle.load(fp)
                id_period = pickle.load(fp)
                id_mean = pickle.load(fp)
                id_stdev = pickle.load(fp)
                id_list = pickle.load(fp)
            else:
                id_log, id_class, id_period, id_mean, id_stdev, id_list = store(file_name)
    else:
        id_log, id_class, id_period, id_mean, id_stdev, id_list = store(file_name)

    matches = []

    # iterate through each pair
    total_pairs = total_tracked = 0
    for i1 in range(len(id_list)):
        for i2 in range(i1, len(id_list)):

            # only compare pairs that don't match
            id1 = id_list[i1]
            id2 = id_list[i2]
            if id1 != id2:

                log1 = id_log[id1]
                log2 = id_log[id2]
                period1 = id_period[id1]
                period2 = id_period[id2]
                mean1 = id_mean[id1]
                mean2 = id_mean[id2]
                stdev1 = id_stdev[id1]
                stdev2 = id_stdev[id2]

                if id_class[id1] == id_class[id2] == 'strong periodic':
                    if tracker(id1, id2, log1, log2, period1, period2, \
                        mean1, mean2, stdev1, stdev2):
                        matches.append((id1, id2))
                    total_tracked += 1

                total_pairs += 1

    print('Total Pairs: {}'.format(total_pairs))
    print('Total Tracked: {}'.format(total_tracked))

    return enumerator(matches)

def store(file_name):

    id_log = extractor(open(file_name, 'r'))
    id_class, id_period, id_mean, id_stdev = classifier(id_log)
    id_list = sorted(id_log.keys())

    if DUMP:
        with open('pickle/dump.dat', 'wb') as fp:
            pickle.dump(sys.argv[1], fp)
            pickle.dump(id_log, fp)
            pickle.dump(id_class, fp)
            pickle.dump(id_period, fp)
            pickle.dump(id_mean, fp)
            pickle.dump(id_stdev, fp)
            pickle.dump(id_list, fp)
    return id_log, id_class, id_period, id_mean, id_stdev, id_list

if __name__ == "__main__":
    file_name = sys.argv[1]
    mapper(file_name)
