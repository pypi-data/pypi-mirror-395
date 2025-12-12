def relative_pos_to_absolute(relative_pos: float, det_width: int):
    """
    Convert relative center of rotation to absolute.
    """
    # Compute the midpoint differently for even and odd widths
    midpoint = det_width / 2.0
    return relative_pos + midpoint


def absolute_pos_to_relative(absolute_pos: float, det_width: int):
    """
    Convert absolute center of rotation to relative.
    """
    # Compute the midpoint differently for even and odd widths
    midpoint = det_width / 2.0
    return absolute_pos - midpoint
