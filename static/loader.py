import pickle

import yaml

with open('typeIDs.yaml', encoding='utf-8') as fp:
    data = yaml.load(fp)

with open('sde_names.pkl', 'wb+') as fp:
    d = {typeID: contents['name']['en'] for typeID, contents in data.items()}
    pickle.dump(d, fp)

with open('sde_sizes.pkl', 'wb+') as fp:
    # The SDE volumes are unpackaged volumes for ships and containers??? fffuuFUFUUCCK
    with open('invVolumes.csv') as csv:
        packagedVols = {
            int(line.split(',')[0]): int(line.split(',')[1])
            for line in csv.read().split('\n')[1:]
        }
    d = {typeID: packagedVols.get(typeID, contents.get('volume', 0)) for typeID, contents in data.items()}
    pickle.dump(d, fp)
