import glob
from pathlib import Path

import napari
import numpy as np
import tifffile
from napari.utils.notifications import show_error, show_info, show_warning
from scipy import ndimage

MASK_FOLDER = "../mito_masks"  # relative to the folder of the loaded .ptu


def loaded_ptu(viewer) -> Path | None:
    """Path of the .ptu loaded in the FLOPA File tab, or None."""
    from napari_flopa.ui.main_widget import FlimWidget

    for widget in getattr(viewer.window, "dock_widgets", {}).values():
        if isinstance(widget, FlimWidget):
            path = widget._ptu_panel.ptu_filepath
            return Path(path) if path else None
    return None


def find_masks(ptu: Path) -> tuple[Path, dict[int, Path], list[Path]]:
    """Per-cell mask files of *ptu*, keyed by the cell id in the name.

    A mask belongs to the image when its name starts with '<ptu stem>_', the
    cell id is the number after the last underscore.
    """
    mask_dir = (ptu.parent / MASK_FOLDER).resolve()
    pattern = f"{glob.escape(ptu.stem)}_*.tif*"
    cells: dict[int, Path] = {}
    skipped: list[Path] = []
    for f in sorted(mask_dir.glob(pattern)):
        tail = f.stem.rsplit("_", 1)[-1]
        if tail.isdigit():
            cells[int(tail)] = f
        else:
            skipped.append(f)
    return mask_dir, dict(sorted(cells.items())), skipped


def combine(masks: dict[int, Path]) -> tuple[np.ndarray, np.ndarray, int]:
    """Merge binary cell masks into (cells, objects, overlapping pixels).

    cells: each pixel holds the cell id from the file name.
    objects: connected components, found per cell so touching cells stay
    apart, numbered 1..N. Where cells overlap, the later file wins.
    """
    cells = objects = claimed = None
    overlap = 0
    n_obj = 0
    for cell_id, path in masks.items():
        m = np.squeeze(tifffile.imread(path)) > 0
        if m.ndim != 2:
            raise ValueError(f"{path.name}: expected a 2D mask, got {m.shape}")
        if cells is None:
            cells = np.zeros(m.shape, dtype=np.uint16)
            objects = np.zeros(m.shape, dtype=np.int32)
            claimed = np.zeros(m.shape, dtype=bool)
        elif m.shape != cells.shape:
            raise ValueError(
                f"{path.name}: shape {m.shape}, other masks are {cells.shape}"
            )
        overlap += int((claimed & m).sum())
        claimed |= m
        cells[m] = cell_id
        comp, n = ndimage.label(m)
        objects[m] = comp[m] + n_obj
        n_obj += n
    # Overwritten objects leave gaps, renumber to 1..N.
    ids, inverse = np.unique(objects, return_inverse=True)
    objects = inverse.reshape(objects.shape).astype(np.uint32)
    if ids[0] != 0:
        objects += 1
    return cells, objects, overlap


def add_or_replace(viewer, data, name, like=None):
    if name in viewer.layers:
        viewer.layers.remove(name)
    kwargs = {}
    if like is not None:
        kwargs = {"scale": like.scale[-2:], "translate": like.translate[-2:]}
    return viewer.add_labels(data, name=name, **kwargs)


def main():
    viewer = napari.current_viewer()
    if viewer is None:
        print("No napari viewer, drop this script onto napari.")
        return
    ptu = loaded_ptu(viewer)
    if ptu is None:
        show_error("Load a .ptu in the FLOPA File tab first.")
        return

    mask_dir, masks, skipped = find_masks(ptu)
    if not masks:
        show_error(
            f"No masks '{ptu.stem}_*.tif' (ending _<cell id>) in {mask_dir}"
        )
        return

    cells, objects, overlap = combine(masks)

    like = viewer.layers["Intensity"] if "Intensity" in viewer.layers else None
    if like is not None and like.data.shape[-2:] != cells.shape:
        show_warning(
            f"Mask shape {cells.shape} differs from the Intensity layer "
            f"{like.data.shape[-2:]}."
        )
        like = None

    add_or_replace(viewer, objects, f"{ptu.stem} objects", like)
    add_or_replace(viewer, cells, f"{ptu.stem} cells", like)

    msg = (
        f"{ptu.stem}: {len(masks)} cells, {int(objects.max())} objects, "
        f"{overlap} overlapping px"
    )
    if skipped:
        msg += f" ({len(skipped)} file(s) without a cell id skipped)"
    print(msg)
    for f in skipped:
        print("  skipped:", f.name)
    show_info(msg)


main()
