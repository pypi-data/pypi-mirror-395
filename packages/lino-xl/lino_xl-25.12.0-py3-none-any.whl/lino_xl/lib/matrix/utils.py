# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import datetime as dt
import json
from requests import Session
from uuid import uuid4
from lino.api import rt, dd

matrix_server = "https://matrix.org"
ses = Session()


def refresh_matrix_creds():
    now = dt.datetime.now().astimezone()

    if getattr(ses, "expires_at", None) is None:
        resp = ses.post(f"{matrix_server}/_matrix/client/v3/login", json={
            "identifier": {
                "type": "m.id.user",
                "user": dd.plugins.matrix.user_id[1:].split(":")[0]},
            "password": dd.plugins.matrix.user_password,
            "type": "m.login.password",
            "refresh_token": True,
            "device_id": getattr(ses, 'device_id', None),
        })
        if resp.status_code != 200:
            dd.logger.error(str(resp.json()))
        resp.raise_for_status()

        json_resp = resp.json()
        ses.headers.update({"Authorization": f"Bearer {json_resp['access_token']}"})
        ses.refresh_token = json_resp['refresh_token']
        ses.device_id = json_resp['device_id']
        ses.expires_at = (now + dt.timedelta(
            milliseconds=int(json_resp['expires_in_ms'])
        ) - dt.timedelta(minutes=5))

    elif ses.expires_at < now:
        resp = ses.post(f"{matrix_server}/_matrix/client/v3/refresh", json={
            "refresh_token": ses.refresh_token})
        if resp.status_code != 200:
            dd.logger.error(str(resp.json()))
        resp.raise_for_status()

        json_resp = resp.json()
        ses.headers.update({"Authorization": f"Bearer {json_resp['access_token']}"})
        ses.refresh_token = json_resp['refresh_token']
        ses.expires_at = (now + dt.timedelta(
            milliseconds=int(json_resp['expires_in_ms'])
        ) - dt.timedelta(minutes=5))


def send_notification_to_matrix_room(msg, room_id=None):
    if dd.plugins.matrix.user_id is None:
        return

    if room_id is None:
        room_id = dd.plugins.matrix.broadcast_room_id

    refresh_matrix_creds()
    resp = ses.put(f"{matrix_server}/_matrix/client/v3/rooms/"
                   f"{room_id}/send/m.room.message/{uuid4()}",
                   data=json.dumps({"body": msg, "msgtype": "m.text"}))
    if resp.status_code != 200:
        dd.logger.error(str(resp.json()))
    resp.raise_for_status()


def send_notification_direct(msg, user):
    if dd.plugins.matrix.user_id is None:
        return

    try:
        ut = user.matrix
    except rt.models.matrix.UserTrait.DoesNotExist:
        return

    if not ut.direct_room:
        if not ut.matrix_user_id:
            return
        refresh_matrix_creds()

        # resp = ses.get(f"{matrix_server}/_matrix/client/v3/joined_rooms")
        # if resp.status_code != 200:
        #     dd.logger.error(str(resp.json()))
        # resp.raise_for_status()
        # for room_id in resp.json()["joined_rooms"]:
        #     pass

        resp = ses.post(f"{matrix_server}/_matrix/client/v3/createRoom",
                        data=json.dumps({
                            "invite": [ut.matrix_user_id], "is_direct": True,
                            "preset": "trusted_private_chat"
                        }))
        if resp.status_code != 200:
            dd.logger.error(str(resp.json()))
        resp.raise_for_status()

        json_resp = resp.json()
        ut.direct_room = json_resp["room_id"]
        ut.full_clean()
        ut.save()

    send_notification_to_matrix_room(msg, ut.direct_room)
