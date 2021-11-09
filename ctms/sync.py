import logging
from datetime import datetime, timezone
from typing import List

from ctms.acoustic_service import Acoustic, CTMSToAcousticService
from ctms.background_metrics import BackgroundMetricService
from ctms.crud import (
    delete_acoustic_record,
    get_acoustic_record_as_contact,
    get_all_acoustic_records_before,
    get_all_acoustic_records_count,
    get_all_acoustic_retries_count,
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
        acoustic_product_table_id,
        server_number,
        retry_limit=5,
        batch_limit=20,
        is_acoustic_enabled=True,
        metric_service: BackgroundMetricService = None,
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
            acoustic_product_table_id=acoustic_product_table_id,
            metric_service=metric_service,
        )
        self.logger = logging.getLogger(__name__)
        self.retry_limit = retry_limit
        self.batch_limit = batch_limit
        self.is_acoustic_enabled = is_acoustic_enabled
        self.metric_service = metric_service

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
        try:
            if self.is_acoustic_enabled:
                contact: ContactSchema = get_acoustic_record_as_contact(
                    db, pending_record
                )
                is_success = self.sync_contact_with_acoustic(contact)
            else:
                self.logger.debug(
                    "Acoustic is not currently enabled. Records will be classified as successful and "
                    "dropped from queue at this time."
                )
                is_success = True

            if is_success:
                # on success delete pending_record from table
                delete_acoustic_record(db, pending_record)
                self.logger.debug(
                    "Successfully sync'd contact; deleting pending_record in table."
                )
                if self.metric_service:
                    self.metric_service.inc_acoustic_sync_total()
            else:
                # on failure increment retry of record in table
                retry_acoustic_record(db, pending_record)
                self.logger.debug(
                    "Failure on sync; incrementing retry for pending_record in table."
                )
        except Exception:  # pylint: disable=W0703
            self.logger.exception("Exception occurred when processing acoustic record.")

    def sync_records(self, db, end_time=None):
        if end_time is None:
            end_time = datetime.now(timezone.utc)
        self.logger.debug("START: sync.sync_records")
        if self.metric_service:
            all_acoustic_records_count: int = get_all_acoustic_records_count(
                db=db, end_time=end_time, retry_limit=self.retry_limit
            )
            self.metric_service.gauge_acoustic_sync_backlog(all_acoustic_records_count)
            all_retry_records_count: int = get_all_acoustic_retries_count(db=db)
            self.metric_service.gauge_acoustic_retry_backlog(all_retry_records_count)
        # Get all Records before current time
        all_acoustic_records_before_now: List[
            PendingAcousticRecord
        ] = get_all_acoustic_records_before(
            db,
            end_time=end_time,
            retry_limit=self.retry_limit,
            batch_limit=self.batch_limit,
        )

        # For each record, attempt downstream sync
        for acoustic_record in all_acoustic_records_before_now:
            self._sync_pending_record(db, acoustic_record)
        # Commit changes to db after ALL records are batch-processed
        db.commit()
        self.logger.debug("END: sync.sync_records")
