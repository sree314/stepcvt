import json
from ..project import *


def check_source(p):
    if not p.sources:
        raise Exception("ERROR: No existing source, add one first")


def add_part(p, args):
    check_source(p)
    source = p.sources[0]

    if args.all == True:  # add all parts
        if source.partinfo:  # not empty
            existing_ids = set([pi.part_id for pi in source.partinfo])
            for partid, obj in source.parts():
                if partid not in existing_ids:
                    source.add_partinfo(partid, obj)
        else:
            for partid, obj in source.parts():
                source.add_partinfo(partid, obj)
    else:
        ids = args.id  # parts that need to be added
        if not ids:
            raise Exception(
                "ERROR: Need to specify at least one partid if --all is not included"
            )
        else:
            ids = set(ids)
            existing_ids = set([pi.part_id for pi in source.partinfo])
            for partid, obj in source.parts():
                if partid in ids:
                    if partid in existing_ids:
                        print(f"{partid} has already been added")
                    else:
                        source.add_partinfo(partid, obj)
    return 1


def remove_part(p, args):
    check_source(p)
    source = p.sources[0]
    spi = source.partinfo
    rids = set(args.id)  # parts that need to be removed

    for pi in spi:
        if pi.part_id in rids:
            spi.remove(pi)
    return 1


def edit_part(p, args):
    check_source(p)
    source = p.sources[0]
    edit_id = args.id
    if args.count == None:
        raise NotImplementedError("Can only modify count for now")

    all_ids = set([p[0] for p in source.parts()])
    existing_ids = set([pi.part_id for pi in source.partinfo])

    if edit_id not in all_ids:
        raise Exception("ERROR: Cannot edit a part that doesn't exist")
    if edit_id not in existing_ids:
        raise NotImplementedError("Need to add the part first")

    for pi in source.partinfo:
        if edit_id == pi.part_id:
            pi._default_count = args.count
    return 1
