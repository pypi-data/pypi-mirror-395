from ..gen_platonic.angle_cal import angle_cal
from .dode_face_leg_reduce_coor_gen import dode_face_leg_reduce_coor_gen
from .dode_face_input_coord import dode_face_input_coord


def dode_face_write(radius: float, sigma: float,create_Solid: bool = False):
    """Generate input file for dodecahedron face-centered simulation.

    This function takes a radius and a sigma value as input parameters,
    and generates an input file for a dodecahedron face-centered simulation
    using the provided parameters. The input file is written to a file named
    'parm.inp' and contains information about simulation parameters,
    boundaries, molecules, and reactions.

    Args:
        radius (float): Radius of the dodecahedron.
        sigma (float): Sigma value.
        create_solid (bool): This is for use in PlatonicSolids.createSolid. 

    Returns:
        parm.inp/cube.mol file: inputs for NERDSS if create_solid == False
        reaction information if create_Solid == True
        
    """

    if create_Solid == True:
        COM, lg1, lg2, lg3, lg4, lg5, n = dode_face_input_coord(radius, sigma)
        coord = dode_face_leg_reduce_coor_gen(radius, sigma)
        theta1, theta2, phi1, phi2, omega = angle_cal(
        coord[0][0], coord[0][3], coord[4][0], coord[4][1])

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
                "lg3": lg3,
                "lg4": lg4,
                "lg5": lg5,}
        return output_reactions_dict, output_mol_dict
    else:
        COM, lg1, lg2, lg3, lg4, lg5, n = dode_face_input_coord(radius, sigma)
        coord = dode_face_leg_reduce_coor_gen(radius, sigma)
        theta1, theta2, phi1, phi2, omega = angle_cal(
                coord[0][0], coord[0][3], coord[4][0], coord[4][1])

        f = open('parm.inp', 'w')
        f.write(' # Input file (dodecahedron face-centered)\n\n')
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
        f.write('    dode(lg1) + dode(lg1) <-> dode(lg1!1).dode(lg1!1)\n')
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
        f.write('    dode(lg2) + dode(lg2) <-> dode(lg2!1).dode(lg2!1)\n')
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
        f.write('    dode(lg3) + dode(lg3) <-> dode(lg3!1).dode(lg3!1)\n')
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
        f.write('    dode(lg4) + dode(lg4) <-> dode(lg4!1).dode(lg4!1)\n')
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
        f.write('    dode(lg5) + dode(lg5) <-> dode(lg5!1).dode(lg5!1)\n')
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
        f.write('    dode(lg1) + dode(lg2) <-> dode(lg1!1).dode(lg2!1)\n')
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
        f.write('    dode(lg1) + dode(lg3) <-> dode(lg1!1).dode(lg3!1)\n')
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
        f.write('    dode(lg1) + dode(lg4) <-> dode(lg1!1).dode(lg4!1)\n')
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
        f.write('    dode(lg1) + dode(lg5) <-> dode(lg1!1).dode(lg5!1)\n')
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
        f.write('    dode(lg2) + dode(lg3) <-> dode(lg2!1).dode(lg3!1)\n')
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
        f.write('    dode(lg2) + dode(lg4) <-> dode(lg2!1).dode(lg4!1)\n')
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
        f.write('    dode(lg2) + dode(lg5) <-> dode(lg2!1).dode(lg5!1)\n')
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
        f.write('    dode(lg3) + dode(lg4) <-> dode(lg3!1).dode(lg4!1)\n')
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
        f.write('    dode(lg3) + dode(lg5) <-> dode(lg3!1).dode(lg5!1)\n')
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
        f.write('    dode(lg4) + dode(lg5) <-> dode(lg4!1).dode(lg5!1)\n')
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

        f = open('dode.mol', 'w')
        f.write('##\n')
        f.write('# Dodecahedron (face-centered) information file.\n')
        f.write('##\n\n')
        f.write('Name = dode\n')
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
        f.write('lg4   ' + str(round(lg4[0], 8)) + '   ' +
                str(round(lg4[1], 8)) + '   ' + str(round(lg4[2], 8)) + '\n')
        f.write('lg5   ' + str(round(lg5[0], 8)) + '   ' +
                str(round(lg5[1], 8)) + '   ' + str(round(lg5[2], 8)) + '\n')
        f.write('\n')
        f.write('# bonds\n')
        f.write('bonds = 5\n')
        f.write('com lg1\n')
        f.write('com lg2\n')
        f.write('com lg3\n')
        f.write('com lg4\n')
        f.write('com lg5\n')
        f.write('\n')


        # DODECAHEDEON VERTEX AS COM

