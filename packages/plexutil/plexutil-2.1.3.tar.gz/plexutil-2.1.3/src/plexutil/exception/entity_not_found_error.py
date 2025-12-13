from peewee import Model


class EntityNotFoundError(Exception):
    def __init__(self, instance: Model) -> None:
        if not isinstance(instance, Model):
            description = "cls must be a subclass of Exception"
            raise TypeError(description)

        self.instance = instance

        self.message = (
            f"{self.instance}: Not Found\nProperties: {self.instance.__dict__}"
        )

        super().__init__(self.message)
