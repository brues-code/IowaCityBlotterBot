import os
import time
from datetime import datetime, timedelta

LOG_DIRECTORY = "logs/"
CACHE_DIRECTORY = "cache/"
SETTINGS_FILE = "settings.txt"
IC_ROOT_URL = 'https://www.iowa-city.org/icgovapps/police/'
DATE_STAMP_HOUR_DELAY = 5


class Settings:
    def __init__(self):
        pass

    def get_dispatch_file_name(self) -> str:
        return "%s/%s.txt" % (CACHE_DIRECTORY, self.get_date_stamp())

    def fetch_old_dispatch_ids(self) -> list:
        return_ids = []
        dispatch_file_name = self.get_dispatch_file_name()
        try:
            if not os.path.exists(CACHE_DIRECTORY):
                os.makedirs(CACHE_DIRECTORY)
            f = open(dispatch_file_name, "r")
            if f.readable():
                text: str = f.read()
                if len(text) > 0:
                    return_ids = text.split(',')
            f.close()
        except:
            pass
        self.delete_old_dispatch_ids()
        return return_ids

    def save_dispatch_id(self, dispatch_id: str):
        f = open(self.get_dispatch_file_name(), "a")
        if f.writable():
            f.write("%s," % dispatch_id)
        f.close()

    def delete_old_dispatch_ids(self):
        current_time = time.time()
        for f in os.listdir(CACHE_DIRECTORY):
            file_name = "%s%s" % (CACHE_DIRECTORY, f)
            creation_time = os.path.getctime(file_name)
            if (current_time - creation_time) // (24 * 3600) >= 2:
                os.unlink(file_name)
                self.print_with_stamp('{} removed'.format(file_name))

    def get_settings(self):
        f = open(SETTINGS_FILE, "r")
        if f.readable():
            return eval(f.read())
        f.close()

    def get_list_url(self, date: str) -> str:
        return "%sactivitylog?activityDate=%s" % (IC_ROOT_URL, date)

    def get_dispatch_url(self, dispatch_id: str) -> str:
        return "%sdetails?dispatchNumber=%s" % (IC_ROOT_URL, dispatch_id)

    def print_with_stamp(self, input_str: str):
        st = datetime.now().strftime('%H:%M:%S')
        output_str = "[%s]: %s" % (st, input_str)
        self.add_to_log(output_str)
        print(output_str)

    def add_to_log(self, log_message: str):
        log_directory = "%s%s" %  (LOG_DIRECTORY, self.get_date_directory())
        if not os.path.exists(log_directory):
            os.makedirs(log_directory)
        f = open("%s%s.txt" % (log_directory, self.get_date_stamp()), "a")
        if f.writable():
            f.write(log_message + "\n")
        f.close()

    def get_date(self) -> datetime:
        return datetime.now() - timedelta(hours=DATE_STAMP_HOUR_DELAY)

    def get_date_stamp(self) -> str:
        return self.get_date().strftime('%m-%d-%Y')

    def get_date_directory(self) -> str:
        date = self.get_date()
        month = date.month
        if month < 10:
            month = "0%s" % month
        return '%s/%s/' % (date.year, month)
