from specter import Spec, incomplete


class Server(Spec):
    """ Smoke tests around server-side IO. """

    class Connection(Spec):
        @incomplete
        def can_start_an_io_loop(self):
            pass

        @incomplete
        def can_stop_the_io_loop(self):
            pass

        @incomplete
        def handles_multiple_connections(self):
            pass

    class StandardIn(Spec):
        @incomplete
        def can_accept_stdin(self):
            pass

        @incomplete
        def stdin_is_converted_into_a_message(self):
            pass

    class Messages(Spec):
        @incomplete
        def delivers_a_message(self):
            pass

        @incomplete
        def delivers_multiple_messages(self):
            pass

        @incomplete
        def delivers_to_multiple_clients(self):
            pass
