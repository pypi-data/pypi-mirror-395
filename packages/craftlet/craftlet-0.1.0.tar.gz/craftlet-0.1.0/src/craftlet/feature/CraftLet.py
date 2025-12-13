from pathlib import Path
from craftlet.utils.mappers import repoUrlToZipUrl
import httpx
from zipfile import ZipFile
from io import BytesIO
import json
from craftlet.utils.helperFunctions import CLIFunctions


class CraftLet:
    @staticmethod
    async def downloadTemplateGithub(repoUrl: str, targetDir: Path):
        zipUrl = repoUrlToZipUrl(repoUrl=repoUrl)

        async with httpx.AsyncClient() as client:
            response = await client.get(zipUrl)
            response.raise_for_status()
            zipBytes = response.content

        CraftLet.diskWrite(inputBytes=zipBytes, targetDestination=targetDir)

    @staticmethod
    def diskWrite(inputBytes: bytes, targetDestination: Path):
        with ZipFile(BytesIO(inputBytes)) as z:
            root = z.namelist()[0].split("/")[0]
            templateConfig = CraftLet.loadTemplateConfigFile(
                zipFileInstance=z, root=root
            )
            personalTemplateConfig = CLIFunctions.buildConfigFromDict(
                dictFile=templateConfig
            )

            for name in z.namelist():
                if name.endswith("/") or name.endswith("templateConfig.json"):
                    continue
                relativePath = Path(name).relative_to(root)
                dest = targetDestination / relativePath
                dest.parent.mkdir(parents=True, exist_ok=True)

                rawText = z.read(name).decode()
                dest.write_text(rawText)

    @staticmethod
    def loadTemplateConfigFile(zipFileInstance: ZipFile, root: str):
        try:
            raw = zipFileInstance.read(f"{root}/templateConfig.json").decode()
            return json.loads(raw)
        except KeyError:
            return {}
