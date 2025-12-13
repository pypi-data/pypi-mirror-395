import httpx, re, asyncio, uvicorn
import tomllib
from super_pocket.settings import click, CONTEXT_SETTINGS, add_help_command
from super_pocket.utils import print_error
from pathlib import Path
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Sequence, Callable
from rich.console import Console

console = Console()


app = FastAPI(title="Requirements Checker API")

# CORS settings to allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PackageInput(BaseModel):
    package: str
    version: str


class PackageResult(BaseModel):
    package: str
    current_version: str
    latest_patch: Optional[str] = None
    latest_overall: Optional[str] = None
    status: str
    message: Optional[str] = None


class CheckRequest(BaseModel):
    packages: List[PackageInput]


def _read_requirements_file(path: Path) -> List[str]:
    """Returns the dependencies extracted from a requirements file."""
    try:
        with open(path, "r") as f:
            lines = [l.strip() for l in f.readlines()[2:]]

    except FileNotFoundError as exc:
        print_error(exc, custom=True, message=f"Requirements file not found: {path}")
        raise
    except OSError as exc:
        print_error(exc, custom=True, message=f"Unable to read {path}")
        raise

    specs: List[str] = []
    for line in lines:
        if not line or line.startswith("#") or line.startswith("--"):
            continue
        spec = _normalize_dependency_spec(line)
        specs.append(spec)

    if not specs:
        print_error(ValueError(f"No valid package found in {path}"), custom=True, message="No valid package found in {path}")
        return []

    return specs


def _read_pyproject_file(path: Path) -> List[str]:
    """Returns the dependencies extracted from a pyproject.toml file."""
    try:
        content = path.read_bytes()
    except FileNotFoundError as e:
        print_error(e, custom=True, message=f"pyproject.toml file not found: {path}")
        raise
    except OSError as exc:
        print_error(exc, custom=True, message=f"Unable to read {path}")
        raise

    try:
        data = tomllib.loads(content.decode("utf-8"))
    except tomllib.TOMLDecodeError as exc:
        print_error(exc, custom=True, message=f"TOML parsing error in {path}")
        raise

    specs: List[str] = []
    
    # Extract the main dependencies
    dependencies = data.get("project", {}).get("dependencies", [])
    for dep in dependencies:
        # Convert the version specifications to ==version format
        # Supported: package>=1.0.0, package~=1.0, package==1.0.0, etc.
        spec = _normalize_dependency_spec(dep)
        if spec:
            specs.append(spec)
    
    # Optional: extract also the optional dependencies
    optional_deps = data.get("project", {}).get("optional-dependencies", {})
    for group_name, group_deps in optional_deps.items():
        for dep in group_deps:
            spec = _normalize_dependency_spec(dep)
            if spec:
                specs.append(spec)

    if not specs:
        print_error(ValueError, custom=True, message=f"No dependencies found in {path}")
        raise

    return specs


def _normalize_dependency_spec(dep: str) -> Optional[str]:
    """Normalize a dependency specification to package==version format."""
    # If already in package==version format, return it as is
    if "==" in dep:
        return dep
    
    # Extract the package name and version for the other formats
    # Supported: >=, ~=, >, <, <=, !=
    match = re.match(r'^([a-zA-Z0-9_-]+)\s*([><=!~]+)\s*(.+)$', dep)
    if match:
        package = match.group(1)
        operator = match.group(2)
        version = match.group(3)
        
        # For >=, ~=, use the minimum version specified
        if operator in (">=", "~=", ">"):
            return f"{package}=={version}"

        # For ==, return it as is
        elif operator == "==":
            return dep
    
    # If no version specified, ignore
    return None


def _expand_spec_inputs(inputs: Sequence[str]) -> List[str]:
    """Decompose CLI arguments: commas, requirements files, pyproject.toml, etc."""
    expanded: List[str] = []
    for entry in inputs:
        if not entry:
            continue
        entry = entry.strip()

        # Handle comma-separated lists in a single argument
        if ',' in entry:
            parts = [part.strip() for part in entry.split(',')]
            expanded.extend(parts)
            continue

        potential_path = Path(entry).expanduser()
        if potential_path.is_file():
            # Detect the file type and use the appropriate parser
            if potential_path.name == "pyproject.toml":
                expanded.extend(_read_pyproject_file(potential_path))
            else:
                # By default, treat as a requirements.txt file
                expanded.extend(_read_requirements_file(potential_path))
            continue

        expanded.append(entry)

    if not expanded:
        print_error(ValueError, custom=True, message="The list of packages cannot be empty")
        raise

    return expanded


def parse_package_specs(specs: Sequence[str]) -> List[PackageInput]:
    """Convert the CLI arguments list to PackageInput objects."""
    expanded_specs = _expand_spec_inputs(specs)
    parsed: List[PackageInput] = []
    for spec in expanded_specs:
        if "==" not in spec:
            print_error(ValueError, 
                        custom=True, 
                        message="Each package must be provided in the form name==version")
            raise
        package, version = spec.split("==", 1)
        package = package.strip()
        version = version.strip()
        if not package or not version:
            print_error(ValueError, 
                        custom=True, 
                        message=f"Invalid format for '{spec}': name or version missing")
            raise
        parsed.append(PackageInput(package=package, version=version))

    return parsed


def parse_version(version_str: str) -> Optional[dict]:
    """Parse a version in semver format"""
    match = re.match(r'^(\d+)\.(\d+)\.(\d+)', version_str)
    if not match:
        return None
    return {
        'major': int(match.group(1)),
        'minor': int(match.group(2)),
        'patch': int(match.group(3)),
        'full': version_str
    }


def find_latest_patch(current_version: str, all_versions: List[str]) -> Optional[str]:
    """Find the latest patch compatible version"""
    current = parse_version(current_version)
    if not current:
        return None
    
    compatible_versions = []
    for v in all_versions:
        parsed = parse_version(v)
        if (parsed and 
            parsed['major'] == current['major'] and 
            parsed['minor'] == current['minor'] and 
            parsed['patch'] > current['patch']):
            compatible_versions.append(parsed)
    
    if not compatible_versions:
        return None
    
    # Sort by patch descending and return the first one
    compatible_versions.sort(key=lambda x: x['patch'], reverse=True)
    return compatible_versions[0]['full']


async def check_package(pkg: str, version: str) -> PackageResult:
    """Check a package on PyPI"""
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(
                f"https://pypi.org/pypi/{pkg}/json",
                timeout=10.0
            )
            
            if response.status_code != 200:
                return PackageResult(
                    package=pkg,
                    current_version=version,
                    status="error",
                    message=f"Package not found (code {response.status_code})"
                )
            
            data = response.json()
            all_versions = list(data.get('releases', {}).keys())
            latest_patch = find_latest_patch(version, all_versions)
            
            return PackageResult(
                package=pkg,
                current_version=version,
                latest_patch=latest_patch,
                latest_overall=data['info']['version'],
                status='outdated' if latest_patch else 'up-to-date'
            )
            
        except httpx.TimeoutException:
            return PackageResult(
                package=pkg,
                current_version=version,
                status="error",
                message="Timeout when querying PyPI"
            )
        except Exception as e:
            return PackageResult(
                package=pkg,
                current_version=version,
                status="error",
                message=str(e)
            )


@app.get("/")
async def root():
    return {
        "message": "Requirements Checker API",
        "endpoints": {
            "/check": "POST - Check dependencies",
            "/docs": "Documentation interactive"
        }
    }


async def _check_packages(request_packages: List[PackageInput]) -> List[PackageResult]:
    """Launch the checks on PyPI for the provided list."""
    tasks = [check_package(pkg.package.lower(), pkg.version) for pkg in request_packages]
    return await asyncio.gather(*tasks)


@app.post("/check", response_model=List[PackageResult])
async def check_packages(request: CheckRequest):
    """
    Check a list of packages and return the available updates
    """
    if not request.packages:
        raise HTTPException(status_code=400, detail="Empty package list")

    return await _check_packages(request.packages)


async def check_packages_from_specs(specs: Sequence[str]) -> List[PackageResult]:
    """Utility interface for the command line."""
    packages = parse_package_specs(specs)
    return await _check_packages(packages)


def run_req_to_date(packages: Sequence[str]) -> List[PackageResult]:
    """Synchronous entry point for CLI (standalone or via pocket)."""
    return asyncio.run(check_packages_from_specs(packages))


def print_req_to_date_results(
    results: Sequence[PackageResult],
    printer: Callable[[PackageResult], None],
) -> None:
    """Shared helper to render results for both CLIs.

    The caller provides a small printer callback so that each CLI
    can control its own styling/output mechanism.
    """
    for result in results:
        if result.current_version != result.latest_overall:
            console.print(
                f"{result.package} [red]{result.current_version}[/red] ---> "
                f"[green]{result.latest_overall}[/green]",
                style="bold",
                justify="center",
            )


@click.command(name="req-to-date", context_settings=CONTEXT_SETTINGS)
@click.argument("packages", nargs=-1)
def req_to_date_cli(packages: tuple[str, ...]):
    """Dependencies Scanner: scan dependencies and print outdated dependencies.
    
    Parameters:
    - packages: package names in the form name==version, comma-separated lists of
    name==version, path to a pyproject.toml or a requirements.txt file.
    """
    packages = _expand_spec_inputs(packages)
    count = 0
    try:
        results = run_req_to_date(packages)
    except ValueError as exc:
        print_error(exc, custom=True, message="ValueError")
        raise

    for result in results:
        if result.current_version != result.latest_overall:
            console.print(
                f"{result.package} [red]{result.current_version}[/red] ---> "
                f"[green]{result.latest_overall}[/green]",
                style="bold",
                justify="center",
            )
            count += 1
    if count == 0:
        console.print("\n\n\nEverything's up to date !\n\n\n", style="bold", justify="center")

add_help_command(req_to_date_cli)
