from upyog.imports import *
from upyog.image.draw import *
from upyog.image.visualiser import Visualiser


__all__ = [
    "draw_rule_of_thirds",
    "img_join_horizontal",
    "img_join_vertical",
    "make_img_grid",
]


ImageCollection = Collection[Image.Image]


def draw_rule_of_thirds(img: Image.Image, thickness=5, opacity=0.4) -> Image.Image:
    vis = Visualiser(img)
    vis.draw_rule_of_thirds(thickness, opacity)
    return vis.img


def assemble_rows(imgs: ImageCollection, ncol: int) -> list:
    """Assemble images into rows based on the number of columns."""
    rows, row = [], []
    for i, img in enumerate(imgs, start=1):
        row.append(img)
        if i % ncol == 0:
            rows.append(row)
            row = []
    if row:
        rows.append(row)
    return rows


def img_join_horizontal(imgs: ImageCollection) -> Image.Image:
    return reduce(operator.__or__, imgs)


def img_join_vertical(imgs: ImageCollection) -> Image.Image:
    return reduce(operator.__floordiv__, imgs)


def make_img_grid(
    imgs: ImageCollection,
    ncol=3,
    size_WH: Optional[tuple] = (640, 384),
    pad=True,
    verbose=False,
):
    # fmt: off
    if size_WH:
        if pad: imgs = [img.resize_pad(size_WH) for img in imgs]
        else:   imgs = [img.resize(size_WH) for img in imgs]
    else:
        pass
    # fmt: on

    if ncol == 1:
        return img_join_vertical(imgs)

    if verbose:
        from rich.progress import Progress

        with Progress() as prog:
            # Create rows with individual images
            rows, row = [], []
            for i, img in enumerate(imgs, start=1):
                row += [img]
                if i % ncol == 0:
                    rows += [row]
                    row = []
            if not row == []:
                rows += [row]

            n_tasks = len(rows) + 1
            task_concat = prog.add_task("Concatenating Rows...", total=n_tasks)
            # print(task_concat.total)
            grid = []

            while not prog.finished:
                for row in rows:
                    grid += [img_join_horizontal(row)]
                    prog.update(task_concat, advance=1)

                grid = img_join_vertical(grid)
                prog.update(task_concat, advance=1)

    else:
        rows, row = [], []
        for i, img in enumerate(imgs, start=1):
            row += [img]
            if i % ncol == 0:
                rows += [row]
                row = []
        if not row == []:
            rows += [row]

        grid = [img_join_horizontal(row) for row in rows]
        grid = img_join_vertical(grid)

    return grid


# # TODO: Test this
# def make_img_grid(
#     imgs: ImageCollection,
#     ncol=3,
#     size_WH: Optional[Tuple[int, int]] = (640, 384),
#     pad=True,
#     verbose=False
# ) -> Image.Image:
#     # fmt: off
#     if size_WH:
#         if pad: imgs = [img.resize_pad(size_WH) for img in imgs]
#         else:   imgs = [img.resize(size_WH) for img in imgs]
#     else:
#         pass
#     # fmt: on

#     rows = assemble_rows(imgs, ncol)
    
#     if verbose:
#         from rich.progress import Progress
#         with Progress() as prog:
#             n_tasks = len(rows) + 1
#             task_concat = prog.add_task("Concatenating Rows...", total=n_tasks)

#             while not prog.finished:
#                 for row in rows:
#                     grid += [img_join_horizontal(row)]
#                     prog.update(task_concat, advance=1)

#                 grid = img_join_vertical(grid)
#                 prog.update(task_concat, advance=1)

#     else:
#         grid = [img_join_horizontal(row) for row in rows]
#         grid = img_join_vertical(grid)
    
#     return grid
