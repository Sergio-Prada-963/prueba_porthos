{
    'name': 'Solicitudes',
    'version': '17.0.1.0.0',
    'summary': 'Modulo para la gestion de solicitudes de vacaciones, permisos, anticipos y otros',
    'description': """
        Este módulo permite a los empleados crear solicitudes de vacaciones, permisos, anticipos y otros tipos de solicitudes.
    """,
    'category': 'Employees',
    'author': 'Sergio Prada',
    'depends': ['hr'],
    'data': [
        "security/ir.model.access.csv",
        "security/record_rules.xml",

        "views/hr_request_views.xml",

        "data/hr_employee_data.xml",
        "data/hr_request_data.xml",
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
