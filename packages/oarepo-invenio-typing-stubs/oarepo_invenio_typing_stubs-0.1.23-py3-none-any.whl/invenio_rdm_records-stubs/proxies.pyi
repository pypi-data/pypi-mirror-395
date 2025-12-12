from __future__ import annotations

from .ext import InvenioRDMRecords
from .oaiserver.services.services import OAIPMHServerService
from .services import RDMRecordService
from .services.communities.service import RecordCommunitiesService
from .services.community_records.service import CommunityRecordsService

current_rdm_records: InvenioRDMRecords  # intentionally not using a LocalProxy[InvenioRDMRecords] here as mypy does not understand it
current_rdm_records_service: RDMRecordService  # intentionally not using a LocalProxy[RDMRecordService] here as mypy does not understand it
current_rdm_records_media_files_service: RDMRecordService  # intentionally not using a LocalProxy[RDMRecordService] here as mypy does not understand it
current_oaipmh_server_service: OAIPMHServerService  # intentionally not using a LocalProxy[OAIPMHServerService] here as mypy does not understand it
current_record_communities_service: RecordCommunitiesService  # intentionally not using a LocalProxy[RecordCommunitiesService] here as mypy does not understand it
current_community_records_service: CommunityRecordsService  # intentionally not using a LocalProxy[CommunityRecordsService] here as mypy does not understand it
