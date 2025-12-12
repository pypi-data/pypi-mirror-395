# -*- coding: UTF-8 -*-
# Copyright 2011-2024 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

import re
from pathlib import Path
import mailbox
import email.errors
import mimetypes
from email.utils import getaddresses, parsedate_to_datetime
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.utils.html import mark_safe, format_html
from django.utils.translation import ngettext
from django.utils.module_loading import import_string
from django.conf import settings

from lino.api import dd, rt, _
from lino.utils import DATE_TO_DIR_TPL
from lino.modlib.linod.choicelists import schedule_often

allowed_chars = "_-+."


def sanitize(filename):
    # Quite similar to lino.modlib.uploads.mixins.safe_filename()  (TODO: unite
    # them.)
    filename = filename.replace(" ", "_")
    filename = "".join(c for c in filename if c.isalpha()
                       or c.isdigit() or c in allowed_chars).strip()
    return filename


upload_area = dd.get_plugin_setting('inbox', 'upload_area', None)

# We search for a pattern #nnnn[:abc] where #nnnn is assumed to be a ticket
# number (more prcisely plugins.memo.parser.suggesters)

# TOPIC_PATTERN = re.compile(r"#(\w+)")


def process_message(ar, key, msg):
    user = None
    for real_name, email in getaddresses(msg.get_all("from", [])):
        try:
            user = rt.models.users.User.objects.get(email=email)
            ar.logger.info("[%s] Process message from user %s", key, user)
            break
        except ObjectDoesNotExist as e:
            pass
    if user is None:
        ar.logger.info("[%s] Ignore unknown sender %s", key, msg.get("from"))
        return
    date = parsedate_to_datetime(msg.get("date"))
    comment_kwargs = dict(user=user, created=date)

    to_parts = msg.get("to").split("@")
    if len(to_parts) != 2:
        ar.logger.info("[%s] Invalid header To: %s", key, msg.get("to"))
        return
    sub_parts = to_parts[0].split(dd.plugins.inbox.subaddress_separator)
    Comment = rt.models.comments.Comment
    if len(sub_parts) == 1:
        pass
    elif len(sub_parts) == 2:
        to, reply_to = sub_parts
        # print("20240902", sub_parts)
        if not reply_to.isnumeric():
            ar.logger.info("[%s] Invalid reply_to %s", key, reply_to)
            # return
        else:
            try:
                comment_kwargs.update(
                    reply_to=Comment.objects.get(pk=reply_to))
            except Comment.DoesNotExist:
                ar.logger.info("[%s] Invalid reply_to %s", key, reply_to)
                # return
    elif len(sub_parts) == 3:
        # print("20240902", sub_parts)
        to, ct, pk = sub_parts  # content type, primary key
        try:
            ct = rt.models.contenttypes.ContentType.objects.get_for_id(ct)
            owner = ct.model_class().objects.get(pk=pk)
            comment_kwargs.update(owner=owner)
        except ObjectDoesNotExist as e:
            ar.logger.info("[%s] Invalid ct or pk in %s", key, msg.get("to"))
            # return
    else:
        ar.logger.info("[%s] Invalid header To: %s", key, msg.get("to"))
        # return

    # m = re.search(TOPIC_PATTERN, subject)
    # if m is not None:
    #     getter = dd.plugins.memo.parser.suggesters['#'].getter
    #     topic = getter(m.groups(1))
    #     logger.info("[%s] Found topic %s in subject %s", key, topic, subject)
    # else:
    #     logger.info("[%s] No topic in subject %s", key, subject)

    upload_volume = dd.plugins.inbox.get_upload_volume()
    if upload_volume is not None:
        inbox_root = Path(upload_volume.root_dir)
        upload_dir = Path(date.strftime(DATE_TO_DIR_TPL)) / key

    subject = msg.get("subject")
    counter = 0
    text_body = None
    html_body = None
    uploaded_files = []
    for part in msg.walk():
        if part.get_content_maintype() == 'multipart':
            # multipart/* are just containers
            continue
        filename = part.get_filename()
        if filename:
            if upload_area is None or upload_volume is None:
                ar.logger.info(
                    "[%s] Ignore attached %s because upload area is none.", key, filename)
                continue
            counter += 1
            upload_options = dict(user=user)
            # if counter == 1:
            #     upload_options.update(description=subject)
            upload_options.update(upload_area=upload_area)
            # filename = key + "." + filename
            filename = sanitize(filename)
            filename = upload_dir / filename
            upload_options.update(library_file=filename, volume=upload_volume)
            # if filename.exists():
            #     logger.warning("Overwriting existing %s", filename)
            filename = inbox_root / filename
            ar.logger.info("Write file %s.", filename)
            filename.parent.mkdir(parents=True, exist_ok=True)
            payload = part.get_payload(decode=True)
            with open(filename, 'wb') as fp:
                fp.write(payload)

            # sar = rt.models.uploads.Uploads.request(parent=ar, user=user)
            # obj = sar.create_instance(**upload_options)
            obj = rt.models.uploads.Upload(**upload_options)
            obj.full_clean()
            # obj.save_new_instance(sar)  # generate comment "Uploaded a picture"
            obj.save()
            errors = list(rt.models.uploads.previewer.check_preview(obj))
            if len(errors):
                raise Exception(f"Oops: {errors}")
            uploaded_files.append(obj)
        else:
            ct = part.get_content_type()
            # logger.info("[%s] %s part without filename", key, ct)
            if ct == "text/html":
                if html_body is None:
                    html_body = part.get_payload()
                else:
                    ar.logger.warning(
                        "Multiple %s parts without filename!", ct)
            elif ct == "text/plain":
                if text_body is None:
                    text_body = part.get_payload()
                else:
                    ar.logger.warning(
                        "Multiple %s parts without filename!", ct)
            else:
                ar.logger.warning("Ignored %s part without filename!", ct)
        #     ext = mimetypes.guess_extension(part.get_content_type())
        #     if ext:
        #         filename = f'{key}-{counter:03d}{ext}'
    if html_body is None:
        body = text_body
    else:
        body = html_body

    if (n := len(uploaded_files)) > 0:
        msg = format_html(
            "{}: {}.",
            ngettext("Uploaded {} file", "Uploaded {} files", n).format(n),
            ", ".join([f"[upload {u.id} {u}]" for u in uploaded_files])
            # mark_safe(", ".join([ar.obj2htmls(u) for u in uploaded_files]))
        )
        if body is None:
            body = msg
        else:
            body = msg + "\n\n" + body

    if not body:
        ar.logger.warning("[%s] No comment because body is empty", key)
        return

    comment_kwargs.update(body=body)
    obj = rt.models.comments.Comment(**comment_kwargs)
    obj.full_clean()
    obj.before_ui_save(ar, None)  # bleach
    obj.save()
    # print("20241113", obj.body_full_preview)


def process_inbox(ar, discard=False):

    if (pth := dd.plugins.inbox.mailbox_path) is None:
        return
    ar.logger.info("Process inbox %s (discard is %s) ...", pth, discard)
    mailbox_type = import_string(dd.plugins.inbox.mailbox_type)
    inbox = mailbox_type(pth)
    try:
        inbox.lock()
    except mailbox.ExternalClashError as e:
        return
    for key, msg in inbox.iteritems():
        process_message(ar, key, msg)
        if discard:
            ar.logger.debug("Discard %s ...", key)
            inbox.discard(key)
            inbox.flush()
    inbox.unlock()
    ar.logger.debug("Done processing inbox %s", pth)


@schedule_often(300)
def read_inbox(ar):
    process_inbox(ar, discard=dd.plugins.inbox.discard_processed_message)
