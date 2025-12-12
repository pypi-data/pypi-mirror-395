# This file is part of SAGE Education.   The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.pool import Pool
from . import company
from . import party
from . import report

def register():
	Pool.register(
		company.Company,
		company.Employee,
        company.Student,
		company.StudentSupervisor,
		party.Party,
		
		module='akademy_company', type_='model'
	)

	Pool.register(
		report.CompanyReport,
		report.EmployeeReport,
		report.StudentReport,

		module='akademy_company', type_='report'
	)

