# This file is part of SAGE Education.   The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import fields
from trytond.pool import PoolMeta


class Party(metaclass=PoolMeta):
    'Party'
    __name__ = 'party.party'
    
    student = fields.One2Many('company.student', 'party', 'Discente')    

