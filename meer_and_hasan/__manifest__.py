{
    'name': "Meer & Hasan",
    'version': '1.0',
    'author': "M Mustajab Shahid",
    'category': 'Law Chamber',
    'description': """
    Meer and Hasan Law Chamber
    """,
    'sequence': -100,
    # data files always loaded at installation
    'data': [
        'views/matter.xml',
        'views/menu.xml',
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/district.xml',
        'views/courtType.xml',
        'views/caseStatus.xml',
        'views/settings.xml'
    ],
    'depends': ['sale'],
    # data files containing optionally loaded demonstration data
    'demo': [
    ],
    'application': True,
}
