from odoo import models, fields

class HrRequest(models.Model):
    _name = "hr.request"
    _rec_name = 'nombre' 
    
    nombre = fields.Char("Nombre")
    tipo = fields.Selection([
        ('vacaciones', 'Vacaciones'), 
        ('permiso', 'Permiso'),
        ('anticipo', 'Anticipo'), 
        ('otro', 'Otro'), 
        ], string="Tipo de Solicitud")
    empleado_id = fields.Many2one('hr.employee', "Empleado")
    fecha_solicitud = fields.Date(default=fields.Date.today, string="Fecha de Solicitud")
    estado = fields.Selection([
        ('nuevo','Nuevo'),
        ('aprobado','Aprobado'),
        ('rechazado','Rechazado')
        ], string="Estado", default='nuevo')
    observaciones = fields.Text("Observaciones")

    def aprobar_solicitud(self):
        self.estado = 'aprobado'

    def rechazar_solicitud(self):
        self.estado = 'rechazado'