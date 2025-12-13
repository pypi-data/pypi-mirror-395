def repoUrlToZipUrl(repoUrl: str):
    zipUrl = (
        repoUrl.replace("github.com", "codeload.github.com") + "/zip/refs/heads/main"
    )
    return zipUrl
