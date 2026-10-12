import socket
import unittest

import utils.networking as net

class TestDisconnect(unittest.TestCase):
    """Tests for detecting players who leave mid-game (issue #73)."""

    def test_closed_connection_raises_error(self):
        """When a player quits, receive_message should raise ConnectionResetError."""
        banker_side, player_side = socket.socketpair()
        player_side.close()

        got_right_error = False
        try:
            net.receive_message(banker_side)
        except ConnectionResetError:
            got_right_error = True

        banker_side.close()
        self.assertTrue(got_right_error)

    def test_normal_message_still_works(self):
        """Normal messages should still be received correctly."""
        banker_side, player_side = socket.socketpair()

        net.send_message(player_side, "0mply,roll")
        message = net.receive_message(banker_side)

        banker_side.close()
        player_side.close()
        self.assertEqual(message, "0mply,roll")


if __name__ == "__main__":
    unittest.main()