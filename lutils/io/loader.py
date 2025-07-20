import numpy as np

from .parser import parse_internal_field


def load_internal_field(case_path: str,
                        file_path: str,
                        fields: list) -> tuple[np.ndarray, np.ndarray]:
    header, data = parse_internal_field(case_path, file_path)

    idx = []
    for f in fields:
        idx.append(header.index(f))
    idx.sort()

    x_idx = header.index('x')
    y_idx = header.index('y')
    z_idx = header.index('z')


    coords = data[:, [x_idx, y_idx, z_idx]]
    values = data[:, idx]

    return coords, values
