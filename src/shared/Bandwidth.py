import speedtest


class Bandwidth:
    def __init__(self):
        pass

    def get_bandwidth_info(self):
        s = speedtest.Speedtest()
        s.download(), s.upload()
        res = s.results.dict()
        download, upload, ping = self.convert_to_mbs_format(res)
        return dict(download_speed=download, upload_speed=upload, ping=ping)

    @staticmethod
    def convert_to_mbs_format(results):
        return (results["download"]//1000000), (results["upload"]//1000000), (results["ping"])
