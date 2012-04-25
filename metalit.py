#!/usr/bin/env python
"""
Literature review assistant.

"""
from __future__ import print_function

import os
import sys
from StringIO import StringIO

import yaml

from mendeley import MendeleyDatabaseInterface

def latex_output(paper):
    section_heading = '{authors} - {year} - {title} - {publication}'.format(**paper)

    output = [r'\section{' + section_heading + '}']
    notes = paper.get('notes')
    if notes:
        output.append(notes)

    for feature, details in paper.get('features', {}).iteritems():
        output.append(r'\subsection{' + feature.capitalize() + '}')
        output.extend([r'\textbf{' + k.capitalize() + '} - ' + v.capitalize() + '\n\n' for k,v in details.iteritems() 
                        if k != 'notes'])

        featurenotes = details.get('notes')
        if featurenotes:
            output.append(featurenotes)

    return '\n'.join(output)

def main():
    assert len(sys.argv) == 2, 'Usage: {0} input'.format(sys.argv[0])
    assert os.path.exists(sys.argv[1])


    db = MendeleyDatabaseInterface()

    lit = yaml.load(file(sys.argv[1]))

    for paper in lit.get('literature', []):
        citekey = paper.get('mendeley')

        # Only support fetching references from the
        # Mendeley database.
        if not citekey:
            continue

        reference = db.get_reference_by_citation_key(citekey)
        paper.update({key:getattr(reference, key) for key in 
                      ['authors', 'year', 'title', 'publication']})

        # For the time being just output data as LaTeX.
        print(latex_output(paper))

if __name__ == '__main__':
    main()
