# This file is part of SAGE Education.   The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.report import Report
from trytond.pool import Pool
from datetime import date


class CompanyReport(Report):
    __name__ = 'akademy_report.company.report'

    @classmethod
    def get_context(cls, records, header, data):
        Company = Pool().get('company.company')
        
        context = super().get_context(records, header, data)
        company = Company.browse(data['ids'])

        context['company'] = company
        context['create_date'] = date.today()        
        return context
   

class EmployeeReport(Report):
    __name__ = 'akademy_report.company.employee.report'

    @classmethod
    def get_context(cls, records, header, data):
        Employee = Pool().get('company.employee')
        
        context = super().get_context(records, header, data)
        employee = Employee.browse(data['ids'])

        context['employee'] = employee
        context['create_date'] = date.today()        
        return context


class StudentReport(Report):
    __name__ = 'akademy_report.company.student.report'

    @classmethod
    def get_context(cls, records, header, data):
        Student = Pool().get('company.student')
        
        context = super().get_context(records, header, data)
        student = Student.browse(data['ids'])

        context['student'] = student
        context['create_date'] = date.today()        
        return context