from flask_nav.elements import View, Navbar, Subgroup

nav_bar = Navbar(
    'Checkers Online',
    View('Home', '.show_index'),
    View('Friends', '.show_friends'),
    View('Games', '.show_games'),
    Subgroup('Account',
             View('Settings', '.show_account_settings'),
             View('Log out', '.logout')
             )
)