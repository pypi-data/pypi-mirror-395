"""
@Author: Luo Jiejian
"""

import os
import re
import shutil
import subprocess
import tempfile
import string
from typing import Literal, Optional, Dict, Any, List

import numpy as np
from Bio.Align import PairwiseAligner, substitution_matrices
from Bio.PDB import Superimposer

from gemmi_protools import StructureParser
from gemmi_protools.io.convert import gemmi2bio, bio2gemmi


def check_sequence(seq: str):
    """
    Remove space, star at the end, and \n, upper the letters
    Check sequence is valid or not

    :param seq:str
    :return:

    """
    seq_clean = re.sub(pattern=r" |\*|-", repl='', string=seq.upper().strip())
    if len(seq_clean) == 0:
        raise ValueError("Sequence is empty")

    s = re.sub(pattern=r"[A-Z]", repl="", string=seq_clean)
    if len(s) > 0:
        raise ValueError("Sequence has Non-alphabetic characters: %s" % str(set(s)))

    return seq_clean


def align_sequences(seq1: str,
                    seq2: str,
                    seq_type: Literal["dna", "rna", "protein"] = "protein",
                    mode: Literal["global", "local"] = "local",
                    substitution_matrix: Optional[str] = None,
                    open_gap_score: Optional[float] = None,
                    extend_gap_score: Optional[float] = None,
                    ):
    default_params = {
        "dna": {
            "matrix": "NUC.4.4",
            "open_gap_score": -10.0,
            "extend_gap_score": -0.5,
            "mode": "global"
        },
        "rna": {
            "matrix": "NUC.4.4",
            "open_gap_score": -10.0,
            "extend_gap_score": -0.5,
            "mode": "global"
        },
        "protein": {
            "matrix": "BLOSUM62",
            "open_gap_score": -11.0,
            "extend_gap_score": -1.0,
            "mode": "global"
        }

    }

    available_matrices = {
        "dna": ["NUC.4.4"],
        "rna": ["NUC.4.4"],
        "protein": ["BLOSUM45", "BLOSUM50", "BLOSUM62",
                    "BLOSUM80", "BLOSUM90",
                    "PAM30", "PAM70", "PAM250"]
    }

    seq1 = check_sequence(seq1)
    seq2 = check_sequence(seq2)

    params = default_params[seq_type].copy()
    a_mats = available_matrices[seq_type]

    if substitution_matrix is not None:
        if substitution_matrix not in a_mats:
            raise ValueError("substitution matrix `%s` not support for %s" % (substitution_matrix, seq_type))
        else:
            params["matrix"] = substitution_matrix

    if open_gap_score is not None:
        params["open_gap_score"] = open_gap_score
    if extend_gap_score is not None:
        params["extend_gap_score"] = extend_gap_score

    params["mode"] = mode
    # Finish parameters checking and setting
    aligner = PairwiseAligner()
    aligner.mode = params["mode"]
    aligner.substitution_matrix = substitution_matrices.load(params["matrix"])
    aligner.open_gap_score = params["open_gap_score"]
    aligner.extend_gap_score = params["extend_gap_score"]

    best_alignment = aligner.align(seq1, seq2)[0]

    aligned_seq1, aligned_seq2 = best_alignment

    # start from 1
    aa_mapper = dict()
    i = 0
    j = 0

    ins_letters = string.ascii_uppercase
    k = 0

    for aa1, aa2 in zip(aligned_seq1, aligned_seq2):
        if aa1 != "-":
            i += 1
        if aa2 != "-":
            j += 1
            # reset k
            if k > 0:
                k = 0

        if aa1 != "-" and aa2 != "-":
            aa_mapper[i] = (j, "")

        # for insertion of seq1
        if aa1 != "-" and aa2 == "-":
            aa_mapper[i] = (j, ins_letters[k])
            k += 1

    # from align idx to sequence idx
    # tmap_1 = re.search(aligned_seq1.replace("-", ""), seq1)
    # tmap_2 = re.search(aligned_seq2.replace("-", ""), seq2)
    # shift_1 = tmap_1.span()[0]
    # shift_2 = tmap_2.span()[0]

    shift_1, shift_2 = best_alignment.coordinates[:, 0]
    out_mapper = {k + shift_1: "%d%s" % (v[0] + shift_2, v[1]) for k, v in aa_mapper.items()}

    ident = best_alignment.counts().identities / best_alignment.length
    n_aligned = best_alignment.length - best_alignment.counts().gaps

    coverage_1 = n_aligned / len(seq1)
    coverage_2 = n_aligned / len(seq2)

    return dict(seq1=seq1,
                seq2=seq2,
                aligned_seq1=aligned_seq1,
                aligned_seq2=aligned_seq2,
                alignment_length=best_alignment.length,
                aligned_aa_mapper=out_mapper,
                identity=round(ident, 3),
                coverage_1=round(coverage_1, 3),
                coverage_2=round(coverage_2, 3),
                # aln=best_alignment
                )


class StructureAligner(object):
    def __init__(self, query_path: str, ref_path: str):
        self._query_st = StructureParser()
        self._query_st.load_from_file(query_path)

        self._ref_st = StructureParser()
        self._ref_st.load_from_file(ref_path)

        self.values = dict()
        self.rot_mat = None
        self.is_aligned = False
        self.by_query = None
        self.by_ref = None
        self.query_path = query_path
        self.ref_path = ref_path

    @property
    def __mmalign_path(self):
        _path = shutil.which("MMAlign") or shutil.which("MMalign")
        if _path is None:
            raise RuntimeError("Executable program MMAlign is not found. "
                               "Download from https://zhanggroup.org/MM-align/ ."
                               "Build it and add MMAlign to environment PATH")
        else:
            return _path

    @staticmethod
    def __parser_rotation_matrix(matrix_file: str):
        rotation_matrix = []
        translation_vector = []

        with open(matrix_file, 'r') as file:
            lines = file.readlines()
            values = lines[2:5]
            for cur_line in values:
                tmp = re.split(pattern=r"\s+", string=cur_line.strip())
                assert len(tmp) == 5
                rotation_matrix.append(tmp[2:])
                translation_vector.append(tmp[1])
        return dict(R=np.array(rotation_matrix).astype(np.float32),
                    T=np.array(translation_vector).astype(np.float32))

    @staticmethod
    def __parse_terminal_outputs(output_string: str) -> Dict[str, Any]:
        lines = re.split(pattern=r"\n", string=output_string)
        # chain mapping
        patterns = dict(query_chain_ids=r"Structure_1.+\.pdb:([\w:]+)",
                        ref_chain_ids=r"Structure_2.+\.pdb:([\w:]+)",
                        query_total_length=r"Length of Structure_1.*?(\d+).*residues",
                        ref_total_length=r"Length of Structure_2.*?(\d+).*residues",
                        aligned_length=r"Aligned length=.*?(\d+)",
                        rmsd=r"RMSD=.*?([\d.]+)",
                        tmscore_by_query=r"TM-score=.*?([\d.]+).+Structure_1",
                        tmscore_by_ref=r"TM-score=.*?([\d.]+).+Structure_2",
                        aligned_seq_start=r"denotes other aligned residues",
                        )

        values = dict()
        for idx, line in enumerate(lines):
            current_keys = list(patterns.keys())
            for key in current_keys:
                tmp = re.search(patterns[key], line)
                if tmp:
                    if key in ['query_chain_ids', 'ref_chain_ids']:
                        values[key] = re.split(pattern=":", string=tmp.groups()[0])
                        del patterns[key]
                    elif key in ['query_total_length', 'ref_total_length', 'aligned_length']:
                        values[key] = int(tmp.groups()[0])
                        del patterns[key]
                    elif key in ['rmsd', 'tmscore_by_query', 'tmscore_by_ref']:
                        values[key] = float(tmp.groups()[0])
                        del patterns[key]
                    elif key == "aligned_seq_start":
                        # idx + 1 and idx + 3 for aligned sequences 1 and 2
                        seq_1 = lines[idx + 1]
                        seq_2 = lines[idx + 3]

                        sp1 = re.split(pattern=r"\*", string=seq_1)
                        sp2 = re.split(pattern=r"\*", string=seq_2)
                        values["query_sequences"] = sp1[:-1] if "*" in seq_1 else sp1
                        values["ref_sequences"] = sp2[:-1] if "*" in seq_2 else sp2
                        del patterns[key]
        return values

    def make_alignment(self, query_chains: Optional[List[str]] = None,
                       ref_chains: Optional[List[str]] = None, timeout=300.0):
        """

        :param
        query_chains: list, None
        for all chains
            :param
        ref_chains: list, None
        for all chains
            :param
        timeout: default
        300
        :return:
        """

        program_path = self.__mmalign_path

        # clone
        if isinstance(query_chains, list):
            q_st = self._query_st.pick_chains(query_chains)
        else:
            q_st = self._query_st

        if isinstance(ref_chains, list):
            r_st = self._ref_st.pick_chains(query_chains)
        else:
            r_st = self._ref_st

        q_ch_mapper = q_st.make_one_letter_chain()
        r_ch_mapper = r_st.make_one_letter_chain()

        q_ch_mapper_r = {v: k for k, v in q_ch_mapper.items()}
        r_ch_mapper_r = {v: k for k, v in r_ch_mapper.items()}

        with tempfile.TemporaryDirectory() as tmp_dir:
            _tmp_a = os.path.join(tmp_dir, "a.pdb")
            q_st.to_pdb(_tmp_a)

            _tmp_b = os.path.join(tmp_dir, "b.pdb")
            r_st.to_pdb(_tmp_b)

            matrix_file = os.path.join(tmp_dir, "m.txt")
            _command = "%s %s %s -m %s" % (program_path, _tmp_a, _tmp_b, matrix_file)

            try:
                result = subprocess.run(_command, shell=True, check=True,
                                        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                        timeout=timeout)
            except Exception as e:
                print("%s: between files %s and %s; between chains: %s and %s" % (
                    str(e), self.query_path, self.ref_path,
                    str(q_st.chain_ids), str(r_st.chain_ids))
                      )
            else:
                self.values = self.__parse_terminal_outputs(result.stdout.decode())
                self.rot_mat = self.__parser_rotation_matrix(matrix_file)
                self.is_aligned = True
                self.by_query = q_st.chain_ids if query_chains is None else query_chains
                self.by_ref = r_st.chain_ids if ref_chains is None else ref_chains
                self.values["query_chain_ids"] = [q_ch_mapper_r.get(ch, ch) for ch in self.values["query_chain_ids"]]
                self.values["ref_chain_ids"] = [r_ch_mapper_r.get(ch, ch) for ch in self.values["ref_chain_ids"]]

    def save_aligned_query(self, out_file: str):
        """

        :param
        out_file:.cif
        file
        :return:
        """
        if not self.is_aligned:
            raise RuntimeError("structure not aligned, run make_alignment first")

        super_imposer = Superimposer()
        super_imposer.rotran = (self.rot_mat["R"].T, self.rot_mat["T"])

        bio_s = gemmi2bio(self._query_st.STRUCT)
        super_imposer.apply(bio_s)
        query_st_aligned = bio2gemmi(bio_s)

        block = query_st_aligned.make_mmcif_block()
        block.write_file(out_file)
