#!/usr/bin/python
import topy
import uuid
from datetime import date, timedelta
from config import logging_in_day_one_for_yesterday, day_one_dir_path, day_one_entry_title, day_one_extension


def log_to_day_one(tlist):
    uid = str(uuid.uuid1()).replace('-', '').upper()
    log_date = date.today()
    if logging_in_day_one_for_yesterday:
        log_date -= timedelta(days=1)
    log_data_str = log_date.isoformat()
    print log_data_str

    filtered = tlist.filter('@done = ' + log_data_str)
    filtered.remove_tag('done')
    entry_text = day_one_entry_title + \
        filtered.as_markdown(emphasise_done=False)

    full_text = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Creation Date</key>
    <date>{date}</date>
    <key>Entry Text</key>
    <string>{entry_text}</string>
    <key>Starred</key>
    <false/>
    <key>UUID</key>
    <string>{uid}</string>
</dict>
</plist>
""".format(
    uid=uid,
    entry_text=entry_text,
    date=log_date.strftime('%Y-%m-%dT23:59:59Z')
)
    with open(day_one_dir_path + uid + day_one_extension, 'w') as f:
        f.write(full_text)

if __name__ == '__main__':
    log_to_day_one(topy.from_files(topy.lists.to_list()))
