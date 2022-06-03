class Material:
    name = ""
    download_url = ""
    upload_date = ""
    file_name = ""

    def __init__(self, name, download_url, upload_date, file_name=None):
        self.name = name
        self.download_url = download_url
        self.upload_date = upload_date
        self.file_name = file_name
        return
