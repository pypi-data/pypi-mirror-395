from datetime import datetime


class VariablesManager:
    def __init__(self) -> None:
        pass

    def json_to_attribute(self, device_vars: list) -> None:
        for var in device_vars:
            if var["created_at"].endswith("Z"):
                var["created_at"] = var["created_at"][:-1]

            setattr(
                self,
                var["variable"],
                DeviceVariable(
                    id=var.get("id", None),
                    created_at=datetime.fromisoformat(var["created_at"]).replace(
                        tzinfo=None
                    ),
                    variable=var.get("variable", None),
                    value=var.get("value", None),
                    device_id=var.get("device_id", None),
                    update=False,
                ),
            )

    def set_variables(self, variables: dict):
        """
        Sets device variables in cache

        Args:
            variables (dict): device variables
        """
        for variable in variables.keys():
            setattr(
                self,
                variable,
                DeviceVariable(
                    id=None,
                    created_at=None,
                    variable=variable,
                    value=variables[variable],
                    device_id=None,
                    update=True,
                ),
            )

    def attributes_to_list(self) -> list:
        """
        Generates list of device variables

        Returns:
            list: device variables
        """
        device_varaibles_list = []

        for _, device_var in self.__dict__.items():
            data = {}

            for key, value in device_var.__dict__.items():
                if key != "update":
                    if isinstance(value, datetime):
                        data[key] = value.isoformat()

                    else:
                        data[key] = value

            device_varaibles_list.append(data)

        return device_varaibles_list

    def get_device_variable(self, variable_name: str) -> dict:
        """
        Get device variable

        Args:
            variable_name (str): device variable name

        Returns:
            dict: device variable
        """
        if hasattr(self, variable_name):
            obj = getattr(self, variable_name)

            return obj.__dict__

    def get_device_variable_for_send(self) -> dict:
        """
        Finds new device variables which should be sent on LicenseSpring server

        Returns:
            dict: Dictionary of device variables
        """
        new_device_variables = {}

        for _, device_var in self.__dict__.items():
            if device_var.update:
                new_device_variables[device_var.variable] = device_var.value
                device_var.update = False

        return new_device_variables


class DeviceVariable:
    def __init__(
        self,
        id: int,
        created_at: str,
        variable: str,
        value: str,
        device_id: int,
        update: bool,
    ) -> None:
        self.id = id
        self.created_at = created_at
        self.variable = variable
        self.value = value
        self.device_id = device_id
        self.update = update
