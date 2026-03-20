{
    'name': "Artline Task: Sale Customization",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "Marat",
    'website': "https://www.yourcompany.com",

    'category': 'Sales',
    'version': '1.0',

    'depends': ['sale', 'hr'],

    'data': [
        'views/sale_order_views.xml',
        'reports/sale_order_report.xml',
    ],
    'installable': True,
}
