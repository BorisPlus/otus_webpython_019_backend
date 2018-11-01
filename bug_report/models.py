import os
import sys

from sqlalchemy.schema import UniqueConstraint

kiosk_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if kiosk_path not in sys.path:
    sys.path.append(kiosk_path)

from bug_report.config import db


class BugReport(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    datetime = db.Column(db.DateTime, nullable=False)
    href = db.Column(db.Text, nullable=False)
    selected_text = db.Column(db.Text, nullable=False)
    user_text = db.Column(db.Text, nullable=False)
    honest = db.Column(db.Boolean, nullable=False)
    request_headers = db.Column(db.Text, nullable=True)
    request_args = db.Column(db.Text, nullable=True)
    request_json = db.Column(db.Text, nullable=True)
    __table_args__ = (
        UniqueConstraint(
            'datetime', 'href', 'selected_text', 'user_text', 'honest',
            name='bug_report__unique'
        ),
    )

    def __repr__(self):
        return '<%s %s>' % (self.__class__, self.id)

    def __str__(self):
        return '%s %s %s %s %s' % (self.datetime, self.href, self.selected_text, self.user_text, self.honest)


if __name__ == '__main__':
    pass
