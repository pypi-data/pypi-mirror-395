"""
Clase para hacer exponential back of de algun callback
"""
import logging
import time
from abc import ABC, abstractmethod
import requests

logger = logging.getLogger(__name__)


class RequestActionManager(ABC):
    """Abstract base class for handling HTTP requests with decision logic"""

    @abstractmethod
    def on_execute(self) -> requests.Response:
        """Execute the HTTP request and return the response"""

    @abstractmethod
    def success_callback(self, response: requests.Response) -> None:
        """Handle successful response"""

    @abstractmethod
    def error_callback(self, response: requests.Response) -> None:
        """Handle error response"""

    @abstractmethod
    def is_request_successful(self, response: requests.Response) -> bool:
        """Determine if the request was successful"""


class RequestManager:
    """
        Maneja los request para poder hacer un exponential backoff
    """

    def __init__(self, manager: RequestActionManager, max_retries: int = 12):
        """

        :param manager:
        :param max_retries:
        """

        self.initial_delay = 80
        self.min_delay = 2.0
        self.backoff_factor = 1.5
        self.max_retries = max_retries
        self.manager = manager

        # State variables
        self.current_delay = self.initial_delay
        self.retry_count = 0
        self.running = False

    def reset_delay(self):
        """
        Re-inicia el delay
        :return:
        """
        self.current_delay = self.initial_delay
        self.retry_count = 0

    def increase_delay(self):
        """
        Aumenta el delay cada
        :return:
        """
        self.current_delay = self.initial_delay = max(self.initial_delay / self.backoff_factor, self.min_delay)
        self.retry_count += 1

    def update_backoff_factor(self, amount: float):
        """
        Update back of factor by given amount
        :param amount:
        :return:
        """
        self.backoff_factor = amount
        logger.warning("Backoff updated to {}".format(self.backoff_factor))

    def should_continue(self) -> bool:
        """
        Determina si debe seguir ejecutando la accion
        :return:
        """

        if not self.running:
            return False
        if self.max_retries is not None and self.retry_count >= self.max_retries:
            return False
        return True

    def stop(self):
        """
        Detiene la ejecusion fozosamente
        :return:
        """
        self.running = False
        logger.warning("Completed exp backoff: {}".format(str(id(self))))

    def start(self):
        """
        Inicia el proceso de llamada con backoof
        :return:
        """
        self.running = True
        logger.warning("Staring exp backoff: {}".format(str(id(self))))
        while self.should_continue():
            try:
                response = self.manager.on_execute()

                if self.manager.is_request_successful(response=response):
                    self.stop()
                    self.manager.success_callback(response=response)
                    self.reset_delay()
                else:
                    self.manager.error_callback(response=response)
                    self.increase_delay()

            except requests.exceptions.RequestException:
                self.increase_delay()
            except KeyboardInterrupt:
                self.stop()
            except Exception:
                self.increase_delay()
            if self.should_continue():
                logger.warning('Waiting {} request {}'.format(self.current_delay, str(id(self))))
                time.sleep(self.current_delay)
