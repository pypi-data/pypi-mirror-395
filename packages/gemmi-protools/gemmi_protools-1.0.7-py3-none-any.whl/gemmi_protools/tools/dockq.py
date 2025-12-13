"""
@Author: Luo Jiejian
"""
import json
import os
import shutil
import subprocess
import tempfile
from copy import deepcopy
from typing import List, Tuple

import gemmi
import pandas as pd

from gemmi_protools.io.reader import StructureParser


def dockq_score_interface(query_model: str,
                          native_model: str,
                          partner_1_mapping: List[Tuple[str, str]],
                          partner_2_mapping: List[Tuple[str, str]],
                          ):
    """
    Calculate Dockq Score for an interface (partner 1 vs partner 2)

    :param query_model: str
        path of query model, support .pdb, .pdb.gz, .cif, .cif.gz
    :param native_model:
    :param partner_1_mapping: a list of chain ID mapping between query and native for partner1 of the interface
        e.g. [(q chain1, n chain1), (q chain2, n chain2)]
    :param partner_2_mapping:
    :return:
    """
    dockq_program = shutil.which("DockQ")
    if dockq_program is None:
        raise RuntimeError("DockQ is need")

    assert len(partner_1_mapping) > 0, "partner_1_mapping must be a list of chain ID tuples, can't be empty"
    assert len(partner_2_mapping) > 0, "partner_2_mapping must be a list of chain ID tuples, can't be empty"

    def load_struct(path: str, partner_1: List[str], partner_2: List[str]):
        st = StructureParser()
        st.load_from_file(path)
        st.clean_structure()

        for ch in partner_1 + partner_2:
            if ch not in st.chain_ids:
                raise ValueError("Chain %s not found for %s (only [%s])" % (ch, path, " ".join(st.chain_ids)))

        # merge chains in each each partner into on chain
        # partner_1 with chain ID A
        # partner_2 with chain ID B

        chain_a = gemmi.Chain("A")
        idx_a = 1
        for ch in partner_1:
            for res in st.get_chain(ch):
                nr = deepcopy(res)
                nr.seqid.icode = " "
                nr.seqid.num = idx_a
                chain_a.add_residue(nr)
                idx_a += 1

        chain_b = gemmi.Chain("B")
        idx_b = 1
        for ch in partner_2:
            for res in st.get_chain(ch):
                nr = deepcopy(res)
                nr.seqid.icode = " "
                nr.seqid.num = idx_b
                chain_b.add_residue(nr)
                idx_b += 1

        model = gemmi.Model(1)
        model.add_chain(chain_a)
        model.add_chain(chain_b)

        struct = gemmi.Structure()
        struct.add_model(model)

        output = StructureParser(struct)
        return output

    partner_1_query, partner_1_native = list(zip(*partner_1_mapping))
    partner_2_query, partner_2_native = list(zip(*partner_2_mapping))

    q_st = load_struct(query_model, list(partner_1_query), list(partner_2_query))
    n_st = load_struct(native_model, list(partner_1_native), list(partner_2_native))

    with tempfile.TemporaryDirectory() as tmp_dir:
        result_file = os.path.join(tmp_dir, "result.json")
        q_file = os.path.join(tmp_dir, "q.pdb")
        n_file = os.path.join(tmp_dir, "n.pdb")
        q_st.to_pdb(q_file, write_minimal_pdb=True)
        n_st.to_pdb(n_file, write_minimal_pdb=True)

        mapping = "AB:AB"

        _command = "%s --mapping %s --json %s %s %s" % (dockq_program, mapping, result_file, q_file, n_file)
        metrics = ['DockQ', 'F1', 'chain1', 'chain2']

        try:
            _ = subprocess.run(_command, shell=True, check=True,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               timeout=300.0)
        except subprocess.CalledProcessError as e:
            # Handle errors in the called executable
            msg = e.stderr.decode()
            outputs = pd.DataFrame(columns=metrics)
        except Exception as e:
            # Handle other exceptions such as file not found or permissions issues
            msg = str(e)
            outputs = pd.DataFrame(columns=metrics)
        else:
            with open(result_file, "r") as fin:
                vals = json.load(fin)
            msg = "Finished"
            result = []
            for v in vals["best_result"].values():
                result.append(v)
            outputs = pd.DataFrame(result)[metrics]

        if len(outputs) > 0:
            score = "%.4f" % outputs.iloc[0]["DockQ"]
        else:
            score = ""

        return dict(score=score, status=msg)
