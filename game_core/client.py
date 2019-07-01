from game_core.progress import Progress


class Client:
    """
    The class stores all the needed info about the client.

    """
    last_created_session_id = 0

    def __init__(self, client_id):
        # TODO: phone_number and other public info about user
        self.progress = Progress.are_you_ready_w
        self.client_id = client_id
        self.session_id = Client.last_created_session_id
        self.first_name = ""
        self.last_name = ""
        self.profile_pic = ""
        self.information_filled = False
        Client.last_created_session_id += 1

    def fill_public_info(self, name, last_name, profile_pic):
        self.first_name = name
        self.last_name = last_name
        self.profile_pic = profile_pic
        self.information_filled = True

    def update_progress(self, p):
        self.progress = p
