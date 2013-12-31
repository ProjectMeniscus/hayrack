from specter import Spec, incomplete


class Client(Spec):
    """ Smoke tests around the client-side receiver. """

    class Connection(Spec):
        @incomplete
        def can_create_connection_object(self):
            pass

        @incomplete
        def can_connect(self):
            pass

        @incomplete
        def can_close(self):
            pass

    class Messages(Spec):
        @incomplete
        def retrieve_a_message(self):
            pass

        @incomplete
        def get_message_is_blocking(self):
            pass
