from complycube.model.complycubeobject import ComplyCubeObject

class LivePhoto(ComplyCubeObject):
    """[Live Photos are images of the client's face. Typically, along with an ID document, they are used to perform Identity Checks.
            Upon creating a Live Photo, the following inspections are conducted:
                Faces Analysis: checks if a face is detected, and that the number of faces does not exceed 1.
                Facial Obstructions: checks if facial features are covered or not visible.
                Facial Orientation: checks if face is at an optimal position.
                Glare Detection: checks if an face has glare.
                Liveness Check: checks if a photo is genuine and is not a spoofed photo of an image, or photo of a photo.]

    Attributes:
        id (str): [The unique identifier for an address.]
        client_id (str): [The ID of the client associated with this live photo.]
        download_link (str): [The URI which can be used to download the live photo. This will be automatically generated upon a successful live photo upload.]
        content_type (str): [The MIME type of the image. This will be automatically set upon a successful live photo upload.]
        size (int): [The size of the live photo in bytes. This will be automatically set upon a successful live photo upload.]
        created_at (str): [The date and time when the live photo was created.]
        updated_at (str): [The date and time when the live photo was updated.]
    """
    def __init__(self, *args, **kwargs):
        self.id = None
        self.client_id = None
        self.download_link = None
        self.content_type = None
        self.size = None
        super(LivePhoto, self).__init__(*args,**kwargs)