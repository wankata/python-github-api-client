class User:
    """
    User model

    Container for all GitHub user attributes *except plan* information
    """

    __slots__ = frozenset(('login', 'id', 'node_id', 'avatar_url', 'gravatar_id', 'url', 'html_url',
                           'followers_url', 'following_url', 'gists_url', 'starred_url',
                           'subscriptions_url', 'organizations_url', 'repos_url', 'events_url',
                           'received_events_url', 'type', 'site_admin', 'name', 'company', 'blog',
                           'location', 'email', 'hireable', 'bio', 'twitter_username',
                           'public_repos', 'public_gists', 'followers', 'following', 'created_at',
                           'updated_at'))

    def __init__(self, initial: dict = None):
        """
        All not provided user attributes will be set to None.
        Non-allowed attributes raise AttributeError with list of the incorrect attrs provided.
        """

        if initial is None:
            initial = {}

        dict_keys = set(initial)
        if not dict_keys.issubset(self.__slots__):
            raise AttributeError(*(dict_keys - self.__slots__))

        for attr in self.__slots__:
            setattr(self, attr, initial.get(attr, None))
