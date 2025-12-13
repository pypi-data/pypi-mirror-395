import typer
from typing import Dict


class CLIFunctions:
    @staticmethod
    def buildConfigFromDict(dictFile: Dict):
        for key, value in dictFile.items():
            userInput = typer.prompt(value.get("prompt", key))
            value["input"] = userInput
        return dictFile
