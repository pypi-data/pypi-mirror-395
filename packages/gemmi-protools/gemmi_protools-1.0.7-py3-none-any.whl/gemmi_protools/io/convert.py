"""
@Author: Luo Jiejian
"""

import gemmi
import numpy as np
from Bio.PDB.Structure import Structure as BioStructure
from Bio.PDB.StructureBuilder import StructureBuilder


def gemmi2bio(gemmi_structure: gemmi.Structure) -> BioStructure:
    """
    Convert gemmi structure to biopython structure
    :param gemmi_structure:
    :return:
    return biopython structure
    """
    structure_builder = StructureBuilder()
    structure_builder.init_structure(structure_id=gemmi_structure.name)

    for model_idx, gemmi_model in enumerate(gemmi_structure):
        structure_builder.init_model(model_idx)

        for gemmi_chain in gemmi_model:
            structure_builder.init_chain(gemmi_chain.name)

            for gemmi_residue in gemmi_chain:
                if gemmi_residue.het_flag == "H":
                    if gemmi_residue.name in ["HOH", "WAT"]:
                        het_flag = "W"
                    else:
                        het_flag = "H"
                else:
                    het_flag = " "

                structure_builder.init_residue(resname=gemmi_residue.name, field=het_flag,
                                               resseq=gemmi_residue.seqid.num, icode=gemmi_residue.seqid.icode)
                for gemmi_atom in gemmi_residue:
                    coord = np.array([gemmi_atom.pos.x, gemmi_atom.pos.y, gemmi_atom.pos.z])
                    structure_builder.init_atom(name=gemmi_atom.name,
                                                coord=coord,
                                                b_factor=gemmi_atom.b_iso,
                                                occupancy=gemmi_atom.occ,
                                                altloc=gemmi_atom.altloc if gemmi_atom.has_altloc() else ' ',
                                                fullname=gemmi_atom.name.center(4),
                                                serial_number=gemmi_atom.serial,
                                                element=gemmi_atom.element.name.upper())

    bio_structure = structure_builder.get_structure()
    return bio_structure


def bio2gemmi(bio_structure: BioStructure) -> gemmi.Structure:
    """
    Convert biopython structure to gemmi structure
    :param bio_structure:
    :return:
    return gemmi structure
    """

    g_structure = gemmi.Structure()
    g_structure.name = bio_structure.id

    for bio_model in bio_structure:
        # bio model start from 0, gemmi model start from 1
        g_model = gemmi.Model(bio_model.id + 1)
        for bio_chain in bio_model:
            g_chain = gemmi.Chain(bio_chain.id)
            for bio_residue in bio_chain:
                g_residue = gemmi.Residue()
                g_residue.name = bio_residue.resname
                het_flag, r_num, i_code = bio_residue.id
                g_residue.seqid.num = r_num
                g_residue.seqid.icode = i_code
                g_residue.het_flag = "A" if het_flag == " " else "H"

                for bio_atom in bio_residue:
                    g_atom = gemmi.Atom()
                    g_atom.name = bio_atom.name
                    g_atom.b_iso = bio_atom.bfactor
                    g_atom.occ = bio_atom.occupancy
                    g_atom.altloc = "\x00" if bio_atom.altloc == " " else bio_atom.altloc
                    g_atom.element = gemmi.Element(bio_atom.element)
                    g_atom.serial = bio_atom.serial_number
                    px, py, pz = bio_atom.coord
                    g_atom.pos = gemmi.Position(px, py, pz)
                    g_residue.add_atom(g_atom)
                g_chain.add_residue(g_residue)
            g_model.add_chain(g_chain)
        g_structure.add_model(g_model)
    g_structure.setup_entities()
    g_structure.assign_het_flags()
    return g_structure
