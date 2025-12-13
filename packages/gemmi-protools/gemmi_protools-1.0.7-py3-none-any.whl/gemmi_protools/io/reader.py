import gzip
import io
import pathlib
import random
import string
from collections import defaultdict
from typing import Dict, Optional, List

import gemmi
import numpy as np
import pandas as pd
from scipy.spatial import cKDTree

ATOM = [("chain_name", "U5"),
        ("residue_num", "i4"),
        ("residue_icode", "U3"),
        ("residue_name", "U5"),
        ("atom_name", "U5"),
        ("element", "U3"),
        ("charge", "i1"),
        ("b_factor", "f4"),
        ("occupancy", "f4"),
        ("coordinate", ("f4", (3,)))
        ]


def is_pdb(path: str) -> bool:
    """
    Check if input file is .pdb or .pdb.gz format
    :param path:
    :return:
        bool
    """
    path = pathlib.Path(path)

    if path.suffixes:
        if path.suffixes[-1] == ".pdb":
            return True
        elif "".join(path.suffixes[-2:]) == ".pdb.gz":
            return True
        else:
            return False
    else:
        return False


def is_cif(path: str) -> bool:
    """
    Check if input file is .cif or .cif.gz
    :param path:
    :return:
        bool
    """

    path = pathlib.Path(path)
    if path.suffixes:
        if path.suffixes[-1] == ".cif":
            return True
        elif "".join(path.suffixes[-2:]) == ".cif.gz":
            return True
        else:
            return False
    else:
        return False


def parse_cif(path: str) -> dict:
    """
    Parse CIF structure and info
    :param path: str
    :return:
        dict
    """
    if not is_cif(path):
        raise TypeError("Input file is not a cif file [.cif or .cif.gz]: %s" % path)

    doc = gemmi.cif.Document()
    st = gemmi.read_structure(path, save_doc=doc)
    st.setup_entities()
    st.assign_serial_numbers()
    block = doc.sole_block()

    def _read_src(query_block, category, name_col, taxid_col):
        dk = pd.DataFrame(query_block.get_mmcif_category(name=category, raw=False))
        dk[dk.isna()] = ""

        if dk.shape[0] > 0 and np.all(np.isin(["entity_id", name_col, taxid_col], dk.columns)):
            return {eid: [name, taxid]
                    for eid, name, taxid in dk[["entity_id", name_col, taxid_col]].to_numpy()
                    }
        else:
            return dict()

    desc = pd.DataFrame(block.get_mmcif_category(name="_entity", raw=False))
    desc[desc.isna()] = ""

    entityid2description = dict()
    if desc.shape[0] > 0 and np.all(np.isin(["id", "pdbx_description"], desc.columns)):
        entityid2description = dict(zip(desc["id"], desc["pdbx_description"]))

    entityid2src = dict()
    src_1 = _read_src(block, "_entity_src_gen.",
                      "pdbx_gene_src_scientific_name",
                      "pdbx_gene_src_ncbi_taxonomy_id")
    src_2 = _read_src(block, "_pdbx_entity_src_syn.",
                      "organism_scientific",
                      "ncbi_taxonomy_id")
    src_3 = _read_src(block, "_entity_src_nat.",
                      "pdbx_organism_scientific",
                      "pdbx_ncbi_taxonomy_id")
    entityid2src.update(src_1)

    for k, v in src_2.items():
        if k not in entityid2src:
            entityid2src[k] = v

    for k, v in src_3.items():
        if k not in entityid2src:
            entityid2src[k] = v

    info_map = dict(st.info)
    pdb_code = info_map.get("_entry.id", "").lower()

    v1 = block.find_value("_refine.ls_d_res_high")
    v2 = block.find_value("_em_3d_reconstruction.resolution")

    resolution = 0.0
    if v1 not in [".", "?", None]:
        resolution = v1
    elif v2 not in [".", "?", None]:
        resolution = v2

    try:
        resolution = float(resolution)
    except:
        resolution = 0.0

    st.resolution = resolution

    info = dict(description={k: v for k, v in entityid2description.items() if v and v != "?"},
                source=entityid2src,
                resolution=st.resolution,
                pdb_id=pdb_code if gemmi.is_pdb_code(pdb_code) else "",
                method=info_map.get("_exptl.method", "").lower(),
                deposition_date=info_map.get("_pdbx_database_status.recvd_initial_deposition_date", ""),
                title=info_map.get("_struct.title", "")
                )
    return dict(structure=st, info=info)


def molecule_description(path: str):
    """
    Molecule description from PDB (.pdb or .pdb.gz)
    :param path:
    :return:
    """
    if is_pdb(path):
        cur_path = pathlib.Path(path)
        if cur_path.suffixes[-1] == ".pdb":
            with open(path, "r") as text_io:
                lines = text_io.readlines()
        else:
            with gzip.open(path, "rb") as gz_handle:
                with io.TextIOWrapper(gz_handle, encoding="utf-8") as text_io:
                    lines = text_io.readlines()
    else:
        raise ValueError("Only support .pdb or .pdb.gz file, but got %s" % path)

    values = {"COMPND": defaultdict(dict),
              "SOURCE": defaultdict(dict),
              }

    comp_molid = ""
    last_comp_key = ""

    for hh in lines:
        h = hh.strip()
        key = h[:6].strip()
        tt = h[10:].strip().strip(";")

        if key in ["COMPND", "SOURCE"]:
            tok = tt.split(":")
            if len(tok) >= 2:
                ckey = tok[0].lower().strip()
                cval = tok[1].strip()
                if ckey == "mol_id":
                    comp_molid = cval
                    values[key][comp_molid] = dict()
                else:
                    values[key][comp_molid][ckey] = cval
                    last_comp_key = ckey
            else:
                if last_comp_key != "":
                    values[key][comp_molid][last_comp_key] += " " + tok[0].strip()

    outputs = dict(description=dict(),
                   source=dict())

    ch_id2mol_id = dict()
    for mol_id, val in values["COMPND"].items():
        chain_str = val.get("chain", "").strip()
        if chain_str != "":
            chains = chain_str.split(",")
            for ch in chains:
                ch_id2mol_id[ch.strip()] = mol_id

    for mol_id, val in values["COMPND"].items():
        m = val.get("molecule", "").strip()
        if m != "":
            outputs["description"][mol_id] = m

    for mol_id, val in values["SOURCE"].items():
        name = val.get("organism_scientific", "").strip()
        taxid = val.get("organism_taxid", "").strip()
        if name not in ["", "?", "."] or taxid not in ["", "?", "."]:
            outputs["source"][mol_id] = [name, taxid]
    outputs["ch_id2mol_id"] = ch_id2mol_id
    return outputs


def parse_pdb(path: str) -> dict:
    if not is_pdb(path):
        raise TypeError("Input file is not a pdb file [.pdb or .pdb.gz]: %s" % path)

    st = gemmi.read_structure(path)
    st.setup_entities()
    st.assign_serial_numbers()

    values = molecule_description(path)

    mol_id2entity_name = dict()
    for ent in st.entities:
        if ent.name in values["ch_id2mol_id"]:
            mol_id = values["ch_id2mol_id"][ent.name]
            mol_id2entity_name[mol_id] = ent.name

    # replace mod_id to entity.name
    description = {mol_id2entity_name[mol_id]: v for mol_id, v in values["description"].items()
                   if mol_id in mol_id2entity_name}
    # add ligand and water entity description
    # gemmi use ligand name or water as entity name, take this as description
    for ent in st.entities:
        if (ent.name not in description
                and ent.polymer_type.name == "Unknown"
                and ent.name != ""
                and len(ent.name) > 1):
            description[ent.name] = ent.name

    source = {mol_id2entity_name[mol_id]: v for mol_id, v in values["source"].items()
              if mol_id in mol_id2entity_name}

    # assign digital entity names
    mapper = assign_digital_entity_names(st)

    info_map = dict(st.info)
    pdb_code = info_map.get("_entry.id", "").lower()
    info = dict(description={mapper.get(k, k): v for k, v in description.items()},
                source={mapper.get(k, k): v for k, v in source.items()},
                resolution=st.resolution,
                pdb_id=pdb_code if gemmi.is_pdb_code(pdb_code) else "",
                method=info_map.get("_exptl.method", "").lower(),
                deposition_date=info_map.get("_pdbx_database_status.recvd_initial_deposition_date", ""),
                title=info_map.get("_struct.title", ""),
                )
    return dict(structure=st, info=info)


def assign_digital_entity_names(structure: gemmi.Structure) -> Optional[Dict[str, str]]:
    """
    :param structure:
    :return:
       dict, original entity name to new digital entity name
    """
    all_digit_name = np.all([ent.name.isdigit() for ent in structure.entities])

    mapper = dict()
    if not all_digit_name:
        for ix, ent in enumerate(structure.entities):
            new_name = str(ix + 1)
            mapper[ent.name] = new_name
            ent.name = new_name
    return mapper


class StructureParser(object):
    """
    Structure reader for .cif, .cif.gz, .pdb or .pdb.gz

    Read the first model
    """

    def __init__(self, structure: Optional[gemmi.Structure] = None):
        if not isinstance(structure, (type(None), gemmi.Structure)):
            raise ValueError("structure must be gemmi.Structure or None")
        if structure is None:
            # init with an empty model
            self.STRUCT = gemmi.Structure()
            self.MODEL = gemmi.Model(1)
            self.STRUCT.add_model(self.MODEL)
        elif isinstance(structure, gemmi.Structure):
            self.STRUCT = structure.clone()
        else:
            raise ValueError("structure must be gemmi.Structure or None")

        self._init_struct()

        info_map = dict(self.STRUCT.info)
        pdb_code = info_map.get("_entry.id", "").lower()
        self.INFO = dict(description=dict(),
                         source=dict(),
                         resolution=self.STRUCT.resolution,
                         pdb_id=pdb_code if gemmi.is_pdb_code(pdb_code) else "",
                         method=info_map.get("_exptl.method", "").lower(),
                         deposition_date=info_map.get("_pdbx_database_status.recvd_initial_deposition_date", ""),
                         title=info_map.get("_struct.title", ""),
                         )
        self.update_entity()

    def _init_struct(self):
        self.STRUCT.setup_entities()
        self.STRUCT.assign_serial_numbers()
        self.STRUCT.renumber_models()

        # keep the first model
        if len(self.STRUCT) > 1:
            for idx in reversed(list(range(1, len(self.STRUCT)))):
                del self.STRUCT[idx]

        self.MODEL = self.STRUCT[0]
        self.STRUCT.remove_empty_chains()
        self._update_full_sequences()

    def load_from_file(self, path: str):
        """
        Load model from file, default use the first model.
        :param path:
        :return:
        """
        if is_pdb(path):
            val = parse_pdb(path)
            self.STRUCT, self.INFO = val["structure"], val["info"]
        elif is_cif(path):
            val = parse_cif(path)
            self.STRUCT, self.INFO = val["structure"], val["info"]
        else:
            raise ValueError("path must be files with suffixes [ .cif, .cif.gz, .pdb or .pdb.gz]")

        self._init_struct()
        self.update_entity()

    def _update_full_sequences(self):
        for idx, ent in enumerate(self.STRUCT.entities):
            if ent.entity_type.name == "Polymer":
                self.STRUCT.entities[idx].full_sequence = [gemmi.Entity.first_mon(item) for item in ent.full_sequence]

                if len(ent.full_sequence) == 0:
                    sc = self.get_subchain(ent.subchains[0])
                    self.STRUCT.entities[idx].full_sequence = sc.extract_sequence()

    @property
    def chain_ids(self):
        return [ch.name for ch in self.MODEL]

    @property
    def subchain_ids(self):
        return [ch.subchain_id() for ch in self.MODEL.subchains()]

    @property
    def assembly_names(self):
        return [assem.name for assem in self.STRUCT.assemblies]

    @property
    def polymer_types(self):
        subchain_id2polymer = dict()
        for ent in self.STRUCT.entities:
            if ent.entity_type.name == "Polymer":
                for ch in ent.subchains:
                    subchain_id2polymer[ch] = ent.polymer_type

        out = dict()
        for chain in self.MODEL:
            polymer_ch = chain.get_polymer()
            seq = polymer_ch.extract_sequence()
            if seq:
                subchain_id = polymer_ch.subchain_id()
                if subchain_id in subchain_id2polymer:
                    out[chain.name] = subchain_id2polymer[subchain_id]
        return out

    def polymer_sequences(self, pdbx: bool = False):
        """
        entity sequences for polymers
        :param pdbx:
        :return:
        """
        out = dict()
        subchain_id2entity_id = self.subchain_id_to_entity_id
        entity_dict = {ent.name: ent for ent in self.STRUCT.entities}

        for ch, polymer_type in self.polymer_types.items():
            polymer = self.get_chain(ch).get_polymer()
            entity_id = subchain_id2entity_id[polymer.subchain_id()]
            ent = entity_dict[entity_id]

            if pdbx:
                s = gemmi.pdbx_one_letter_code(ent.full_sequence, gemmi.sequence_kind(polymer_type))
            else:
                # s = "".join([gemmi.find_tabulated_residue(r).one_letter_code for r in ent.full_sequence]).upper()
                s = "".join([gemmi.find_tabulated_residue(r).one_letter_code
                             for r in ent.full_sequence]).upper().replace(" ", "X")
            out[ch] = s
        return out

    def get_subchain(self, subchain_id: str):
        out = None
        for ch in self.MODEL.subchains():
            if ch.subchain_id() == subchain_id:
                out = ch
                break

        if out is None:
            raise ValueError("Sub-Chain %s not found (only [%s])" % (subchain_id, " ".join(self.subchain_ids)))

        return out

    @property
    def subchain_id_to_entity_id(self):
        return {ch: ent.name for ent in self.STRUCT.entities for ch in ent.subchains}

    @property
    def subchain_id_to_chain_id(self):
        return {sch.subchain_id(): chain.name for chain in self.MODEL for sch in chain.subchains()}

    def get_chain(self, chain_id: str):
        return self.MODEL[chain_id]

    def pick_chains(self, chain_names: List[str]):
        struct = gemmi.Structure()
        struct.name = self.STRUCT.name
        model = gemmi.Model(1)
        for ch_id in chain_names:
            model.add_chain(self.get_chain(ch_id))

        struct.add_model(model)

        # add basic information
        struct.resolution = self.STRUCT.resolution

        vals = {"_exptl.method": self.INFO["method"],
                "_struct.title": "(Chains %s): " % " ".join(chain_names) + self.INFO["title"],
                "_pdbx_database_status.recvd_initial_deposition_date": self.INFO["deposition_date"],
                }
        if self.INFO["pdb_id"] != "":
            vals["_entry.id"] = self.INFO["pdb_id"]

        struct.info = gemmi.InfoMap(vals)
        new_struct = StructureParser(struct)

        new_struct.INFO["description"] = {ent.name: self.INFO["description"][ent.name]
                                          for ent in new_struct.STRUCT.entities
                                          if ent.name in self.INFO["description"]
                                          }
        new_struct.INFO["source"] = {ent.name: self.INFO["source"][ent.name]
                                     for ent in new_struct.STRUCT.entities
                                     if ent.name in self.INFO["source"]
                                     }
        return new_struct

    def _raw_marks(self):
        subchain2chain = dict()
        for chain in self.MODEL:
            for sub_chain in chain.subchains():
                subchain_id = sub_chain.subchain_id()
                subchain2chain[subchain_id] = chain.name

        entity2chains = dict()
        for ent in self.STRUCT.entities:
            val = [subchain2chain[sub_ch] for sub_ch in ent.subchains if sub_ch in subchain2chain]
            if len(val) > 0:
                entity2chains[ent.name] = val

        mol_id = 1
        n_line = 1
        compound_mol = "COMPND {n_line:>3} MOL_ID: {mol_id};"
        compound_molecule = "COMPND {n_line:>3} MOLECULE: {molecule};"
        compound_chain = "COMPND {n_line:>3} CHAIN: {chain};"

        outputs = []

        for ent in self.STRUCT.entities:
            if ent.entity_type.name == "Polymer":
                chain = ", ".join(entity2chains[ent.name])

                molecule = self.INFO["description"].get(ent.name, "")
                if n_line == 1:
                    outputs.append("COMPND    MOL_ID: {mol_id};".format(mol_id=mol_id))
                else:
                    outputs.append(compound_mol.format(n_line=n_line, mol_id=mol_id))
                n_line += 1

                outputs.append(compound_molecule.format(n_line=n_line, molecule=molecule))
                n_line += 1

                outputs.append(compound_chain.format(n_line=n_line, chain=chain))
                n_line += 1

                mol_id += 1

        mol_id = 1
        n_line = 1
        source_mol = "SOURCE {n_line:>3} MOL_ID: {mol_id};"
        source_scientific = "SOURCE {n_line:>3} ORGANISM_SCIENTIFIC: {organism_scientific};"
        source_taxid = "SOURCE {n_line:>3} ORGANISM_TAXID: {organism_taxid};"

        for ent in self.STRUCT.entities:
            if ent.entity_type.name == "Polymer":
                src = self.INFO["source"].get(ent.name)
                if src is None:
                    organism_scientific, organism_taxid = "", ""
                else:
                    organism_scientific, organism_taxid = src

                if n_line == 1:
                    outputs.append("SOURCE    MOL_ID: {mol_id};".format(mol_id=mol_id))
                else:
                    outputs.append(source_mol.format(n_line=n_line, mol_id=mol_id))
                n_line += 1

                outputs.append(source_scientific.format(n_line=n_line, organism_scientific=organism_scientific))
                n_line += 1

                outputs.append(source_taxid.format(n_line=n_line, organism_taxid=organism_taxid))
                n_line += 1

                mol_id += 1

        resolution_remarks = ["REMARK   2",
                              "REMARK   2 RESOLUTION.    %.2f ANGSTROMS." % self.STRUCT.resolution
                              ]
        outputs.extend(resolution_remarks)
        return outputs

    def to_pdb(self, outfile: str, write_minimal_pdb=False):
        struct = self.STRUCT.clone()
        if write_minimal_pdb:
            struct.write_minimal_pdb(outfile)
        else:
            struct.raw_remarks = self._raw_marks()
            struct.write_pdb(outfile)

    @staticmethod
    def _item_index(block: gemmi.cif.Block, tag: str):
        mapper = dict()
        for idx, item in enumerate(block):
            if item.loop is not None:
                keys = item.loop.tags
                for k in keys:
                    mapper[k] = idx
            elif item.pair is not None:
                key = item.pair[0]
                mapper[key] = idx
        return mapper.get(tag)

    def to_cif(self, outfile: str):
        block = self.STRUCT.make_mmcif_block()
        #### add resolution
        # block.set_pair(tag="_refine.entry_id", value=gemmi.cif.quote(self.INFO["pdb_id"].upper()))
        # block.set_pair(tag="_refine.pdbx_refine_id", value=gemmi.cif.quote(self.INFO["method"].upper()))
        block.set_pair(tag="_refine.ls_d_res_high", value=gemmi.cif.quote(str(self.INFO["resolution"])))

        # tag_names = ["_exptl.entry_id",
        #              "_refine.entry_id", "_refine.pdbx_refine_id",
        #              "_refine.ls_d_res_high"]
        # for i in range(1, len(tag_names)):
        #     idx_1a = self._item_index(block, tag=tag_names[i])
        #     idx_2a = self._item_index(block, tag=tag_names[i - 1])
        #     block.move_item(idx_1a, idx_2a + 1)

        #### add entity description
        ta = block.find_mmcif_category(category="_entity.")
        da = pd.DataFrame(list(ta), columns=list(ta.tags))
        da["_entity.pdbx_description"] = da["_entity.id"].apply(
            lambda i: gemmi.cif.quote(self.INFO["description"].get(i, "?")))

        rows_1 = da.to_numpy().tolist()
        tags_1 = [s.replace("_entity.", "") for s in da.columns.tolist()]

        # erase
        qitem = block.find_loop_item("_entity.id")
        if isinstance(qitem, gemmi.cif.Item):
            qitem.erase()

        # add
        loop_1 = block.init_loop(prefix="_entity.", tags=tags_1)
        for r in rows_1:
            loop_1.add_row(r)

        idx_1b = self._item_index(block, tag="_entity.id")
        idx_2b = self._item_index(block, tag="_entity_poly.entity_id")

        # place _entity. before _entity_poly.
        if isinstance(idx_1b, int) and isinstance(idx_2b, int):
            block.move_item(idx_1b, idx_2b - 1)

        #### add source name and taxid
        loop_2 = block.init_loop(prefix="_entity_src_gen.", tags=["entity_id",
                                                                  "pdbx_gene_src_scientific_name",
                                                                  "pdbx_gene_src_ncbi_taxonomy_id"])

        for k, (name, taxid) in self.INFO["source"].items():
            name = name if name != "" else "?"
            taxid = taxid if taxid != "" else "?"

            loop_2.add_row([gemmi.cif.quote(k),
                            gemmi.cif.quote(name),
                            gemmi.cif.quote(taxid)]
                           )

        idx_1c = self._item_index(block, tag="_entity_src_gen.entity_id")
        idx_2c = self._item_index(block, tag="_entity_poly_seq.entity_id")
        # place _entity_src_gen. after _entity_poly_seq.
        if isinstance(idx_1c, int) and isinstance(idx_2c, int):
            block.move_item(idx_1c, idx_2c + 1)

        block.write_file(outfile)

    def update_entity(self):
        """
        Update ENTITY, .entities .assemblies according to subchains
        :return:
        """
        subchains = self.subchain_ids

        # update .entities
        new_entities = gemmi.EntityList()
        ent_names = []  # keep
        for ent in self.STRUCT.entities:
            tmp = [i for i in ent.subchains if i in subchains]
            if tmp:
                ent.subchains = tmp
                new_entities.append(ent)
                ent_names.append(ent.name)
        self.STRUCT.entities = new_entities

        # update INFO
        self.INFO["description"] = {k: v for k, v in self.INFO["description"].items() if k in ent_names}
        self.INFO["source"] = {k: v for k, v in self.INFO["source"].items() if k in ent_names}

        # update .assemblies
        all_cid = self.chain_ids
        del_assembly_indexes = []

        for a_i, assembly in enumerate(self.STRUCT.assemblies):
            del_gen_indexes = []
            for g_i, gen in enumerate(assembly.generators):
                # chains
                tmp1 = [i for i in gen.chains if i in all_cid]
                gen.chains = tmp1

                tmp2 = [i for i in gen.subchains if i in subchains]
                gen.subchains = tmp2
                # empty gen
                if gen.chains == [] and gen.subchains == []:
                    del_gen_indexes.append(g_i)

            del_gen_indexes.sort(reverse=True)
            for dgi in del_gen_indexes:
                del assembly.generators[dgi]

            if len(del_gen_indexes) == len(assembly.generators):
                del_assembly_indexes.append(a_i)

        del_assembly_indexes.sort(reverse=True)
        for dai in del_assembly_indexes:
            del self.STRUCT.assemblies[dai]

    def rename_chain(self, origin_name: str, target_name: str):
        if origin_name not in self.chain_ids:
            raise ValueError("Chain %s not found" % origin_name)

        other_chain_names = set(self.chain_ids) - {origin_name}

        if target_name in other_chain_names:
            raise ValueError("Chain %s has existed, please set a different target_name." % target_name)

        self.STRUCT.rename_chain(origin_name, target_name)

        for assembly in self.STRUCT.assemblies:
            for gen in assembly.generators:
                tmp = [target_name if c == origin_name else c for c in gen.chains]
                gen.chains = tmp

    def swap_chain_names(self, chain_name_1: str, chain_name_2: str):
        if chain_name_1 not in self.chain_ids:
            raise ValueError("Chain %s not found" % chain_name_1)
        if chain_name_2 not in self.chain_ids:
            raise ValueError("Chain %s not in found" % chain_name_2)

        flag = True
        sw_name = ""

        while flag:
            characters = string.ascii_letters + string.digits
            sw_name = ''.join(random.choices(characters, k=4))
            if sw_name not in self.chain_ids:
                flag = False

        if sw_name != "":
            self.rename_chain(chain_name_1, sw_name)
            self.rename_chain(chain_name_2, chain_name_1)
            self.rename_chain(sw_name, chain_name_2)

    def make_one_letter_chain(self, only_uppercase: bool = True):
        uppercase_letters = list(string.ascii_uppercase)
        uppercase_letters.sort(reverse=True)

        lowercase_letters = list(string.ascii_lowercase)
        lowercase_letters.sort(reverse=True)

        digit_letters = list(string.digits)
        digit_letters.sort(reverse=True)

        if only_uppercase:
            letters = uppercase_letters
        else:
            letters = digit_letters + lowercase_letters + uppercase_letters

        if only_uppercase:
            msg = "The number of chains exceed the number of uppercase letters: %d > %d"
        else:
            msg = "The number of chains exceed the number of one-letter characters: %d > %d"

        if len(self.chain_ids) > len(letters):
            raise RuntimeError(msg % (len(self.chain_ids), len(letters)))

        # not use yet
        letters_valid = [l for l in letters if l not in self.chain_ids]
        mapper = {ch: letters_valid.pop() for ch in self.chain_ids if ch not in letters}

        for origin_name, target_name in mapper.items():
            self.rename_chain(origin_name, target_name)
        return mapper

    def get_assembly(self, assembly_name: str,
                     how: gemmi.HowToNameCopiedChain = gemmi.HowToNameCopiedChain.AddNumber):
        if assembly_name not in self.assembly_names:
            raise ValueError("Assembly %s not found (only [%s])" % (assembly_name, ", ".join(self.assembly_names)))

        struct = self.STRUCT.clone()
        struct.transform_to_assembly(assembly_name, how)
        struct.info["_struct.title"] = "(Assembly %s): " % assembly_name + struct.info["_struct.title"]

        new_struct = StructureParser(struct)

        # find perfect match entities
        entity_mapper = dict()
        for new_ent in new_struct.STRUCT.entities:
            for ent in self.STRUCT.entities:
                if new_ent.entity_type == ent.entity_type:
                    if ent.entity_type.name == "Polymer":
                        if new_ent.full_sequence == ent.full_sequence:
                            entity_mapper[new_ent.name] = ent.name
                            break
                    else:
                        new_s = new_struct.get_subchain(new_ent.subchains[0]).extract_sequence()
                        s = self.get_subchain(ent.subchains[0]).extract_sequence()
                        if new_s == s:
                            entity_mapper[new_ent.name] = ent.name
                            break

        # update Info
        desc = dict()
        src = dict()

        for ent in new_struct.STRUCT.entities:
            if ent.name in entity_mapper and entity_mapper[ent.name] in self.INFO["description"]:
                desc[ent.name] = self.INFO["description"][entity_mapper[ent.name]]

            if ent.name in entity_mapper and entity_mapper[ent.name] in self.INFO["source"]:
                src[ent.name] = self.INFO["source"][entity_mapper[ent.name]]

        new_struct.INFO["description"] = desc
        new_struct.INFO["source"] = src
        return new_struct

    def clean_structure(self, remove_ligand=False, remove_hydrogen=True):
        """
        Remove water by default

        :param remove_ligand: bool, default False
        :param remove_hydrogen: bool, default True
        :return:
        """
        self.STRUCT.remove_alternative_conformations()

        if remove_hydrogen:
            self.STRUCT.remove_hydrogens()

        if remove_ligand:
            self.STRUCT.remove_ligands_and_waters()
        else:
            self.STRUCT.remove_waters()

        self.STRUCT.remove_empty_chains()
        self.update_entity()

    def met_to_mse(self):
        for chain in self.MODEL:
            for residue in chain:
                if residue.name == 'MET':
                    residue.name = 'MSE'
                    for atom in residue:
                        if atom.name == 'SD':
                            atom.name = 'SE'
                            atom.element = gemmi.Element('Se')

    def get_atoms(self, arg: str = "*", exclude_hydrogen=False):
        """

        :param arg: str, "*", "/1/*//N,CA,C,O", "/1/*"
            see gemmi.Selection
        :param exclude_hydrogen: bool, default False
        :return:
        np.ndarray
        """
        sel = gemmi.Selection(arg)
        res = []

        for model in sel.models(self.STRUCT):
            for chain in sel.chains(model):
                for residue in sel.residues(chain):
                    for atom in sel.atoms(residue):
                        if exclude_hydrogen and atom.is_hydrogen():
                            continue

                        val = (chain.name,
                               residue.seqid.num,
                               residue.seqid.icode,
                               residue.name,
                               atom.name,
                               atom.element.name,
                               atom.charge,
                               atom.b_iso,
                               atom.occ,
                               tuple(atom.pos.tolist()),
                               )
                        res.append(val)

        return np.array(res, dtype=ATOM)

    def compute_interface(self,
                          chains_x: List[str],
                          chains_y: List[str],
                          threshold: float = 5.0):
        """
        Identify PPI among protein, DNA, RNA using heavy atom distances.
        :param chains_x:
        :param chains_y:
        :param threshold:
        :return:
         PPI residues of chains_x, PPI residues of chains_y
        """
        for ch in chains_x + chains_y:
            if ch not in self.chain_ids:
                raise ValueError("Chain %s not found (only [%s])" % (ch, " ".join(self.chain_ids)))
            elif ch not in self.polymer_types:
                raise ValueError("Chain %s is not a polymer (only [%s])"
                                 % (ch, " ".join(list(self.polymer_types.keys())))
                                 )

        atom_x = self.get_atoms("/1/%s" % ",".join(chains_x), exclude_hydrogen=True)
        atom_y = self.get_atoms("/1/%s" % ",".join(chains_y), exclude_hydrogen=True)

        kd_tree_x = cKDTree(atom_x["coordinate"])
        kd_tree_y = cKDTree(atom_y["coordinate"])

        pairs = kd_tree_x.sparse_distance_matrix(kd_tree_y, threshold, output_type='coo_matrix')
        x_res = np.unique(atom_x[pairs.row][["chain_name", "residue_num", "residue_icode", "residue_name"]])
        y_res = np.unique(atom_y[pairs.col][["chain_name", "residue_num", "residue_icode", "residue_name"]])

        return x_res, y_res
