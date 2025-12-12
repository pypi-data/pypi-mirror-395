class BaseResourceObserver:
    """base class of the resource observer"""

    def release_resource(self, resource):
        raise NotImplementedError("Base class")


class _DummyResourceManager:
    """
    Simple resource manager. It holds a set of observer tha must release a resource when requested
    Observers must implement the 'BaseResourceObserver'
    """

    def __init__(self):
        self._observers = set()

    def register(self, observer):
        """Register a process to be notified when the resource should be released."""
        if observer not in self._observers:
            self._observers.add(observer)

    def unregister(self, observer):
        """Unregister a process so it won't be notified anymore."""
        if observer in self._observers:
            self._observers.remove(observer)

    def release_resource(self, resource: str):
        """Force all observer to release the given resource"""
        for observer in self._observers:
            observer.release_resource(resource)


HDF5VolumeManager = _DummyResourceManager()
