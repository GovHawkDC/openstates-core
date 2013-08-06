from .. import Check
from .common import common_checks


def check(db):
    for meta in db.metadata.find():
        for check in common_checks(meta, 'metadata', 'metadata'):
            yield check

        blacklist = [
            "latest_json_url",
            "latest_json_date",
            "latest_csv_url",
            "latest_csv_date",
        ]

        for entry in blacklist:
            if entry in meta:
                yield Check(collection='metadata',
                            id=meta['_id'],
                            tagname='meta-has-%s' % (entry),
                            severity='important')