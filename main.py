"""Main run"""
from chainbrain import Dataset
from chainbrain.core.configs.note_context import NoteContext
from chainbrain.utils.data_service import DataService, Table
from .logger import get_logger
from .config import get_settings
from .utils.appservice import AppService

logger = get_logger()
settings = get_settings()
NoteContext.source = "studio"

source_scenario_id = settings.source_scenario_id #pylint: disable=invalid-name
target_scenario_id = settings.target_scenario_id #pylint: disable=invalid-name

logger.debug(
    "Triggering the copy scenario from source: %s, to target: %s",
    source_scenario_id,
    target_scenario_id
)
try:
    tables = DataService(service_url=settings.data_service_url).list(
        scenario_id=source_scenario_id
    )
    for table in tables:
        _table = Table(**table)
        sdf = Dataset(_table.name).read(
            data_type="spark",
            path=_table.storage.storage_location,
            scenario_id=source_scenario_id,
            file_type="parquet",
            force=True,
        )
        Dataset(_table.name).write(
            sdf,
            table_type=_table.table_type,
            scenario_id=target_scenario_id,
            sequence_note_id=_table.created_by.sequence_note_id,
            service_url=settings.data_service_url,
        )

        logger.debug(
            "Copied table %s from scenario %s to %s",
            _table.id,
            source_scenario_id,
            target_scenario_id,
        )
    AppService().update_scenario(
        scenario_id=target_scenario_id, status="active"
    )
except Exception as exc: # pylint: disable=broad-except
    logger.error("Error while copying scenario: %s", exc)
    AppService().update_scenario(
        scenario_id=target_scenario_id, status="copyFailed"
    )
logger.debug(
    "Completed the copy scenario from source: %s, to target: %s",
    source_scenario_id,
    target_scenario_id
)
