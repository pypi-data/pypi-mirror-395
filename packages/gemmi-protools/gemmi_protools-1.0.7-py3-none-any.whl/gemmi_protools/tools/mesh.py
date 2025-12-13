"""
@Author: Luo Jiejian
"""
import os
import subprocess
import tempfile
from collections import defaultdict
from typing import List, Optional, Union

import freesasa
import numpy as np
import trimesh
from Bio.PDB import Selection
from Bio.PDB.ResidueDepth import _get_atom_radius, _read_vertex_array

from gemmi_protools import StructureParser
from gemmi_protools import gemmi2bio


def _read_face_array(filename: str):
    with open(filename) as fp:
        face_list = []
        for line in fp:
            sl = line.split()
            if len(sl) != 5:
                # skip header
                continue
            vl = [int(x) for x in sl[0:3]]
            face_list.append(vl)
    return np.array(face_list)


def get_mesh(struct_file: str, chains: Optional[List[str]] = None, MSMS: str = "msms"):
    """

    :param struct_file: str
        .pdb, .cif, .pdb.gz, .cif.gz
    :param chains: a list of chain names
        default None to include all chains
    :param MSMS: str
        path of msms executable
    :return:
        https://ccsb.scripps.edu/msms/downloads/
    """
    xyz_tmp = tempfile.NamedTemporaryFile(delete=False).name
    surface_tmp = tempfile.NamedTemporaryFile(delete=False).name
    msms_tmp = tempfile.NamedTemporaryFile(delete=False).name
    face_file = surface_tmp + ".face"
    surface_file = surface_tmp + ".vert"

    try:
        st = StructureParser()
        st.load_from_file(struct_file)
        st.clean_structure(remove_ligand=True)

        if chains is None:
            st_p = st
        else:
            for ch in chains:
                if ch not in st.chain_ids:
                    raise ValueError("Chain %s not found (only [%s])" % (ch, " ".join(st.chain_ids)))
            st_p = st.pick_chains(chains)

        bio_st = gemmi2bio(st_p.STRUCT)
        model = bio_st[0]

        # Replace pdb_to_xyzr
        # Make x,y,z,radius file
        atom_list = Selection.unfold_entities(model, "A")

        with open(xyz_tmp, "w") as pdb_to_xyzr:
            for atom in atom_list:
                x, y, z = atom.coord
                radius = _get_atom_radius(atom, rtype="united")
                pdb_to_xyzr.write(f"{x:6.3f}\t{y:6.3f}\t{z:6.3f}\t{radius:1.2f}\n")

        # Make surface
        MSMS = MSMS + " -no_header -probe_radius 1.5 -if %s -of %s > " + msms_tmp
        make_surface = MSMS % (xyz_tmp, surface_tmp)
        subprocess.call(make_surface, shell=True)
        if not os.path.isfile(surface_file):
            raise RuntimeError(
                f"Failed to generate surface file using command:\n{make_surface}"
            )

    except Exception as e:
        print(str(e))
        mesh = None
    else:
        # Read surface vertices from vertex file
        vertices = _read_vertex_array(surface_file)
        faces = _read_face_array(face_file)
        mesh = trimesh.Trimesh(vertices=vertices, faces=faces - 1)
        mesh.merge_vertices()
        mesh.update_faces(mesh.unique_faces())
        mesh.update_faces(mesh.nondegenerate_faces())
        mesh.remove_unreferenced_vertices()

    # Remove temporary files
    for fn in [xyz_tmp, surface_tmp, msms_tmp, face_file, surface_file]:
        try:
            os.remove(fn)
        except OSError:
            pass

    return mesh


def get_surface_residues(struct_file: str,
                         chains: Optional[List[str]] = None,
                         relative_sasa_cutoff: Union[int, float] = 0.15):
    ####################
    # check and pick
    ####################
    st = StructureParser()
    st.load_from_file(struct_file)
    st.clean_structure()

    if chains is None:
        chains = st.chain_ids

    if isinstance(chains, list):
        if len(chains) == 0:
            raise ValueError("chains is not set")
        else:
            # check if chains valid
            for ch in chains:
                if ch not in st.chain_ids:
                    raise ValueError("Chain %s not found" % ch)

    st_p = st.pick_chains(chains)
    # sequences = {k: s.replace("-", "").upper() for k, s in st_p.polymer_sequences().items()}

    # start from 1
    seq_num_mapper = dict()
    for chain in st_p.MODEL:
        for i, res in enumerate(chain):
            key = (chain.name, str(res.seqid.num) + res.seqid.icode.strip(), res.name)
            seq_num_mapper[key] = i + 1

    # make one upper letter chain ID
    mapper = st_p.make_one_letter_chain(only_uppercase=True)
    mapper_r = {v: k for k, v in mapper.items()}

    ####################
    # save to pdb
    ####################
    with tempfile.NamedTemporaryFile(delete=True, suffix=".pdb", mode='w') as tmp_file:
        st_p.to_pdb(tmp_file.name)
        structure = freesasa.Structure(tmp_file.name)

    result = freesasa.calc(structure)

    residue_areas = result.residueAreas()

    surface_residues_relative_sasa = dict()
    surface_atoms = defaultdict(list)
    for atom_index in range(structure.nAtoms()):
        ch = structure.chainLabel(atom_index)
        ch = mapper_r.get(ch, ch)

        res_num = structure.residueNumber(atom_index).strip()
        res_name = structure.residueName(atom_index)
        atom_sasa = result.atomArea(atom_index)

        res_id = (ch, res_num, res_name)
        res_relative_total = residue_areas[ch][res_num].relativeTotal
        if res_relative_total > relative_sasa_cutoff:
            if res_id not in surface_residues_relative_sasa:
                surface_residues_relative_sasa[res_id] = res_relative_total
            if atom_sasa > 0:
                atom_name = structure.atomName(atom_index).strip()
                pos = structure.coord(atom_index)
                surface_atoms[res_id].append((atom_sasa, atom_name, pos))

    results = []
    for res_id, query_atoms in surface_atoms.items():
        seq_loc = seq_num_mapper[res_id]

        query_atoms.sort(reverse=True)
        centroid = tuple(np.array([a[2] for a in query_atoms[0:3]]).mean(axis=0).tolist())
        results.append((res_id[0],
                        res_id[1],
                        res_id[2],
                        seq_loc,
                        centroid,
                        surface_residues_relative_sasa[res_id]
                        )
                       )
    dtype = [("chain_name", "U5"),
             ("residue_numi", "U8"),
             ("residue_name", "U5"),
             ("sequential_residue_num", "i4"),
             ("centroid", ("f4", (3,))),
             ("relative_sasa", "f4"),
             ]
    return np.array(results, dtype=dtype)
