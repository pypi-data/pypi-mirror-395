import requests

from licensespring.licensefile import License
from licensespring.licensefile.base_manager import BaseManager
from licensespring.licensefile.config import Configuration


class FloatingManager(BaseManager):
    def __init__(self, conf: Configuration) -> None:
        super().__init__(conf=conf)

    def auth(self, username: str, password: str) -> dict:
        """
        Authenitcate

        Args:
            username (str): username
            password (str): password

        Returns:
            dict: response
        """
        return self.api_client.floating_client.auth(
            username=username, password=password
        )

    def register(
        self,
        os_hostname: str = None,
        ip_local: str = None,
        user_info: str = None,
        license_id: int = None,
    ) -> License:
        """
        Register License

        Args:
            os_hostname (str, optional): os hostname. Defaults to None.
            ip_local (str, optional): ip local. Defaults to None.
            user_info (str, optional): user info. Defaults to None.
            license_id (int, optional):license id. Defaults to None.

        Returns:
            License: license
        """

        response = self.api_client.floating_client.register_user(
            product=self._conf._product,
            license_id=license_id,
            os_hostname=os_hostname,
            ip_local=ip_local,
            user_info=user_info,
        )

        if self.api_client.floating_client.is_floating_server_v2():
            self.licensefile_handler._cache.update_cache(
                "floating_server_register_v2", response
            )

        else:
            self.licensefile_handler._cache.update_cache(
                "floating_server_register", response
            )
        self.licensefile_handler._cache.update_floating_period(
            getattr(self.licensefile_handler._cache, "borrowed_until", None)
        )
        self.licensefile_handler.save_licensefile(self.licensefile_handler._cache)

        return License(
            self._conf._product,
            api_client=self.api_client,
            licensefile_handler=self.licensefile_handler,
        )

    def unregister(self, license_id: int = None) -> str:
        """
        Unregister license

        Args:
            license_id (int, optional): license id. Defaults to None.

        Returns:
            str: license unregistered
        """
        return self.api_client.floating_client.unregister_user(
            product=self._conf._product, license_id=license_id
        )

    def unregister_all(self) -> str:
        """
        Unregister all

        Returns:
            str: ""
        """
        return self.api_client.floating_client.unregister_all()

    def borrow(
        self,
        borrowed_until: str,
        os_hostname: str = None,
        ip_local: str = None,
        user_info: str = None,
        license_id: int = None,
    ) -> License:
        """
        borrow license

        Args:
            borrowed_until (str): borrow until date
            os_hostname (str, optional): os hostname. Defaults to None.
            ip_local (str, optional): ip local. Defaults to None.
            user_info (str, optional): user info. Defaults to None.
            license_id (int, optional):license id. Defaults to None.

        Returns:
            License: license
        """
        response = self.api_client.floating_client.register_user(
            product=self._conf._product,
            license_id=license_id,
            os_hostname=os_hostname,
            ip_local=ip_local,
            user_info=user_info,
        )
        self.licensefile_handler._cache.update_cache(
            "floating_server_register", response
        )
        self.licensefile_handler.save_licensefile(self.licensefile_handler._cache)

        license = License(
            self._conf._product,
            api_client=self.api_client,
            licensefile_handler=self.licensefile_handler,
        )

        license.floating_borrow(borrow_until=borrowed_until)

        return license

    def is_online(self, throw_e=False) -> bool:
        """
        Checks if floating server is online

        Args:
            throw_e (bool, optional): True if you want raise exception. Defaults to False.

        Raises:
            ex: Exception

        Returns:
            bool: True if server is online, otherwise False
        """
        try:
            response = requests.get(
                f"{self.api_client.api_protocol}://{self.api_client.api_domain}"
            )

            if response.status_code == 200:
                return True

        except Exception as ex:
            if throw_e:
                raise ex

        return False

    def fetch_licenses(self, product: str = None):
        return self.api_client.floating_client.fetch_licenses(product=product)
