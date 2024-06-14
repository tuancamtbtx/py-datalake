from pydata.logger.logger_mixing import LoggerMixing

class SFTPTransfer(LoggerMixing):
    def __init__(self, host, username, password, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
    
    def upload(self, local_path, remote_path):
        import pysftp
        with pysftp.Connection(self.host, username=self.username, password=self.password, port=self.port) as sftp:
            sftp.put(local_path, remote_path)
            self.logger.info("Uploaded file from {} to {}".format(local_path, remote_path))
    
    def download(self, remote_path, local_path):
        import pysftp
        with pysftp.Connection(self.host, username=self.username, password=self.password, port=self.port) as sftp:
            sftp.get(remote_path, local_path)
            self.logger.info("Downloaded file from {} to {}".format(remote_path, local_path))