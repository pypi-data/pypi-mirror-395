import random
import sys
import tempfile
import typing
from abc import ABC, abstractmethod
from pathlib import Path

import yaml
from biophony import (
    BioSeqGen,
    CovGen,
    Elements,
    FastaWriter,
    MutSim,
    MutSimParams,
)

from genelastic.common.types import (
    RandomAnalysisData,
    RandomBiProcessData,
    RandomWetProcessData,
)


class RandomBundleItem(ABC):
    """Abstract class representing a randomly generated bundle item."""

    def _random_alphanum_str(
        self, chars: str = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789", n: int = 4
    ) -> str:
        """Generate a random alphanumerical string."""
        return "".join(random.sample(list(chars), n))

    @abstractmethod
    def to_dict(self) -> typing.Any:  # noqa: ANN401
        """Return the randomly generated item data as a dict."""


class RandomWetProcess(RandomBundleItem):
    """Generate a random wet lab process.

    :param seed: Set a seed for data reproducibility.
    """

    KITS: typing.ClassVar = [
        {
            "generic_kit": "truseq-illumina",
            "library_kit": "truseq-illumina",
            "sequencing_kit": "truseq-illumina",
        },
        {
            "generic_kit": "smrtbellprepkit3.0",
            "library_kit": "smrtbellprepkit3.0",
            "sequencing_kit": "revio_polymerase_sequencing",
        },
        {
            "generic_kit": "sqk-lsk114",
            "library_kit": "sqk-lsk114",
            "sequencing_kit": "sqk-lsk114",
        },
    ]

    def __init__(self, seed: int | None = None) -> None:
        random.seed(seed)

        self._proc_id = self._random_alphanum_str(n=8)
        self._manufacturer = random.choice(["illumina", "ont", "pacbio"])
        self._sequencer = random.choice(
            ["novaseqxplus", "promethion", "novaseq6000", "revio"]
        )

        kit: dict[str, str] = random.choice(self.KITS)
        self._generic_kit = kit["generic_kit"]
        self._library_kit = kit["library_kit"]
        self._sequencing_kit = kit["sequencing_kit"]

        self._fragmentation = random.choice(range(100, 401, 50))
        self._reads_size = random.choice(range(100, 401, 50))
        self._flowcell_type = f"{random.choice(range(10, 101, 10))}b"
        self._sequencing_type = "wgs" + random.choice(["", "-iclr", "-lowpass"])
        self._error_rate_expected = round(random.uniform(0.01, 0.1), 2)

    def to_dict(self) -> RandomWetProcessData:
        """Return the generated wet lab process as a dictionary."""
        return {
            "proc_id": self._proc_id,
            "manufacturer": self._manufacturer,
            "sequencer": self._sequencer,
            "generic_kit": self._generic_kit,
            "library_kit": self._library_kit,
            "sequencing_kit": self._sequencing_kit,
            "fragmentation": self._fragmentation,
            "reads_size": self._reads_size,
            "input_type": "gdna",
            "amplification": "pcr-free",
            "flowcell_type": self._flowcell_type,
            "sequencing_type": self._sequencing_type,
            "error_rate_expected": self._error_rate_expected,
        }


class RandomBiProcess(RandomBundleItem):
    """Generate a random bioinformatics process.

    :param seed: Set a seed for data reproducibility.
    """

    STEPS: typing.ClassVar = [
        {"name": "basecalling", "cmd": ["bclconvert", "dorado", "smrtlink"]},
        {"name": "mapping", "cmd": ["bwa", "dragmap", "minimap", "pbmm"]},
        {"name": "postmapping", "cmd": ["bqsr", "dragen"]},
        {
            "name": "smallvarcalling",
            "cmd": [
                "gatk_haplotypecaller",
                "octopus",
                "glimpse",
                "dragen",
                "deepvariant",
                "clair",
            ],
            "output": "smallvar",
        },
        {
            "name": "svcalling",
            "cmd": ["manta", "dragen", "sniffles", "cutesv", "pbsv"],
            "output": "sv",
        },
        {"name": "secondary_qc", "cmd": ["genomx", "dragen", "lrqc"]},
        {"name": "trimming", "cmd": ["dragen", "seqfiltering"]},
        {"name": "phasing", "cmd": ["whatshap"]},
    ]

    def __init__(self, seed: int | None = None) -> None:
        random.seed(seed)

        self._proc_id = self._random_alphanum_str(n=8)

        version_str_len = random.choice(range(1, 5))
        self._pipeline_version = self._generate_version(version_str_len)
        self._name = random.choice(
            ["varscope", "glimpse", "dragen", "vacana", "pbvaria"]
        )

        self._steps: list[dict[str, str]] = []
        self._generate_steps()

    @staticmethod
    def _generate_version(count: int) -> str:
        """Generate a random version string.

        :param count: Count of numbers present in the number string.
        :raises ValueError: If count is less than 1.
        :return: A random version string with the specified count of numbers.
        """
        if count < 1:
            msg = "Count of numbers present in the version string must be > 0."
            raise ValueError(msg)

        lower_bound = 0
        # Do not use 0 for versions string with only one number.
        if count == 1:
            lower_bound = 1

        version_parts = [
            str(random.randint(lower_bound, 9)) for _ in range(count)
        ]
        return ".".join(version_parts)

    def _generate_steps(self) -> None:
        steps_count = random.randint(1, 5)
        random_steps = random.sample(self.STEPS, steps_count)
        for rs in random_steps:
            v = self._generate_version(random.choice(range(1, 5)))
            self._steps.append(
                {
                    "version": v,
                    "name": str(rs["name"]),
                    "cmd": random.choice(rs["cmd"]),
                }
            )

    def to_dict(self) -> RandomBiProcessData:
        """Return the generated bi informatics process as a dictionary."""
        return {
            "proc_id": self._proc_id,
            "name": self._name,
            "pipeline_version": self._pipeline_version,
            "steps": self._steps,
            "sequencing_type": "wgs",
        }


class RandomAnalysis(RandomBundleItem):
    """Generate a random analysis.

    :param fasta_dir: Directory where to create the FASTA file used as a basis to generate the analysis VCF file.
    :param output_dir: Directory where the analysis VCF file
        (and coverage file if `do_gen_coverage` is set to True) is generated.

    :raises RuntimeError: Could not generate a VCF file with the given simulation parameters.
    """

    def __init__(  # noqa: PLR0913
        self,
        fasta_dir: Path,
        output_dir: Path,
        seq_len: int,
        nb_chrom: int,
        wet_proc_id: str,
        bi_proc_id: str,
        sim_params: MutSimParams,
        *,
        do_gen_coverage: bool,
    ) -> None:
        self._fasta_dir = fasta_dir
        self._output_dir = output_dir
        self._seq_len = seq_len
        self._nb_chrom = nb_chrom
        self._wet_process_id = wet_proc_id
        self._bi_process_id = bi_proc_id

        self._sample_name = "HG000" + str(random.randint(1, 9))
        sim_params.sample_name = self._sample_name
        self._sim_params = sim_params

        self._source = "CNRGH"
        self._barcode = self._random_alphanum_str(n=6)
        self._reference_genome = "hg38"
        self._prefix = (
            f"{self._sample_name}_{self._source}_{self._wet_process_id}_{self._bi_process_id}_"
            f"{self._barcode}_{self._reference_genome}"
        )

        self._gen_vcf_file()
        if do_gen_coverage:
            self.gen_cov_file()

    def _gen_vcf_file(self) -> None:
        """Generate a dummy VCF file.

        :raises RuntimeError: The call to `mutation-simulator` returned a non-zero exit status.
        """
        fasta_out_file = self._fasta_dir / "seq.fasta"
        vcf_out_file = self._output_dir / f"{self._prefix}.vcf"

        # 1 - Generate a FASTA file and save it to a temporary directory.
        gen = BioSeqGen(
            elements=Elements(), seqlen=self._seq_len, count=self._nb_chrom
        )
        with fasta_out_file.open("w", encoding="utf-8") as f:
            FastaWriter(f, header=False).write_seqs(gen)

        # 2 - Generate a VCF from the previously created FASTA file.
        MutSim(
            fasta_file=str(fasta_out_file),
            vcf_file=str(vcf_out_file),
            sim_params=self._sim_params,
        ).run()

    def gen_cov_file(self) -> None:
        """Generate a dummy coverage file."""
        chrom_end = self._seq_len - 1

        output_path = self._output_dir / f"{self._prefix}.cov.tsv"
        with output_path.open("w", encoding="utf-8") as f:
            for chrom in range(1, self._nb_chrom + 1):
                coverage = CovGen(
                    chrom=str(chrom),
                    min_pos=0,
                    max_pos=chrom_end,
                    min_depth=5,
                    max_depth=15,
                    depth_offset=0,
                    depth_change_rate=0.1,
                )

                for item in coverage:
                    f.write(item.to_bed_line() + "\n")

    def to_dict(self) -> RandomAnalysisData:
        """Return the generated analysis as a dictionary."""
        return {
            "file_prefix": "%S_%F_%W_%B_%A_%R",
            "sample_name": self._sample_name,
            "source": self._source,
            "barcode": self._barcode,
            "wet_process": self._wet_process_id,
            "bi_process": self._bi_process_id,
            "reference_genome": self._reference_genome,
            "flowcell": self._random_alphanum_str(n=8),
            "lanes": [random.randint(1, 10)],
            "seq_indices": [
                "DUAL219",
                "DUAL222",
                "DUAL225",
                "DUAL228",
                "DUAL289",
            ],
            "data_path": str(self._output_dir),
        }


class RandomBundle(RandomBundleItem):
    """Generate a random analyses bundle."""

    def __init__(  # noqa: PLR0913
        self,
        output_dir: Path,
        analyses_count: int,
        processes_count: int,
        nb_chrom: int,
        seq_len: int,
        sim_params: MutSimParams,
        *,
        do_gen_coverage: bool,
    ) -> None:
        self._output_dir = output_dir
        self._analyses_count = analyses_count
        self._processes_count = processes_count
        self._nb_chrom = nb_chrom
        self._seq_len = seq_len
        self._do_gen_coverage = do_gen_coverage
        self._analyses: list[RandomAnalysisData] = []

        self._wet_processes = [
            RandomWetProcess().to_dict() for _ in range(self._processes_count)
        ]
        self._assigned_wet_processes = self._assign_processes(
            self._wet_processes, self._analyses_count
        )

        self._bi_processes = [
            RandomBiProcess().to_dict() for _ in range(self._processes_count)
        ]
        self._assigned_bi_processes = self._assign_processes(
            self._bi_processes, self._analyses_count
        )

        with tempfile.TemporaryDirectory() as fasta_dir:
            try:
                self._analyses.extend(
                    [
                        RandomAnalysis(
                            Path(fasta_dir),
                            self._output_dir,
                            self._seq_len,
                            self._nb_chrom,
                            str(self._assigned_wet_processes[i]["proc_id"]),
                            str(self._assigned_bi_processes[i]["proc_id"]),
                            sim_params,
                            do_gen_coverage=self._do_gen_coverage,
                        ).to_dict()
                        for i in range(self._analyses_count)
                    ]
                )
            except RuntimeError as e:
                msg = f"VCF file generation for one analysis failed. {e}"
                raise SystemExit(msg) from None

    @staticmethod
    def _assign_processes(
        random_processes: list[dict[str, typing.Any]],
        analyses_count: int,
    ) -> list[dict[str, typing.Any]]:
        """Assigns a specified number of processes to analyses.

        This function ensures that the returned list contains exactly `analyses_count` processes:
            - If there are more processes than required, it selects a random subset.
            - If there are fewer processes than required, it extends the list by randomly selecting additional
              processes until the desired size is reached.
            - If the number of processes matches the number of analyses, the same list is returned.

        :param random_processes: A list of available processes.
        :param analyses_count: The number of processes required.
        :raises ValueError: If the input list `random_processes` is empty.
        :returns: A list of processes with a length of `analyses_count`.
        """
        if not random_processes:
            msg = "Random processes list is empty."
            raise ValueError(msg)

        if len(random_processes) > analyses_count:
            # Case 1: More processes than analyses.
            # Select a random subset of processes with the required size.
            return random.sample(random_processes, analyses_count)

        # Case 2: Equal or fewer processes than analyses.
        # If the number of processes equals the number of analyses, return the same list.
        # Otherwise, extend the list by randomly selecting additional processes until the desired size is reached.
        random_process_copy = random_processes.copy()

        while len(random_process_copy) < analyses_count:
            random_process_copy.append(random.choice(random_processes))

        return random_process_copy

    # Write import bundle YAML
    def to_yaml(self, output_file: Path | None) -> None:
        """Export the generated bundle in YAML format to a file or stdout."""
        # Standard output
        if not output_file:
            sys.stdout.write("---\n")
            yaml.dump(self.to_dict(), sys.stdout)

        # File
        else:
            with output_file.open("w", encoding="utf-8") as f:
                f.write("---\n")
                yaml.dump(self.to_dict(), f)

    def to_dict(
        self,
    ) -> dict[
        str,
        int
        | list[RandomAnalysisData]
        | list[RandomBiProcessData]
        | list[RandomWetProcessData],
    ]:
        """Return the generated bundle as a dictionary."""
        return {
            "version": 3,
            "analyses": self._analyses,
            "bi_processes": self._bi_processes,
            "wet_processes": self._wet_processes,
        }
