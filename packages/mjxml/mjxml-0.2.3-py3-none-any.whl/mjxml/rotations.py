from mjxml.typeutils import ArrayLike, floatarr_to_str, floatarr_to_tuple
from typing import Literal, SupportsFloat
import numpy as np
import numpy.typing as npt

__all__ = [
    "RotationType",
    "to_mjc",

    "to_euler_z",
    "closest",
    "to_quaternion",
    "multiply_quat",
    "localize",
    "rotate_vector_by_quat"
]

RotationType = tuple[
    Literal["quat", "axisangle", "euler", "q", "aa", "e"],
    ArrayLike[SupportsFloat, Literal[3, 4, 6]],
]


def to_mjc(rot: RotationType):
    rot_type, values = rot
    if rot_type in ["quat", "q"]:
        mjc_type = "quat"
    elif rot_type in ["axisangle", "aa"]:
        mjc_type = "axisangle"
    elif rot_type in ["euler", "e"]:
        mjc_type = "euler"
    else:
        raise ValueError(f"Unsupported rotation type: {rot_type}")
    return (mjc_type, floatarr_to_str(values))

def to_quaternion(rotation: RotationType) -> npt.NDArray[np.float64]:
    """Converts a rotation of type RotationType to a quaternion rotation.
    Returns a numpy array with values [w, x, y, z]"""
    rotation_type, values = rotation
    values = np.asarray(values, dtype=np.float64)
    match rotation_type:
        case 'e' | 'euler':
            roll: float
            pitch: float
            yaw: float
            roll, pitch, yaw = np.radians(values)
            
            cy: float = np.cos(yaw * 0.5)
            sy: float = np.sin(yaw * 0.5)
            cp: float = np.cos(pitch * 0.5)
            sp: float = np.sin(pitch * 0.5)
            cr: float = np.cos(roll * 0.5)
            sr: float = np.sin(roll * 0.5)
            
            w: float = cr * cp * cy + sr * sp * sy
            x: float = sr * cp * cy - cr * sp * sy
            y: float = cr * sp * cy + sr * cp * sy
            z: float = cr * cp * sy - sr * sp * cy
            
            return np.array([w, x, y, z])
            
        case 'q' | 'quat':
            return np.array(values)
            
        case 'a' | 'aa' | 'axisangle':
            angle: float = np.radians(values[0])
            x: float = values[1]
            y: float = values[2]
            z: float = values[3]
            
            norm: float = np.sqrt(x*x + y*y + z*z)
            if norm == 0:
                return np.array([1.0, 0.0, 0.0, 0.0])
            
            x /= norm
            y /= norm
            z /= norm
            
            s: float = np.sin(angle / 2)
            w: float = np.cos(angle / 2)
            
            return np.array([w, x * s, y * s, z * s])
            
        case _:
            raise ValueError(f"Unknown rotation type: {rotation_type}")

def to_euler_z(quat: ArrayLike[SupportsFloat, Literal[4]]) -> float:
    """Returns yaw angle from quaternion"""
    w, x, y, z = floatarr_to_tuple(quat) # type: ignore
    siny_cosp: float = 2 * (w * z + x * y)
    cosy_cosp: float = 1 - 2 * (y * y + z * z)
    yaw = np.arctan2(siny_cosp, cosy_cosp)
    return yaw

def closest(theta1: float, theta2: float) -> float:
    """Returns closest difference in theta2 - theta1"""
    return ((theta2 - theta1 + np.pi) % (2*np.pi)) - np.pi

def multiply_quat(
        q1: ArrayLike[SupportsFloat, Literal[4]],
        q2: ArrayLike[SupportsFloat, Literal[4]]) -> npt.NDArray[np.float64]:
    """Multiplies two quaternions"""
    w1, x1, y1, z1 = floatarr_to_tuple(q1)  # type: ignore
    w2, x2, y2, z2 = floatarr_to_tuple(q2)  # type: ignore
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2
    return np.array([w, x, y, z])

def localize(
        inertial: ArrayLike[SupportsFloat, Literal[7]], 
        qpos: ArrayLike[SupportsFloat, Literal[7]]) -> npt.NDArray[np.float64]:
    """
    Given reference frame I_1 (inertial) and I_2 (qpos) in world frame,
    returns qpos of I_2 in frame I_1.
    
    Both inertial and qpos are expected to be in [x, y, z, qw, qx, qy, qz] format.
    """
    inertial_pos = inertial[:3]
    inertial_quat = inertial[3:7]  # [w, x, y, z]
    pos = qpos[:3]
    quat = qpos[3:7]

    pos = pos - inertial_pos
    
    inertial_quat_inv = np.array([
        inertial_quat[0],
        *(-inertial_quat[1:]),
    ])
    pos = rotate_vector_by_quat(inertial_quat_inv, pos)
    
    quat = multiply_quat(inertial_quat_inv, quat)
    
    return np.array([*pos, *quat])

def rotate_vector_by_quat(q: np.ndarray, v: np.ndarray) -> np.ndarray:
    """Rotates vector v by quaternion q"""
    v_quat = np.array([0.0, *v])
    
    temp = multiply_quat(q, v_quat)
    
    q_conj = np.array([q[0], -q[1], -q[2], -q[3]])
    result = multiply_quat(temp, q_conj)
    
    return result[1:4]
