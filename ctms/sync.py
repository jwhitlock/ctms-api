import logging
from datetime import datetime, timezone
from typing import List

from ctms.acoustic_service import Acoustic, CTMSToAcousticService
from ctms.crud import (
    delete_acoustic_record,
    get_acoustic_record_as_contact,
    get_all_acoustic_records_before,
    retry_acoustic_record,
)
from ctms.models import PendingAcousticRecord
from ctms.schemas import ContactSchema


class CTMSToAcousticSync:
    def __init__(
        self,
        client_id,
        client_secret,
        refresh_token,
        acoustic_main_table_id,
        acoustic_newsletter_table_id,
        server_number,
    ):
        acoustic_client = Acoustic(
            client_id=client_id,
            client_secret=client_secret,
            refresh_token=refresh_token,
            server_number=server_number,
        )
        self.ctms_to_acoustic = CTMSToAcousticService(
            acoustic_client=acoustic_client,
            acoustic_main_table_id=acoustic_main_table_id,
            acoustic_newsletter_table_id=acoustic_newsletter_table_id,
        )
        self.logger = logging.getLogger(__name__)

    def sync_contact_with_acoustic(self, contact: ContactSchema):
        """

        :param contact:
        :return: Boolean value indicating success:True or failure:False
        """
        try:
            # Convert ContactSchema to Acoustic Readable, attempt API call
            return self.ctms_to_acoustic.attempt_to_upload_ctms_contact(contact)
        except Exception:  # pylint: disable=W0703
            self.logger.exception("Error executing sync.sync_contact_with_acoustic")
            return False

    def _sync_pending_record(self, db, pending_record: PendingAcousticRecord):
        contact: ContactSchema = get_acoustic_record_as_contact(db, pending_record)
        is_success = self.sync_contact_with_acoustic(contact)

        if is_success:
            # on success delete pending_record from table
            delete_acoustic_record(db, pending_record)
            self.logger.debug(
                "Successfully sync'd contact; deleting pending_record in table."
            )
        else:
            # on failure increment retry of record in table
            retry_acoustic_record(db, pending_record)
            self.logger.debug(
                "Failure on sync; incrementing retry for pending_record in table."
            )

    def sync_records(self, db, end_time=datetime.now(timezone.utc)):
        self.logger.debug("START: sync.sync_records")
        # Get all Records before current time
        all_acoustic_records_before_now: List[
            PendingAcousticRecord
        ] = get_all_acoustic_records_before(db, end_time=end_time)

        # For each record, attempt downstream sync
        for acoustic_record in all_acoustic_records_before_now:
            self._sync_pending_record(db, acoustic_record)
        # Commit changes to db after all records are processed
        db.commit()
        self.logger.debug("END: sync.sync_records")
