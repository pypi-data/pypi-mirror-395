from .api import quantim

class mstar_data(quantim):
    def __init__(self, username, password, secretpool, env="pdn", api_url=None):
        super().__init__(username, password, secretpool, env, api_url)

    def load_token(self, file_path):
        """
        Load token file to s3.
        """
        # Validate filename:
        filename = file_path.split("/")[-1]
        if filename.split(".")[-1]!="txt":
            raise ValueError("Extension must be txt. Please check file.")

        resp = self.upload_with_presigned_url(file_path, "condor-sura", f"inputs/morningstar_api/token/token.txt")
        return resp
