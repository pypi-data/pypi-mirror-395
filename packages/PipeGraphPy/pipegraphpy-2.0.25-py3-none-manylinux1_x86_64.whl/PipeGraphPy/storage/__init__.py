# from . import redis_backend
from . import file_backend
from PipeGraphPy.config import settings

storage_backend = {
    # 'redis': redis_backend,
    'file': file_backend
}

store = storage_backend.get(settings.STORAGE_ENGINE)
