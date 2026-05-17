from datetime import date, datetime
from supabase import Client
from src.config import Config
from src.back.db.exceptions import *
from src.session import Me

class Calendar:
    @staticmethod
    def _get_db() -> Client:
        return Config.DB

    @staticmethod
    def get(date_from: date, date_to: date) -> list[dict]:
        db = Calendar._get_db()

        res = (
            db.table('user_events')
            .select('*, events(*)')
            .eq('user_id', Me.require_user_id())
            .gte('date', date_from.isoformat())
            .lte('date', date_to.isoformat())
            .order('date')
            .execute()
        )

        return res.data

    @staticmethod
    def add_new(
        event_date: date,
        start: datetime,
        finish: datetime,
        description: str,
        tag: str | None = None,
        color: str | None = None,
    ) -> dict:
        db = Calendar._get_db()

        event_res = db.table('events').insert({
            'start': start.isoformat(),
            'finish': finish.isoformat(),
            'description': description,
            'tag': tag,
            'color': color,
        }).execute()

        event_id = event_res.data[0]['id']

        ue_res = db.table('user_events').insert({
            'date': event_date.isoformat(),
            'user_id': Me.require_user_id(),
            'event_id': event_id,
        }).execute()

        return ue_res.data[0]

    @staticmethod
    def delete(event_id: str) -> None:
        db = Calendar._get_db()

        db.table('user_events').delete().eq('event_id', event_id).execute()
        db.table('events').delete().eq('id', event_id).execute()
