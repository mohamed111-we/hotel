{
    'name': 'Room Reservation',
    'version': '1.0',
    'summary': 'Manage Room Reservations',
    'description': """
        A module for managing room reservations. 
        Includes functionality for booking, availability checks, and customer management.
    """,
    'author': 'Arafa',
    'website': 'http://www.yourcompany.com',
    'category': 'Hospitality',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'views/room_view.xml',
        'views/reservation_view.xml',
        'views/extra_details_view.xml',

    ],
    'demo': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
