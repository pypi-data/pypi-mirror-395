# This file is part of SAGE Education.   The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from . import party

def register():
	Pool.register(
		party.Party,
		
		module='akademy_party', type_='model'
	)

