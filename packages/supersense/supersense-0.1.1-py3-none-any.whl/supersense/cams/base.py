
class CameraBase:
    def read(self):
        """Return a frame (or frames) in OpenCV format. Must be implemented by subclass."""
        raise NotImplementedError

    def release(self):
        """Release the camera resources. Must be implemented by subclass."""
        raise NotImplementedError
