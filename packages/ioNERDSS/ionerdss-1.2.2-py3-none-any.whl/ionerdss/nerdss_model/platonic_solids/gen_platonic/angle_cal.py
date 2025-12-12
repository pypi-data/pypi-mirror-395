import math
import numpy as np


def angle_cal(COM1: float, leg1: float, COM2: float, leg2: float):
    """Calculates angles between vectors based on given inputs.

    Args:
        COM1 (float): Center of Mass (COM) for the first leg.
        leg1 (float): Endpoint of the first leg.
        COM2 (float): Center of Mass (COM) for the second leg.
        leg2 (float): Endpoint of the second leg.

    Returns:
        tuple: A tuple containing the following angles (in radians) rounded to 8 decimal places:
            - theta1 (float): Angle between vector from COM1 to leg1 and vector from leg1 to leg2.
            - theta2 (float): Angle between vector from COM2 to leg2 and vector from leg2 to leg1.
            - phi1 (float): Angle between vectors perpendicular to leg1 and leg2, passing through COM1.
            - phi2 (float): Angle between vectors perpendicular to leg2 and leg1, passing through COM2.
            - omega (float): Angle between vectors perpendicular to leg1 and leg2, passing through leg1 and leg2.
    """
    
    n = 8
    c1 = np.array(COM1)
    p1 = np.array(leg1)
    c2 = np.array(COM2)
    p2 = np.array(leg2)
    v1 = p1 - c1
    v2 = p2 - c2
    sig1 = p1 - p2
    sig2 = -sig1
    theta1 = round(math.acos(np.dot(v1, sig1) /
                   (np.linalg.norm(v1)*np.linalg.norm(sig1))), n)
    theta2 = round(math.acos(np.dot(v2, sig2) /
                   (np.linalg.norm(v2)*np.linalg.norm(sig2))), n)
    t1 = np.cross(v1, sig1)
    t2 = np.cross(v1, c1)  # n1 = c1 here
    t1_hat = t1/np.linalg.norm(t1)
    t2_hat = t2/np.linalg.norm(t2)
    phi1 = round(math.acos(np.around(np.dot(t1_hat, t2_hat), n)), n)
    t3 = np.cross(v2, sig2)
    t4 = np.cross(v2, c2)  # n2 = c2 here
    t3_hat = t3/np.linalg.norm(t3)
    t4_hat = t4/np.linalg.norm(t4)
    phi2 = round(math.acos(np.around(np.dot(t3_hat, t4_hat), n)), n)
    t1_ = np.cross(sig1, v1)
    t2_ = np.cross(sig1, v2)
    t1__hat = t1_/np.linalg.norm(t1_)
    t2__hat = t2_/np.linalg.norm(t2_)
    omega = round(math.acos(np.around(np.dot(t1__hat, t2__hat), n)), n)
    return theta1, theta2, phi1, phi2, omega


# DODECAHEDEON FACE AS COM

