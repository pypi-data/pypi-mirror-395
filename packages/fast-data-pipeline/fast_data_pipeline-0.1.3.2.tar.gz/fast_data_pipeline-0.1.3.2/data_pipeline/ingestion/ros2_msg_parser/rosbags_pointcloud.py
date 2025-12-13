from typing import List, Tuple, Generator, Optional, Any
import math
import struct
import logging

logger = logging.getLogger()


_POINT_FIELD_DATATYPES = {
    1: ('b', 1),  # INT8
    2: ('B', 1),  # UINT8
    3: ('h', 2),  # INT16
    4: ('H', 2),  # UINT16
    5: ('i', 4),  # INT32
    6: ('I', 4),  # UINT32
    7: ('f', 4),  # FLOAT32
    8: ('d', 8),  # FLOAT64
}

def read_points_rosbags(cloud: Any, field_names: Optional[List[str]] = None, 
                       skip_nans: bool = False, uvs: List[Tuple[int, int]] = []) -> Generator[Tuple, None, None]:
    """
    Read points from a rosbags PointCloud2 message without converting to native type.
    
    Args:
        cloud: Rosbags PointCloud2 message
        field_names: Names of fields to read. If None, read all fields.
        skip_nans: If True, skip points with NaN values
        uvs: List of (u, v) coordinates to read specific points
        
    Returns:
        Generator yielding tuples of point values
    """
    # Build format string for unpacking
    fmt = _get_struct_fmt_rosbags(cloud.is_bigendian, cloud.fields, field_names)
    point_step = cloud.point_step
    row_step = cloud.row_step
    data = cloud.data
    unpack_from = struct.Struct(fmt).unpack_from

    if skip_nans:
        for v in range(cloud.height):
            offset = v * row_step
            for u in range(cloud.width):
                point_data = unpack_from(data, offset)
                if not any(math.isnan(val) for val in point_data):
                    yield point_data
                offset += point_step
    else:
        for v in range(cloud.height):
            offset = v * row_step
            for u in range(cloud.width):
                yield unpack_from(data, offset)
                offset += point_step

def _get_struct_fmt_rosbags(is_bigendian: bool, fields: List[Any], 
                           field_names: Optional[List[str]] = None) -> str:
    """
    Generate format string for struct unpacking from rosbags fields.
    """
    fmt = '>' if is_bigendian else '<'
    offset = 0
    
    # Sort fields by offset and filter by field_names
    sorted_fields = sorted(fields, key=lambda f: f.offset)
    if field_names is not None:
        sorted_fields = [f for f in sorted_fields if f.name in field_names]
    
    for field in sorted_fields:
        if offset < field.offset:
            fmt += 'x' * (field.offset - offset)
            offset = field.offset
        
        if field.datatype not in _POINT_FIELD_DATATYPES:
            logger.warning(f'Skipping unknown PointField datatype: {field.datatype}')
            continue
            
        datatype_fmt, datatype_length = _POINT_FIELD_DATATYPES[field.datatype]
        fmt += str(field.count) + datatype_fmt
        offset += field.count * datatype_length
        
    return fmt