from odoo import models, fields, api
from datetime import datetime, timedelta


class Student(models.Model):
    _name = 'edu_center.student'
    _description = "Talaba ma'lumotlari"

    name = fields.Char(string='Ism', required=True)
    age = fields.Integer(string='Yosh')
    email = fields.Char(string='Elektron pochta')
    courses = fields.Many2many('edu_center.course', string='Kurslar')


class Course(models.Model):
    _name = 'edu_center.course'
    _description = "Kurs ma'lumotlari"

    name = fields.Char(string='Nomi', required=True)
    teacher_id = fields.Many2one('edu_center.teacher', string='O\'qituvchi')
    students = fields.Many2many('edu_center.student', string='Talabalar')


class Teacher(models.Model):
    _name = 'edu_center.teacher'
    _description = "O'qituvchi ma'lumotlari"

    name = fields.Char(string='Ism', required=True)
    email = fields.Char(string='Elektron pochta')
    courses_taught = fields.One2many('edu_center.course', 'teacher_id', string='O\'qitilgan kurslar')


class Payment(models.Model):
    _name = 'edu_center.payment'
    _description = "To'lov ma'lumotlari"

    student_id = fields.Many2one('edu_center.student', string='Talaba')
    course_id = fields.Many2one('edu_center.course', string='Kurs')
    amount = fields.Float(string='Summa')
    date = fields.Date(string='Sana', default=fields.Date.today())
    description = fields.Text(string="Ta'rif")
    admin_approved = fields.Boolean(string='Admin tasdiqlandi')

    @api.model
    def get_last_week_payments(self):
        last_week_start_date = datetime.now().date() - timedelta(days=7)
        payments = self.search([('date', '>=', last_week_start_date)])
        return payments

    @api.model
    def create(self, vals):
        if self.env.user.has_group('edu_center.group_admin'):
            vals['admin_approved'] = True
        return super(Payment, self).create(vals)

    def write(self, vals):
        if self.env.user.has_group('edu_center.group_admin'):
            vals['admin_approved'] = True
        return super(Payment, self).write(vals)


class Group(models.Model):
    _name = 'edu_center.group'
    _description = 'Guruh ma\'lumotlari'

    name = fields.Char(string='Nomi', required=True)
    course_id = fields.Many2one('edu_center.course', string='Kurs')
    teacher_id = fields.Many2one('edu_center.teacher', string='O\'qituvchi')


class Admin(models.Model):
    _name = 'edu_center.admin'
    _description = "Administrator ma'lumotlari"

    name = fields.Char(string='Ism', required=True)
    role = fields.Selection([('admin', 'Administrator'), ('administrator', 'Admin')], string='Rol')

    @api.onchange('role')
    def _onchange_role(self):
        if self.role == 'admin':
            self.ensure_one()
            self.write({'role': 'admin'})

        if self.role == 'administrator':
            self.ensure_one()
            self.write({'role': 'administrator'})
