

class Instruction:
    def __init__(self, name: str, description: str, instruction: str, version: int) -> None:
        self.name: str = self.__name_by_env(name)
        self.description: str = description
        self.instruction: str = instruction
        self.version: int = version

    @staticmethod
    def __name_by_env(name: str) -> str:
        from dotenv import load_dotenv
        load_dotenv()
        import os
        app_name = os.getenv("APP_NAME")
        env = os.getenv('ENV')
        if env == 'dev':
            return f"{app_name}:{name}:dev"
        return f"{name}:prod"
