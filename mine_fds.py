"""
FCA - Python libraries to support FCA tasks
Copyright (C) 2017  

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""
# Kyori code.
from __future__ import print_function
import argparse
import time
from fca.algorithms import lst2str
from fca.algorithms.canonical_base import PSCanonicalBase
from fca.defs.patterns.hypergraphs import TrimmedPartitionPattern
from fca.io.transformers import List2PartitionsTransformer
from fca.io.sorters import PartitionSorter
from fca.io.input_models import PatternStructureModel
import json

def mine_fds(filepath, output_fname=None, rule_fname=None):
    """
    Based on Example 21: Duquenne Guigues Base using TrimmedPartitions with PreviousClosure OnDisk - Streaming patterns to disk
    """
    t0 = time.time()
    if rule_fname is None:
        rule_fname = filepath[:filepath.rfind('.')] + '.rules.json'

    transposed = True
    TrimmedPartitionPattern.reset()

    fctx = PatternStructureModel(
        filepath=filepath,
        transformer=List2PartitionsTransformer(transposed),
        sorter=PartitionSorter(),
        transposed=transposed,
        file_manager_params={
            'style': 'tab'
        }
    )
    canonical_base = PSCanonicalBase(
        # PSPreviousClosure(
        fctx,
        pattern=TrimmedPartitionPattern,
        lazy=False,
        silent=False,
        ondisk=True,
        ondisk_kwargs={
            'output_path':'/tmp',
            'output_fname': output_fname,
            'write_support':True,
            'write_extent':False
            }
    )
    print ("\t=> Execution Time: {} seconds".format(time.time()-t0))
    output_path = canonical_base.poset.close()
    print ("\t=> Pseudo closures stored in {}".format(output_path))

    fctx.transformer.attribute_index = {i:j for i, j in enumerate(fctx.sorter.processing_order)}
    # print(fctx.transformer.attribute_index)

    rules = []

    for i, (rule, support) in enumerate(canonical_base.get_implications()):
        rules.append(rule)
        # ant, con = rule
        # print('{}: {:10s} => {:10s}'.format(i+1, lst2str(ant), lst2str(con)), support)
    print ('{} Rules found'.format(len(rules)))
    
    with open(rule_fname, 'w') as fout:
        json.dump(rules, fout)
        print ("\t=> Implications stored in {}".format(rule_fname))
    

if __name__ == '__main__':
    __parser__ = argparse.ArgumentParser(
        description='Example 21: Duquenne Guigues Base using TrimmedPartitions with PreviousClosure OnDisk - Streaming patterns to disk'
    )
    __parser__.add_argument(
        'context_path',
        metavar='context_path',
        type=str,
        help='path to the formal context'
    )
    __parser__.add_argument(
        '-o',
        '--output_fname',
        metavar='output_fname',
        type=str,
        help='Output file to save formal concepts',
        default=None
    )
    __parser__.add_argument(
        '-r',
        '--output_fname_rules',
        metavar='output_fname_rules',
        type=str,
        help='Output file to save implications',
        default=None
    )

    __args__ = __parser__.parse_args()
    mine_fds(__args__.context_path, __args__.output_fname, __args__.output_fname_rules)
