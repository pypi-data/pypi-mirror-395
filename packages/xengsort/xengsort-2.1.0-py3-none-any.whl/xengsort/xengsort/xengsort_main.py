"""
xengsort_main.py
xengsort: xenograft indexing and classification
by Jens Zentgraf & Sven Rahmann, 2019--2023
"""

from importlib import import_module  # dynamically import subcommand
from importlib.metadata import metadata
from os.path import dirname, join as pathjoin

from jsonargparse import ArgumentParser, ActionConfigFile, SUPPRESS
from jsonargparse.typing import restricted_number_type

from ..lowlevel.debug import set_debugfunctions
from ..fastcash_main import info, get_name_version_description


def get_config_path():
    xengsortfolder = dirname(__file__)
    cfgpath = pathjoin(xengsortfolder, "config")
    return cfgpath


def classify(p):
    p.add_argument("--fastq", "-q", metavar="FASTQ", required=True, nargs="+",
        help="single or first paired-end FASTQ file to classify")
    p.add_argument("--pairs", "-p", metavar="FASTQ", nargs="+",
        help="second paired-end FASTQ file (only together with --fastq)")
    p.add_argument("--index", required=True,
        help="existing index")
    p.add_argument("--shared", action="store_true",
        help="The index should be loaded via shared memory")
    p.add_argument("--out", "-o", "--prefix", required=True,
        dest="prefix", metavar="PREFIX",
        help="prefix for output files (directory and name prefix)")
    p.add_argument("--compression", default="gz", choices=("none", "gz", "bz2", "xz"),
        help="Compression of output files")
    CL_CHOICES = ("count", "coverage", "quick")
    p.add_argument("--classification", "--mode", metavar="MODE",
        choices=CL_CHOICES, help=f"classification mode {CL_CHOICES}")
    p.add_argument("--params_count", type=dict, help=SUPPRESS)
        # help="All paramteres for classification based on counts as a dictionary. Update in config file.")
    p.add_argument("--params_bisulfite", type=dict, help=SUPPRESS)
        # help="All paramteres for classification based on counts as a dictionary. Update in config file.")
    p.add_argument("--params_coverage", type=dict, help=SUPPRESS)
        # help="All paramteres for classification based on coverage as a dictionary. Update in config file.")
    p.add_argument("--threads", "-T", "-j", metavar="INT", type=int,
        help="maximum number of worker threads for classification")
    gmode = p.add_mutually_exclusive_group(required=False)
    gmode.add_argument("--filter", action="store_true",
        help="only output the graft FASTQ file, not the other class FASTQ files")
    gmode.add_argument("--count", action="store_true",
        help="only count reads or read pairs for each class, do not output any FASTQ")
    p.add_argument("--prefetchlevel", metavar="INT",
        type=restricted_number_type("from_0_to_2", int, [(">=", 0), ("<=", 2)]),
        help="amount of prefetching: none (0), second bucket (1), all buckets (2)")
    p.add_argument("--chunksize", "-C", metavar="FLOAT_SIZE_MB", type=float, default=8.0,
        help="chunk size in MB; one chunk is allocated per thread.")
    p.add_argument("--chunkreads", "-R", metavar="INT", type=int,
        help="maximum number of reads per chunk per thread [SIZE_MB*(2**20) // 200]")
    p.add_argument("--progress", "-P", action="store_true",
        help="Show progress")


def index(p):
    p.add_argument("--index", required=True,
        help="name of the resulting index (.hash and .info output)")
    p.add_argument("--host", "-H", metavar="FASTA", nargs="+",
        help="reference FASTA file(s) for the host organism")
    p.add_argument("--graft", "-G", metavar="FASTA", nargs="+",
        help="reference FASTA file(s) for the graft organism")
    # TODO? support for a precomputed set of k-mers with values (dump)?

    p.add_argument("-n", "--nobjects", metavar="INT",
        type=int, required=True,
        help="number of k-mers to be stored in hash table (4_500_000_000 for mouse+human)")

    k_group = p.add_mutually_exclusive_group(required=True)
    k_group.add_argument('--mask', metavar="MASK", type=str,
        help="gapped k-mer mask (quoted string like '#__##_##__#')")
    k_group.add_argument('-k', '--kmersize', dest="mask",
        type=int, metavar="INT", help="k-mer size")

    p.add_argument("--type", default="default",
        # help="hash type (e.g. s3c_fbcbvb), implemented in hash_{TYPE}.py")
        help=SUPPRESS)
    p.add_argument("--bucketsize", "-b", "-p",
        metavar="INT", type=int, required=True,
        help="bucket size, i.e. number of elements in a bucket")
    p.add_argument("--fill",
        type=float, metavar="FLOAT",
        help="desired fill rate (< 1.0) of the hash table")
    p.add_argument("--subtables", type=int, metavar="INT",  # no default -> None!
        help="number of subtables used; subtables+1 threads are used")
    p.add_argument("--threads-read", type=int,  # 2?
        help="Number of reader threads")
    p.add_argument("--threads-split", type=int,  # 4?
        help="Number of splitter threads")

    p.add_argument("--shortcutbits", "-S", metavar="INT",
        type=restricted_number_type("from_0_to_2", int, [(">=", 0), ("<=", 2)]),
        help="number of shortcut bits (0,1,2)")
    p.add_argument("--hashfunctions", "--functions", metavar="SPEC", default="default",
        help="hash functions: 'default', 'random', or 'func0:func1:func2:func3'")
    p.add_argument("--aligned", action="store_true",
        help="use power-of-two-bits-aligned buckets (slightly faster, but larger)")
    p.add_argument("--statistics", "--stats",
        choices=("none", "summary", "details", "full"), default="summary",
        help="level of detail for statistics (none, summary, details, full (all subtables))")
    p.add_argument("--weakthreads", "-W", metavar="INT", type=int,
        help="calculate weak kmers with the given number of threads")
    p.add_argument("--groupprefixlength",
        metavar="INT", type=int,
        help="calculate weak k-mers in groups with common prefix of this length")
    p.add_argument("--maxwalk", metavar="INT", type=int,
        help="maximum length of random walk through hash table before failing")
    p.add_argument("--maxfailures", metavar="INT", type=int,
        help="continue even after this many failures; forever: -1]")
    p.add_argument("--walkseed", type=int, metavar="INT",
        help="seed for random walks while inserting elements")
    p.add_argument("--bisulfite", action='store_true',
        help="filtering WGBS data with translated index (EXPERIMENTAL)")


def load(p):
    p.add_argument("--name", required=True,
        help="name (prefix) of the index to load into shared memory")


def remove(p):
    p.add_argument("--name", required=True,
        help="name (prefix) of the index to remove from shared memory")


CFGPATH = get_config_path()
SUBCOMMANDS = [
    ("index",
        "build index of two species' FASTA references (toplevel + cdna) for xenograft sorting",
        index,
        "xengsort_index", "main",
        [f"{CFGPATH}/index.yaml", 'config/index.yaml', 'index.yaml']),
    ("classify",
        "sort (or filter or count) FASTQ reads according to species of origin",
        classify,
        "xengsort_classify", "main",
        [f"{CFGPATH}/classify.yaml", 'config/classify.yaml', 'classify.yaml']),
    ("info",
        "get information about a hash table and dump its data",
        info,
        "xengsort_info", "main", []),
    ("load",
        "Load the index as a shared memory object with the provided name.",
        load,
        "xengsort_load", "main", []),
    ("remove",
        "Remove the shared memory object with the provided name.",
        remove,
        "xengsort_remove", "main", []),
        ]


# main argument parser #############################

def get_argument_parser():
    """
    return an ArgumentParser object
    that describes the command line interface (CLI)
    of this application
    """

    NAME, VERSION, DESCRIPTION = get_name_version_description(__package__, __file__)
    p = ArgumentParser(
        prog="xengsort",
        description=DESCRIPTION,
        epilog="(c) 2019-2024 by Algorithmic Bioinformatics, Saarland University. MIT License."
    )
    # global options
    p.add_argument("--version", action="version", version=VERSION,
        help="show version and exit")
    p.add_argument("--debug", "-D", action="count", default=0,
        help="output debugging information (repeat for more)")

    # add subcommands to parser
    scs = p.add_subcommands()
    subcommands = SUBCOMMANDS
    for (name, helptext, f_parser, module, f_main, default_configs) in subcommands:
        if name.endswith('!'):
            name = name[:-1]
            chandler = 'resolve'
        else:
            chandler = 'error'
        sp = ArgumentParser(prog=name, description=helptext,
            default_config_files=default_configs)
        if name in ["classify", "index"]:
            sp.add_argument('--cfg', "--config", action=ActionConfigFile)
        sp.add_argument("--func", default=(module, f_main), help=SUPPRESS)
        f_parser(sp)
        scs.add_subcommand(name, sp, help=helptext,
            description=helptext, conflict_handler=chandler)
    return p


def main(args=None):
    p = get_argument_parser()
    pargs = p.parse_args() if args is None else p.parse_args(args)
    set_debugfunctions(debug=pargs.debug, timestamps=pargs.debug)
    sc_pargs = pargs[pargs.subcommand]
    (module, f_main) = sc_pargs.func
    m = import_module("." + module, __package__)
    mymain = getattr(m, f_main)
    mymain(sc_pargs)
