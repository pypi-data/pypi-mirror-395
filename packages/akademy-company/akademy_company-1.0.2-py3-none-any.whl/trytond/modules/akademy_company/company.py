# This file is part of SAGE Education.   The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.model import ModelSQL, ModelView, fields, Unique
from trytond.transaction import Transaction
from trytond.pyson import Eval, If
from trytond.pool import PoolMeta
from datetime import date


_DEGREE_KINSHIP = [
    # Parentesco direto (linha reta)
    ('pai', 'Pai'),
    ('mae', 'Mãe'),
    ('padrasto', 'Padrasto'),
    ('madrasta', 'Madrasta'),
    ('filho', 'Filho'),
    ('filha', 'Filha'),
    ('avo', 'Avô'),
    ('avoa', 'Avó'),
    ('bisavo', 'Bisavô'),
    ('bisavoa', 'Bisavó'),

    # Parentesco colateral
    ('irmao', 'Irmão'),
    ('irma', 'Irmã'),
    ('tio', 'Tio'),
    ('tia', 'Tia'),
    ('primo', 'Primo'),
    ('prima', 'Prima'),
    ('sobrinho', 'Sobrinho'),
    ('sobrinha', 'Sobrinha'),

    # Afinidade ou tutela
    ('tutor_legal', 'Tutor Legal'),
    ('encarregado', 'Encarregado'),
    ('guardiao', 'Guardião'),
    ('cuidador', 'Cuidador(a)'),
    ('companheiro_pai', 'Companheiro(a) do Pai'),
    ('companheiro_mae', 'Companheiro(a) da Mãe'),
    ('padrinho', 'Padrinho'),
    ('madrinha', 'Madrinha'),

    # Outros vínculos
    ('amigo_familia', 'Amigo da Família'),
    ('responsavel', 'Responsável'),
    ('outro', 'Outro'),
]



class Company(metaclass=PoolMeta):
    'Company'
    __name__ = 'company.company'
    
    party = fields.Many2One(
        'party.party', 'Party', 
        domain=[
            ('is_institution', '=', True)
            ], required=True,
        ondelete='CASCADE')
    student = fields.One2Many('company.student', 'company', 'Discentes',
        help="Adicionar discentes a instituição.")


class Employee(metaclass=PoolMeta):
    'Employee'
    __name__ = 'company.employee'
       
    teacher = fields.Boolean(
        'Docente', 
        help="A entidade será tratada como docente.")
    party = fields.Many2One(
        'party.party', 'Entidade', 
        domain=[
            ('is_person', '=', True)
            ], required=True, 
        context={
            'company': If(
                Eval('company', -1) >= 0, Eval('company', None), None),
            },
        depends={'company'}, ondelete="RESTRICT",
        help="Escolha a entidade que vau representar o funcionário.")

    @classmethod
    def __setup__(cls):
        super(Employee, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('key', Unique(table, table.party, table.company), 
            u'Não foi possível cadastrar o(a) novo(a) funcionário(a), por favor verificar se o(a) funcionário(a) já existe.')
        ]
        cls._order = [('party', 'ASC')]

    @classmethod
    def default_start_date(cls):
        return date.today()  
    

class Student(ModelSQL, ModelView):
    'Student'
    __name__ = 'company.student'

    code = fields.Char('Nº de matrícula', size=20,
        help="Número de matrícula do discente.")
    start_date = fields.Date('Início',
        domain=[
                If(
                    (Eval('start_date')) & (Eval('end_date')),
                    ('start_date', '<=', Eval('end_date')),
                    (),
                )
            ], depends={'end_date'},
        required=True, help="Início da formação.")
    end_date = fields.Date('Fim',
        domain=[
                If(
                    (Eval('start_date')) & (Eval('end_date')),
                    ('end_date', '>=', Eval('start_date')),
                    (),
                )
            ], depends=['start_date'],
        help="Fim da formação.")    
    party = fields.Many2One(
        'party.party', 'Entidade', 
        required=True, domain=[
            ('is_person', '=', True)
            ], ondelete="RESTRICT",
        help="Nome do discente.")
    company = fields.Many2One(
        'company.company', 'Instituição',
        readonly=True, ondelete="RESTRICT",
        help="Nome da instituição.")     
    student_supervisor = fields.One2Many('company.student.supervisor', 
        'student', 'Discente')      
    
    @classmethod
    def __setup__(cls):
        super(Student, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('key', Unique(table, table.party, table.company),
            u'Não foi possível cadastrar o(a) novo(a) discente, por favor verificar se o(a) discente já existe.')
        ]
        cls._order = [('party', 'ASC')]
        
    @classmethod
    def default_start_date(cls):
        return date.today()

    @staticmethod
    def default_company():
        transaction = Transaction()
        if transaction:
            return transaction.company
            
        #return Transaction().context.get('company')

    def get_rec_name(self, name):
        return self.party.rec_name

    @classmethod
    def search_rec_name(cls, name, clause):
        return [('party.rec_name',) + tuple(clause[1:])]


class StudentSupervisor(ModelSQL, ModelView):
    'Student Supervisor'
    __name__ = 'company.student.supervisor'    
	
    description = fields.Text('Descrição')
    degree_kinship = fields.Selection(_DEGREE_KINSHIP, 
        string=u'Grau parentesco', required=True)
    phone_number = fields.Char('Telefone', size=20,
        help="Número de telefone")
    is_primary = fields.Boolean('Principal', 
        help='Indica se é o encarregado principal')    
    student = fields.Many2One('company.student', 'Discente', required=True)
    party = fields.Many2One('party.party', 'Encarregado', required=True)

    @classmethod
    def __setup__(cls):
        super(StudentSupervisor, cls).__setup__()
        table = cls.__table__()
        cls._sql_constraints = [
            ('key', Unique(table, table.party, table.student), 
            u'Não foi possível cadastrar o(a) novo(a) encarregado(a), por favor verificar se o(a) encarregado(a) já está associado ao discente.')
        ]

    def get_rec_name(self, name):
        return self.party.rec_name

    @classmethod
    def search_rec_name(cls, name, clause):
        return [('party.rec_name',) + tuple(clause[1:])]