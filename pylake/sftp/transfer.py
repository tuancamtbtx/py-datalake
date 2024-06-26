from pylake.logger.logger_mixing import LoggerMixing

class SFTPTransfer(LoggerMixing):
    def __init__(self, host, username, password, port=22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port
    
    def upload(self, local_path, remote_path):
        """
        Uploads a file from a local directory to a remote server using SFTP.

        Parameters:
        local_path (str): The path to the file on the local machine.
        remote_path (str): The path where the file will be saved on the remote server.
        """
        import pysftp
        with pysftp.Connection(self.host, username=self.username, password=self.password, port=self.port) as sftp:
            sftp.put(local_path, remote_path)
            self.logger.info("Uploaded file from {} to {}".format(local_path, remote_path))
    
    def download(self, remote_path, local_path):
        """
        Downloads a file from a remote server to a local directory using SFTP.

        Parameters:
        remote_path (str): The path to the file on the remote server.
        local_path (str): The path where the file will be saved locally.
        """
        import pysftp
        # Establish an SFTP connection using the provided host, username, password, and port
        with pysftp.Connection(self.host, username=self.username, password=self.password, port=self.port) as sftp:
            sftp.get(remote_path, local_path)
            self.logger.info("Downloaded file from {} to {}".format(remote_path, local_path))