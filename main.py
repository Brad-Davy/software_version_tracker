import subprocess
from packaging import version

def get_latest_tag(repo_url: str = None) -> str:

    #######################################################
    ## Run a git command to pull all tags from a remort url
    #######################################################

    try:
        result = subprocess.run(
            ["git", "ls-remote", "--tags", repo_url],
            capture_output=True, text=True, check=True
        )

        tags = [line.split("/")[-1] for line in result.stdout.splitlines() if "refs/tags" in line]
        tags = [t.strip() for t in tags if t.strip()]

        #####################################################################
        ## Determine if the tag is a valid release, i.e. not a dev tag and so
        ## on
        #####################################################################

        valid_releases = []
        for t in tags:
            clean_tag = t.lstrip('v')

            #################################################################
            ## Here we create a version object which is designed to work with
            ## typical versioning norms.
            #################################################################

            try:
                parsed = version.parse(clean_tag)
                if not (parsed.is_prerelease or parsed.is_devrelease):
                    valid_releases.append(t)
            except version.InvalidVersion:
                continue

        #########################################################
        ## Check if the list is empty, i.e. no stable tags found.
        #########################################################

        if len(valid_releases) == 0:
            print("No valid stable release tags found.")
            return None

        latest_tag = sorted(valid_releases, key=lambda t: version.parse(t.lstrip('v')))[-1]
        return latest_tag.lstrip('v')

    ############################################
    ## Catch errors from running the git command
    ############################################

    except subprocess.CalledProcessError as e:
        print("Error running git command:", e)
        return None


hpc_repos = [
    # --- MPI / Communication ---
    "https://github.com/open-mpi/ompi.git",
    "https://github.com/pmodels/mpich.git",
    "https://github.com/openucx/ucx.git",

    # --- Math Libraries ---
    "https://github.com/FFTW/fftw3.git",
    "https://github.com/flame/blis.git",
    "https://github.com/xianyi/OpenBLAS.git",
    "https://github.com/Reference-ScaLAPACK/scalapack.git",
    "https://gitlab.com/petsc/petsc.git",
    "https://gitlab.com/slepc/slepc.git",

    # --- Parallel / Accelerator Frameworks ---
    "https://github.com/NVIDIA/cuda-samples.git",
    "https://github.com/ROCm/HIP.git",
    "https://github.com/RadeonOpenCompute/ROCm.git",
    "https://github.com/kokkos/kokkos.git",
    "https://github.com/LLNL/RAJA.git",

    # --- Tools / Build / Profiling ---
    "https://github.com/spack/spack.git",
    "https://github.com/easybuilders/easybuild-framework.git",
    "https://github.com/TACC/Lmod.git",

    # --- Python / HPC Ecosystem ---
    "https://github.com/python/cpython.git",
    "https://github.com/h5py/h5py.git",
    "https://github.com/mpi4py/mpi4py.git",

    # Test
    "http://git.savannah.gnu.org/r/m4.git",
]

for repo in hpc_repos:
    print(f"Latest stable tag for {repo}: {get_latest_tag(repo_url=repo)}")
