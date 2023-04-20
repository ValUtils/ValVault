from threading import Lock


class SingletonMeta(type):
    """
    This is a thread-safe Singleton.
    """
    _instances = {}
    _lock: Lock = Lock()

    def destroy(cls):
        try:
            del cls._instances[cls]
        except KeyError:
            pass

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]
