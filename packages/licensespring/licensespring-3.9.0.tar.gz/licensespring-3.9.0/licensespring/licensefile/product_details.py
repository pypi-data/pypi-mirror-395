from datetime import datetime


class ProductDetailsManager:
    def __init__(
        self,
        product_id: int = None,
        product_name: str = None,
        short_code: str = None,
        allow_trial: bool = None,
        trial_days: int = None,
        authorization_method: str = None,
        allow_overages: bool = None,
        max_overages: int = None,
        prevent_vm: bool = None,
        floating_timeout: int = None,
        metadata: dict = None,
    ) -> None:
        self.product_id = product_id
        self.product_name = product_name
        self.short_code = short_code
        self.allow_trial = allow_trial
        self.trial_days = trial_days
        self.authorization_method = authorization_method
        self.allow_overages = allow_overages
        self.max_overages = max_overages
        self.prevent_vm = prevent_vm
        self.floating_timeout = floating_timeout
        self.metadata = metadata

    def json_to_attribute(self, product_details: dict) -> None:
        for key, value in product_details.items():
            if key in self.__dict__:
                setattr(self, key, value)
