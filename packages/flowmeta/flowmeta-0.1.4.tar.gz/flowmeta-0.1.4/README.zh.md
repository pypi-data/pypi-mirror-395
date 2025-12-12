gunzip GCA_000001405.28_GRCh38.p13_genomic.fna.gz
# FlowMeta: Operations Quick Reference 🌟

> Repository: <https://github.com/SkinMicrobe/FlowMeta>  
> Title: FlowMeta: Automated End-to-End Metagenomic Profiling Pipeline  
> Author: Dongqiang Zeng  
> Email: interlaken@smu.edu.cn

## 1. Overview

FlowMeta consolidates 10 previously separate shell and Python scripts into a single Python package. Through the `flowmeta_base` command you can execute the entire workflow from `fastp → Bowtie2 → Kraken2/Bracken → host filtering → downstream merges`, suitable for microbiome, environmental, soil, or clinical shotgun metagenomic studies.

- Each stage writes `*.task.complete` markers to support resumable execution.
- Optional shared-memory caching accelerates Kraken2 when large databases are involved.
- The `--project_prefix` flag tags Step 6 merged files (for example `SMOOTH-`).

## 2. Environment and installation

```bash
conda activate meta   # Python >= 3.8
pip install flowmeta   # install from PyPI
```

Use [`environment.yml`](environment.yml) to recreate the recommended Conda environment. External executables required on `PATH` include fastp, Bowtie2, samtools, kraken2, bracken, pigz, and seqkit.

## 3. Typical invocation

```bash
flowmeta_base \
    --input_dir /mnt/data/01-raw \
    --output_dir /mnt/data/flowmeta-out \
    --db_bowtie2 /mnt/db/GRCh38_noalt_as/GRCh38_noalt_as \
    --db_kraken /mnt/db/k2ppf \
    --threads 32 \
    --project_prefix SMOOTH-
```

### Output layout

```
01-raw/        Raw FASTQ (read-only)
02-qc/         fastp reports and QC checkpoints
03-hr/         Host-depleted FASTQ
04-bam/        Bowtie2 BAM files and stats
05-host/       Optional host read exports
06-ku/         Kraken2 reports (round one)
07-bracken/    Bracken abundance tables
08-ku2/        Host-filtered rerun outputs
09-mpa/        Final OTU/MPA/summary matrices
```

## 4. Frequently used flags

| Flag | Description |
| --- | --- |
| `--input_dir` | Raw FASTQ directory; expects `_1.fastq.gz` / `_2.fastq.gz` pairs by default. |
| `--output_dir` | Pipeline workspace; automatically creates directories `02-qc` through `09-mpa`. |
| `--db_bowtie2` | Bowtie2 index prefix. |
| `--db_kraken` | Kraken2 database directory containing `hash.k2d`, `opts.k2d`, `taxo.k2d`. |
| `--threads` | Thread count for fastp, Bowtie2, and Kraken2. |
| `--batch` | Number of samples processed concurrently for fastp/Kraken2. |
| `--min_count` | Bracken minimum count threshold for Step 5 host filtering. |
| `--check_result` | Enable integrity checks for Steps 2 and 4 (off by default to save time). |
| `--project_prefix` | Prefix applied to Step 6 merged products (e.g. `SMOOTH-`). |
| `--skip_host_extract` | Skip Step 5 host read extraction. |
| `--force` | Force recomputation from the step specified by `--step`. |
| `--step` | Resume from a given logical step (1–10). Leave unset to run everything. |
| `--no_shm` / `--shm_path` | Control whether the Kraken2 database is copied to shared memory. |

Refer to `docs/tutorial.html` for the complete CLI description and troubleshooting guidance.

## 5. Step 说明与断点续跑

通过 `--step N` 可以仅运行某一阶段（默认 `--step 1`，即全流程）。进入每个 Step 前，CLI 会打印“这一步要做什么？预计多少样本可用”，并说明当前 `--force` 状态，便于判断是否需要重新生成结果。启动时还会输出一次路径总览。开启 `--check_result` 时才会跑 Step 2/4 的完整性检查（默认关闭以节省时间）。

| Step | 目的 | 进入时统计的样本/文件 |
| --- | --- | --- |
| 1 | fastp 质控与修剪。 | `01-raw` 中符合 `suffix1` 的 FASTQ（单双端皆可）。 |
| 2 | fastp 结果完整性验证（需 `--check_result`）。 | `02-qc` 下的 `.task.complete` 或 `_fastp.json`。 |
| 3 | Bowtie2 去宿主并生成 BAM/FASTQ。 | `02-qc` 中的 `.task.complete`。 |
| 4 | 去宿主 FASTQ 完整性检查（需 `--check_result`）。 | `03-hr` 中 `_host_remove_R1.fastq.gz`。 |
| 5 | （可选）samtools 导出宿主 reads。 | `04-bam` 中 `.bam`。 |
| 6 | 将 Kraken2 数据库拷贝到共享内存（若未 `--no_shm`）。 | N/A |
| 7 | Kraken2/Bracken 分类。 | `03-hr` 中 `_host_remove_R1.fastq.gz`。 |
| 8 | Kraken 报告验证。 | `06-ku` 中 `.kraken.report.std.txt`。 |
| 9 | 二次去宿主并重跑 Bracken。 | `06-ku` 中 `.kraken.report.std.txt`。 |
| 10 | 合并 OTU/MPA/Bracken 矩阵。 | `08-ku2` 中 `.nohuman.kraken.mpa.std.txt` + `07-bracken` 中 `.bracken`。 |

`--force` 可与任意 Step 一起使用，以忽略相应目录中的 `.task.complete`。

## 6. Build the package

```bash
pip install build
python -m build --wheel
ls dist/
```

Wheel artifacts install on any Python ≥ 3.8 interpreter. Run `python -m build --sdist` when preparing a PyPI release so that documentation is bundled with the source distribution.

## 7. Reference databases

### Kraken2

- Download official libraries: <https://benlangmead.github.io/aws-indexes/k2>
- Extract to a location such as `/mnt/db/k2ppf` and point `--db_kraken` to the directory containing `hash.k2d`, `opts.k2d`, and `taxo.k2d`.
- SSD or RAM-disk staging delivers the best throughput for large projects.

### Bowtie2 (human GRCh38 example)

```bash
wget https://ftp.ncbi.nlm.nih.gov/genomes/all/GCA/000/001/405/GCA_000001405.28_GRCh38.p13/GCA_000001405.28_GRCh38.p13_genomic.fna.gz
gunzip GCA_000001405.28_GRCh38.p13_genomic.fna.gz
seqkit grep -rvp "alt|PATCH" GCA_000001405.28_GRCh38.p13_genomic.fna > GRCh38_noalt.fna
mkdir -p /mnt/db/GRCh38_noalt_as
bowtie2-build GRCh38_noalt.fna /mnt/db/GRCh38_noalt_as/GRCh38_noalt_as
flowmeta_base ... --db_bowtie2 /mnt/db/GRCh38_noalt_as/GRCh38_noalt_as
```

## 8. Documentation links

- Primary README: [`README.md`](README.md)
- Detailed HTML tutorial: [`docs/tutorial.html`](docs/tutorial.html)
- Quick validation script: `docs/quickstart.md`

## 9. Contact

For support or collaboration, contact **Dongqiang Zeng** at <interlaken@smu.edu.cn>. The canonical repository is <https://github.com/SkinMicrobe/FlowMeta>.

