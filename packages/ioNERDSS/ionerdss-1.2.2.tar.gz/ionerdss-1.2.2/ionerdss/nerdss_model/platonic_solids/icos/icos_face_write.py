from ..gen_platonic.angle_cal import angle_cal
from .icos_face_leg_reduce_coord_gen import icos_face_leg_reduce_coord_gen
from .icos_face_input_coord import icos_face_input_coord


def icos_face_write(radius: float, sigma: float,create_Solid: bool=False):
    """ Writes input parameters for a simulation of an icosahedron face-centered system.

    Args:
        radius (float): Radius of the icosahedron.
        sigma (float): Sigma parameter for the simulation.

    Returns:
        parm.inp/icos.mol: input files for NERDSS

    This function writes input parameters for a simulation of an icosahedron face-centered system
    to a file named 'parm.inp'. The input parameters include simulation settings such as the number
    of iterations, time step, and output frequency, as well as parameters related to the geometry
    and interaction potentials of the system. The input parameters are derived from the given radius
    and sigma values, which are used to calculate other quantities using helper functions
    `icos_face_input_coord`, `icos_face_leg_reduce_coord_gen`, and `angle_cal`.
    """
    if create_Solid == True:
        COM, lg1, lg2, lg3, n = icos_face_input_coord(radius, sigma)
        coord = icos_face_leg_reduce_coord_gen(radius, sigma)
        theta1, theta2, phi1, phi2, omega = angle_cal(
        coord[0][0], coord[0][2], coord[11][0], coord[11][3])

        output_reactions_dict :dict = {
                "n": n,
                "coord": coord,
                "theta1": theta1,
                "theta2": theta2,
                "phi1": phi1,
                "phi2": phi2,
                "omega": omega
                }
        output_mol_dict: dict = {
                "COM": COM,
                "lg1": lg1,
                "lg2": lg2,
                "lg3": lg3,}
        return output_reactions_dict, output_mol_dict



    else:

        COM, lg1, lg2, lg3, n = icos_face_input_coord(radius, sigma)
        coord = icos_face_leg_reduce_coord_gen(radius, sigma)
        theta1, theta2, phi1, phi2, omega = angle_cal(
                coord[0][0], coord[0][2], coord[11][0], coord[11][3])

        f = open('parm.inp', 'w')
        f.write(' # Input file (icosahedron face-centered)\n\n')
        f.write('start parameters\n')
        f.write('    nItr = 10000000 #iterations\n')
        f.write('    timeStep = 0.1\n')
        f.write('    timeWrite = 10000\n')
        f.write('    pdbWrite = 10000\n')
        f.write('    trajWrite = 10000\n')
        f.write('    restartWrite = 50000\n')
        f.write('    checkPoint = 1000000\n')
        f.write('    overlapSepLimit = 7.0\n')
        f.write('end parameters\n\n')
        f.write('start boundaries\n')
        f.write('    WaterBox = [500,500,500]\n')
        f.write('end boundaries\n\n')
        f.write('start molecules\n')
        f.write('    dode : 200\n')
        f.write('end molecules\n\n')
        f.write('start reactions\n')
        f.write('    icos(lg1) + icos(lg1) <-> icos(lg1!1).icos(lg1!1)\n')
        f.write('    onRate3Dka = 2\n')
        f.write('    offRatekb = 2\n')
        f.write('    norm1 = [' + str(n[0]) + ', ' +
                str(n[1]) + ', ' + str(n[2]) + ']\n')
        f.write('    norm2 = [' + str(n[0]) + ', ' +
                str(n[1]) + ', ' + str(n[2]) + ']\n')
        f.write('    sigma = ' + str(float(sigma)) + '\n')
        f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
                ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
        f.write('    observeLabel = leg\n')
        f.write('    bindRadSameCom = 5.0\n')
        f.write('\n')
        f.write('    icos(lg2) + icos(lg2) <-> icos(lg2!1).icos(lg2!1)\n')
        f.write('    onRate3Dka = 2\n')
        f.write('    offRatekb = 2\n')
        f.write('    norm1 = [' + str(n[0]) + ', ' +
                str(n[1]) + ', ' + str(n[2]) + ']\n')
        f.write('    norm2 = [' + str(n[0]) + ', ' +
                str(n[1]) + ', ' + str(n[2]) + ']\n')
        f.write('    sigma = ' + str(float(sigma)) + '\n')
        f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
                ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
        f.write('    observeLabel = leg\n')
        f.write('    bindRadSameCom = 5.0\n')
        f.write('\n')
        f.write('    icos(lg3) + icos(lg3) <-> icos(lg3!1).icos(lg3!1)\n')
        f.write('    onRate3Dka = 2\n')
        f.write('    offRatekb = 2\n')
        f.write('    norm1 = [' + str(n[0]) + ', ' +
                str(n[1]) + ', ' + str(n[2]) + ']\n')
        f.write('    norm2 = [' + str(n[0]) + ', ' +
                str(n[1]) + ', ' + str(n[2]) + ']\n')
        f.write('    sigma = ' + str(float(sigma)) + '\n')
        f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
                ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
        f.write('    observeLabel = leg\n')
        f.write('    bindRadSameCom = 5.0\n')
        f.write('\n')
        f.write('    icos(lg1) + icos(lg2) <-> icos(lg1!1).icos(lg2!1)\n')
        f.write('    onRate3Dka = 4\n')
        f.write('    offRatekb = 2\n')
        f.write('    norm1 = [' + str(n[0]) + ', ' +
                str(n[1]) + ', ' + str(n[2]) + ']\n')
        f.write('    norm2 = [' + str(n[0]) + ', ' +
                str(n[1]) + ', ' + str(n[2]) + ']\n')
        f.write('    sigma = ' + str(float(sigma)) + '\n')
        f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
                ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
        f.write('    observeLabel = leg\n')
        f.write('    bindRadSameCom = 5.0\n')
        f.write('\n')
        f.write('    icos(lg1) + icos(lg3) <-> icos(lg1!1).icos(lg3!1)\n')
        f.write('    onRate3Dka = 4\n')
        f.write('    offRatekb = 2\n')
        f.write('    norm1 = [' + str(n[0]) + ', ' +
                str(n[1]) + ', ' + str(n[2]) + ']\n')
        f.write('    norm2 = [' + str(n[0]) + ', ' +
                str(n[1]) + ', ' + str(n[2]) + ']\n')
        f.write('    sigma = ' + str(float(sigma)) + '\n')
        f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
                ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
        f.write('    observeLabel = leg\n')
        f.write('    bindRadSameCom = 5.0\n')
        f.write('\n')
        f.write('    icos(lg2) + icos(lg3) <-> icos(lg2!1).icos(lg3!1)\n')
        f.write('    onRate3Dka = 4\n')
        f.write('    offRatekb = 2\n')
        f.write('    norm1 = [' + str(n[0]) + ', ' +
                str(n[1]) + ', ' + str(n[2]) + ']\n')
        f.write('    norm2 = [' + str(n[0]) + ', ' +
                str(n[1]) + ', ' + str(n[2]) + ']\n')
        f.write('    sigma = ' + str(float(sigma)) + '\n')
        f.write('    assocAngles = [' + str(theta1) + ', ' + str(theta2) +
                ', ' + str(phi1) + ', ' + str(phi2) + ', ' + str(omega) + ']\n')
        f.write('    observeLabel = leg\n')
        f.write('    bindRadSameCom = 5.0\n')
        f.write('\n')
        f.write('end reactions\n')

        f = open('icos.mol', 'w')
        f.write('##\n')
        f.write('# Icosahehedron (face-centered) information file.\n')
        f.write('##\n\n')
        f.write('Name = icos\n')
        f.write('checkOverlap = true\n\n')
        f.write('# translational diffusion constants\n')
        f.write('D = [13.0, 13.0, 13.0]\n\n')
        f.write('# rotational diffusion constants\n')
        f.write('Dr = [0.03, 0.03, 0.03]\n\n')
        f.write('# Coordinates\n')
        f.write('COM   ' + str(round(COM[0], 8)) + '   ' +
                str(round(COM[1], 8)) + '   ' + str(round(COM[2], 8)) + '\n')
        f.write('lg1   ' + str(round(lg1[0], 8)) + '   ' +
                str(round(lg1[1], 8)) + '   ' + str(round(lg1[2], 8)) + '\n')
        f.write('lg2   ' + str(round(lg2[0], 8)) + '   ' +
                str(round(lg2[1], 8)) + '   ' + str(round(lg2[2], 8)) + '\n')
        f.write('lg3   ' + str(round(lg3[0], 8)) + '   ' +
                str(round(lg3[1], 8)) + '   ' + str(round(lg3[2], 8)) + '\n')
        f.write('\n')
        f.write('# bonds\n')
        f.write('bonds = 3\n')
        f.write('com lg1\n')
        f.write('com lg2\n')
        f.write('com lg3\n')
        f.write('\n')


# ICOSAHEDRON VERTEX AS COM

