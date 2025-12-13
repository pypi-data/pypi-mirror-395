"""
@Author: Luo Jiejian
"""
import hashlib
import os
import re
import shutil
import subprocess
import uuid
from collections import defaultdict
from importlib.resources import files

import numpy as np
from anarci import run_anarci
from anarci.germlines import all_germlines

from gemmi_protools import StructureParser


def hash_sequence(seq: str) -> str:
    """Hash a sequence."""
    return hashlib.sha256(seq.encode()).hexdigest()


def get_fv_region(in_sequence: str):
    # IMGT number, include start and end
    # https://www.imgt.org/IMGTScientificChart/Nomenclature/IMGT-FRCDRdefinition.html
    # αβTCR：Light chain α, heavy chain β
    # γδTCR：Light chain γ, heavy chain δ
    imgt_scheme = dict(
        fr1=(1, 26),
        cdr1=(27, 38),
        fr2=(39, 55),
        cdr2=(56, 65),
        fr3=(66, 104),
        cdr3=(105, 117),
        fr4=(118, 128),
    )

    mapper = dict()
    num_mapper = dict()
    for k, v in imgt_scheme.items():
        for i in range(v[0], v[1] + 1):
            mapper[i] = k

            if k == "cdr1":
                ki = 1
            elif k == "cdr2":
                ki = 2
            elif k == "cdr3":
                ki = 3
            else:
                ki = 0
            num_mapper[i] = ki

    inputs = [("input", in_sequence)]
    _, numbered, alignment_details, _ = run_anarci(inputs, scheme="imgt", assign_germline=True)
    if numbered[0] is None:
        return []

    outputs = []
    for cur_numbered, cur_details in zip(numbered[0], alignment_details[0]):
        aligned_sites, start, end = cur_numbered
        # add mask
        # 9 for not Fv region
        # 0 for non-CDR region, 1, 2, 3 for CDR region for the current Fv
        mask = np.full(len(in_sequence), fill_value=9, dtype=np.int8)
        mask[start: end + 1] = 0
        i = 0
        for (site_num, _), site_aa in aligned_sites:
            if site_aa != "-":
                mask[i + start] = num_mapper[site_num]
                i += 1

        # region_seq
        regions = defaultdict(list)
        for site in aligned_sites:
            region_name = mapper[site[0][0]]
            regions[region_name].append(site[1])

        max_index = aligned_sites[-1][0][0]
        if max_index < 128:
            for idx in range(max_index + 1, 129):
                region_name = mapper[idx]
                regions[region_name].append("-")

        cdr1_seq = "".join([aa for aa in regions["cdr1"] if aa != "-"])
        cdr2_seq = "".join([aa for aa in regions["cdr2"] if aa != "-"])
        cdr3_seq = "".join([aa for aa in regions["cdr3"] if aa != "-"])

        # germ line V gene [fr1], germ line J gene [fr4]
        chain_type = cur_details["chain_type"]
        v_gene_specie, v_gene = cur_details["germlines"]["v_gene"][0]
        j_gene_specie, j_gene = cur_details["germlines"]["j_gene"][0]

        gl_fr1 = list(
            all_germlines["V"][chain_type][v_gene_specie][v_gene][imgt_scheme["fr1"][0] - 1:imgt_scheme["fr1"][1]])
        gl_fr1_mapper = dict(zip(range(imgt_scheme["fr1"][0], imgt_scheme["fr1"][1] + 1), gl_fr1))

        gl_fr4 = list(
            all_germlines["J"][chain_type][j_gene_specie][j_gene][imgt_scheme["fr4"][0] - 1:imgt_scheme["fr4"][1]])
        gl_fr4_mapper = dict(zip(range(imgt_scheme["fr4"][0], imgt_scheme["fr4"][1] + 1), gl_fr4))

        # repair the gap with gl_fr1 and gl_fr4
        # For FR1
        fixed_fr1 = []
        for site in aligned_sites:
            idx, ins = site[0]
            if imgt_scheme["fr1"][0] <= idx <= imgt_scheme["fr1"][1]:
                if ins == ' ' and site[1] == "-" and gl_fr1_mapper[idx] != "-":
                    fixed_fr1.append(gl_fr1_mapper[idx])
                else:
                    fixed_fr1.append(site[1])

        # For FR4
        fixed_fr4 = []
        for site in aligned_sites:
            idx, ins = site[0]
            if imgt_scheme["fr4"][0] <= idx <= imgt_scheme["fr4"][1]:
                if ins == ' ' and site[1] == "-" and gl_fr4_mapper[idx] != "-":
                    fixed_fr4.append(gl_fr4_mapper[idx])
                else:
                    fixed_fr4.append(site[1])

        # update regions
        regions["fr1"] = fixed_fr1
        regions["fr4"] = fixed_fr4

        fixed_fv_seq = []
        for r_name in ["fr1", "cdr1", "fr2", "cdr2", "fr3", "cdr3", "fr4"]:
            for aa in regions[r_name]:
                if aa != "-":
                    fixed_fv_seq.append(aa)
        fixed_fv_seq = "".join(fixed_fv_seq)

        outputs.append(dict(Fv_aa=fixed_fv_seq,
                            classification=v_gene[0:2],
                            chain_type=chain_type,
                            v_gene=v_gene_specie + "/" + v_gene,
                            j_gene=j_gene_specie + "/" + j_gene,
                            cdr1_aa=cdr1_seq,
                            cdr2_aa=cdr2_seq,
                            cdr3_aa=cdr3_seq,
                            mask="".join([str(i) for i in mask.tolist()])
                            )
                       )
    return outputs


def fv_region_type(inputs: list[dict]):
    n = len(inputs)
    if n == 0:
        return "not-Fv"
    elif n == 1:
        clf = inputs[0]["classification"]
        ct = inputs[0]["chain_type"]

        v = "%s%s" % (clf, ct)
        if v in ["IGH", "TRB", "TRD"]:
            return "%s/VH" % clf
        elif v in ["IGK", "IGL", "TRA", "TRG"]:
            return "%s/VL" % clf
        else:
            return "other"
    elif n == 2:
        p = {"%s%s" % (item["classification"], item["chain_type"]) for item in inputs}
        if p in [{"IGH", "IGL"}, {"IGH", "IGK"}, {"TRA", "TRB"}, {"TRG", "TRD"}]:
            clf = p.pop()[0:2]
            return "%s/scFv" % clf
        else:
            return "other"
    else:
        return "other"


def annotate_mhc(seq_dict: dict):
    """

    Args:
        seq_dict: dict,
                key: ch_id
                val: protein seq

    Returns:

    """
    hmm_model = str(files("gemmi_protools.data") / "MHC" / "MHC_combined.hmm")
    # save sequences to fasta
    # all chains of biomolecule
    home_dir = os.path.expanduser("~")
    tmp_dir = os.path.join(home_dir, str(uuid.uuid4()))
    os.makedirs(tmp_dir)

    fasta_file = os.path.join(tmp_dir, "input.fasta")
    with open(fasta_file, "w") as fo:
        for ch_id, seq in seq_dict.items():
            print(">%s" % ch_id, file=fo)
            print(seq, file=fo)

    result_file = os.path.join(tmp_dir, "result.txt")
    _path = shutil.which("hmmscan")

    if _path is None:
        raise RuntimeError("hmmscan is not found.")

    cmd = "%s --tblout %s --cut_ga %s %s" % (_path, result_file, hmm_model, fasta_file)

    try:
        _ = subprocess.run(cmd, shell=True, check=True,
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    except subprocess.CalledProcessError as ce:
        raise Exception(ce)
    else:
        out = dict()
        with open(result_file, "r") as fi:
            for li in fi:
                if not re.match("#", li.strip()):
                    tmp = re.split(r"\s+", li.strip())[0:3]
                    out[tmp[2]] = tmp[0]
    finally:
        if os.path.isdir(tmp_dir):
            shutil.rmtree(tmp_dir)
    return out


def annotate_pdb(struct_file: str):
    st = StructureParser()
    st.load_from_file(struct_file)
    st.clean_structure()

    subchain_id2entity_id = st.subchain_id_to_entity_id

    # Merge sequences
    polymers = dict()
    for ch, seq in st.polymer_sequences().items():
        subchain_id = st.get_chain(ch).get_polymer().subchain_id()
        entity_id = subchain_id2entity_id[subchain_id]

        hash_id = hash_sequence(seq.upper())
        if hash_id not in polymers:
            val = dict(chain_ids=[ch],
                       sequence=seq.upper(),
                       type=st.polymer_types[ch].name,
                       description=st.INFO["description"].get(entity_id, "Unknown"),
                       )
            polymers[hash_id] = val
        else:
            polymers[hash_id]["chain_ids"].append(ch)

    proteins = dict()
    results = dict()
    for hash_id, val in polymers.items():
        val["chain_ids"].sort()
        if val["type"] == "PeptideL":
            proteins[hash_id] = val["sequence"]
            anarci_info = get_fv_region(val["sequence"])
            fvt = fv_region_type(anarci_info)
            if fvt != "not-Fv":
                results[hash_id] = dict(fv_type=fvt, annotations=anarci_info)

    struct_info = {k: st.INFO[k] for k in ["resolution", "pdb_id", "deposition_date", "method", "title"]}
    return dict(path=os.path.abspath(os.path.expanduser(struct_file)),
                info=struct_info,
                polymers=polymers,
                anarci=results,
                mhc=annotate_mhc(proteins) if len(proteins) > 0 else dict(),
                )
