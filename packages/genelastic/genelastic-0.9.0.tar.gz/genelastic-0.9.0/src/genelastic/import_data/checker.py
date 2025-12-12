import logging

from genelastic.common.elastic import ElasticQueryConn
from genelastic.import_data.checker_observer import CheckerObserver
from genelastic.import_data.models.analyses import Analyses
from genelastic.import_data.models.processes import Processes

logger = logging.getLogger("genelastic")


class Checker:
    """Validate coherence between YAML metadata and Elasticsearch,
    using a project-specific observer mechanism.
    """

    def __init__(self, es: ElasticQueryConn, *, strict: bool = False) -> None:
        """Initialize the Checker.

        Args:
            es: Elasticsearch connection instance.
            strict: Treat ES-only entries as errors when True.
        """
        self.es = es
        self.strict = strict
        self.errors_detected = False
        self._observers: list[CheckerObserver] = []

    def attach(self, observer: CheckerObserver) -> None:
        """Register an observer to receive Checker notifications."""
        self._observers.append(observer)

    def detach(self, observer: CheckerObserver) -> None:
        """Unregister an observer so it no longer receives notifications."""
        self._observers.remove(observer)

    def _notify_missing(self, label: str, missing: list[str]) -> None:
        """Notify observers about missing IDs."""
        self.errors_detected = True
        for obs in self._observers:
            obs.notify_missing(label, missing)

    def _notify_extra(self, label: str, extra: list[str]) -> None:
        """Notify observers about extra IDs."""
        self.errors_detected = True
        for obs in self._observers:
            obs.notify_extra(label, extra)

    def _check_generic(
        self, label: str, ids_yaml: set[str], ids_es: set[str]
    ) -> None:
        """Compare YAML IDs vs Elasticsearch IDs for a given entity type."""
        logger.info("Checking %s...", label)

        missing = sorted(ids_yaml - ids_es)
        extra = sorted(ids_es - ids_yaml)

        if missing:
            logger.error("Missing %s in ES: %s", label, missing)
            self._notify_missing(label, missing)

        if extra:
            if self.strict:
                logger.error(
                    "%s in ES but missing from YAML: %s",
                    label.capitalize(),
                    extra,
                )
                self._notify_extra(label, extra)
            else:
                logger.info("Extra %s ignored (non-strict mode).", label)

        if not missing and (self.strict and not extra):
            logger.info("OK ✓ All %s match exactly.", label)
        elif not missing and not self.strict:
            logger.info("OK ✓ YAML %s present (extra ignored).", label)

    def check_analyses(self, analyses: Analyses) -> None:
        """Check analysis IDs between YAML and Elasticsearch."""
        ids_yaml = {a.id for a in analyses}
        ids_es = set(
            self.es.get_field_values(self.es.data_files_index, "analysis_id")
        )
        self._check_generic("analyses", ids_yaml, ids_es)

    def check_wet_processes(self, processes: Processes) -> None:
        """Check wet process IDs between YAML and Elasticsearch."""
        ids_yaml = set(processes.keys())
        ids_es = set(
            self.es.get_field_values(self.es.wet_processes_index, "proc_id")
        )
        self._check_generic("wet processes", ids_yaml, ids_es)

    def check_bi_processes(self, processes: Processes) -> None:
        """Check biological process IDs between YAML and Elasticsearch."""
        ids_yaml = set(processes.keys())
        ids_es = set(
            self.es.get_field_values(self.es.bi_processes_index, "proc_id")
        )
        self._check_generic("bi processes", ids_yaml, ids_es)
