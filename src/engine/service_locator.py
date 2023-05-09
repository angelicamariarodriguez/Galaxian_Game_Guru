from src.engine.services.images_service import ImagesService
from src.engine.services.fonts_service import FontsService

class ServiceLocator:
    images_services = ImagesService()
    fonts_service = FontsService()
    