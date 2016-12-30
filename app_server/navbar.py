from flask_nav.elements import View, Subgroup

from helpers.ui.bootstrap import CustomNavbar

logged_in_nav_bar = CustomNavbar(
    'Checkers Online',
    [
        View('Home', '.show_index'),
        View('Friends', '.show_friends'),
        View('Games', '.show_games')
    ], [
        Subgroup('Account',
                 View('Settings', '.show_account_settings'),
                 View('Sign out', '.logout'),
                 ),
    ]
)
not_logged_in_nav_bar = CustomNavbar(
    'Checkers Online',
    [
        View('Home', '.show_index')
    ], [
        Subgroup('Account',
                 View('Sign in', '.login'),
                 View('Sign up', '.register'))
    ]
)
