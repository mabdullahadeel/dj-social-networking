from django.apps import AppConfig


class ProfilesConfig(AppConfig):
    name = 'profiles'

    # Signals related stuff
    def ready(self):
        import profiles.signals
