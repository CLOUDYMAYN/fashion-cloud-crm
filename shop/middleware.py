import logging
import time

from django.core.cache import cache
from django.http import JsonResponse
from django.utils.deprecation import MiddlewareMixin

logger = logging.getLogger(__name__)


class RequestLoggingMiddleware(MiddlewareMixin):
    """Middleware для логирования запросов"""

    def process_request(self, request):
        request.start_time = time.time()

    def process_response(self, request, response):
        if hasattr(request, "start_time"):
            duration = time.time() - request.start_time

            # Логируем медленные запросы (> 1 секунды)
            if duration > 1.0:
                logger.warning(
                    f"Slow request: {request.method} {request.path} " f"took {duration:.2f}s"
                )

        return response


class RateLimitMiddleware(MiddlewareMixin):
    """Простое rate limiting middleware"""

    def process_request(self, request):
        # Применяем rate limiting только к API endpoints
        if request.path.startswith("/api/"):
            client_ip = self.get_client_ip(request)
            cache_key = f"rate_limit_{client_ip}"

            # Получаем количество запросов за последнюю минуту
            requests_count = cache.get(cache_key, 0)

            if requests_count >= 100:  # Максимум 100 запросов в минуту
                return JsonResponse(
                    {
                        "error": "Rate limit exceeded",
                        "message": "Too many requests. Please try again later.",
                    },
                    status=429,
                )

            # Увеличиваем счетчик
            cache.set(cache_key, requests_count + 1, 60)

        return None

    def get_client_ip(self, request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")
        return ip
