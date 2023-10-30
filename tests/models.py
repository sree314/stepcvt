#!/usr/bin/env python3

# referred to https://cadquery.readthedocs.io/en/latest/assy.html

import cadquery as cq


def book_model():
    book_length = 10
    book_width = 8
    book_thickness = 1
    spine_thickness = 0.8
    assy = cq.Assembly()

    book_body = cq.Workplane("XY").box(book_length, book_width, book_thickness)

    spine = (
        cq.Workplane("XY")
        .box(
            book_length, spine_thickness, book_thickness + 0.2
        )  # Making spine slightly larger
        .translate((0, book_width / 2 - spine_thickness / 2, 0))
    )

    assy.add(book_body, name="book_body")
    assy.add(spine, name="spine")
    return assy


def torch_model():
    flame = cq.Solid.makeCone(2, 0, 5).translate((0, 0, 2))
    assy = cq.Assembly()

    assy.add(flame, name="flame")
    assy.add(
        cq.Solid.makeCone(2, 1, 15),
        loc=cq.Location((0, 0, 0), (1, 0, 0), 180),
        name="handle",
    )
    assy.add(
        cq.Solid.makeCone(3.5, 2.5, 2).translate((0, 0, -2)),
        loc=cq.Location((0, 0, 0), (1, 0, 0), 180),
        name="middle",
    )
    return assy


def desk_model():
    desk_top_length = 10
    desk_top_width = 8
    desk_top_thickness = 1

    leg_length = 6
    leg_width = 1

    assy = cq.Assembly()
    desk_top = cq.Workplane("XY").box(
        desk_top_length, desk_top_width, desk_top_thickness
    )

    def create_leg(x, y):
        return (
            cq.Workplane("XY")
            .box(leg_width, leg_width, leg_length)
            .translate((x, y, leg_length / 2 + desk_top_thickness / 2))
        )

    legs = [
        create_leg(
            desk_top_length / 2 - leg_width / 2, desk_top_width / 2 - leg_width / 2
        ),
        create_leg(
            -desk_top_length / 2 + leg_width / 2, desk_top_width / 2 - leg_width / 2
        ),
        create_leg(
            desk_top_length / 2 - leg_width / 2, -desk_top_width / 2 + leg_width / 2
        ),
        create_leg(
            -desk_top_length / 2 + leg_width / 2, -desk_top_width / 2 + leg_width / 2
        ),
    ]

    assy.add(desk_top, name="desk_top")
    for i in range(4):
        assy.add(legs[i], loc=cq.Location((0, 0, 0), (1, 0, 0), 180), name=f"leg{i}")
    return assy


MODELS = {"book": book_model, "torch": torch_model, "desk": desk_model}

if __name__ == "__main__":
    import argparse

    p = argparse.ArgumentParser(description="Export STEP models to files")
    p.add_argument("model", choices=MODELS.keys(), help="Model to export")
    p.add_argument("output", help="Output STEP file")

    args = p.parse_args()

    modfn = MODELS[args.model]
    assy = modfn()
    assy.save(args.output)
