from contextlib import suppress
from enum import Enum
from inspect import isfunction
import random
import string
import typing
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Tuple,
    Type,
    TypedDict,
    Union,
    cast,
)

from nightskyrunner.status import RunnerStatusDict, StatusDict

from .fix import deserialize_fix_dict, serialize_fix_dict
from .serialize import deserialize, serialize

# --- dev notes ---
#
# The following conventions have to be enforced:
# Subclasses of RunnerStatusDict *must* be named
# {runner class name}Entries (e.g. CommandRunnerEntries)
#
# report class (which "cast" an instance of RunnerStatusDict
# to Dict[str,str], *must* be named:
# get_{runner class name}_report
#


NightskycamRunner = Literal[
    "CamRunner",
    "AsiCamRunner",
    "USBCamRunner",
    "ImageProcessRunner",
    "SpaceKeeperRunner",
    "FtpRunner",
    "LocationInfoRunner",
    "SleepyPiRunner",
    "CommandRunner",
    "StatusRunner",
    "ConfigRunner",
    "ApertureRunner",
]
"""The list of runner classes defined and used by nightskycam"""


class RunnerClasses(Enum):
    """
    Enumerating all known runner classes
    """

    # dev note: there is a unit test checking
    # there is no mismatch with NightskycamRunner
    # right above
    CamRunner = "CamRunner"
    AsiCamRunner = "AsiCamRunner"
    USBCamRunner = "USBCamRunner"
    CommandRunner = "CommandRunner"
    FtpRunner = "FtpRunner"
    LocationInfoRunner = "LocationInfoRunner"
    ImageProcessRunner = "ImageProcessRunner"
    SleepyPiRunner = "SleepyPiRunner"
    SpaceKeeperRunner = "SpaceKeeperRunner"
    ConfigRunner = "ConfigRunner"
    StatusRunner = "StatusRunner"
    ApertureRunner = "ApertureRunner"


def serialize_status(
    system: str, status: Iterable[StatusDict], token: Optional[str] = None
) -> str:
    """
    Serialize the dictionary with the keys "system" and "status".

    Arguments
      system: the name of the nightskycam system
      status: the status dictionary to serialize
      token: the shared secret

    Counterpart: [deserialize_status]().

    See: [serialize.serialize]()
    """
    d: Dict[str, Union[str, Dict[str, StatusDict]]] = {"system": system}
    status_d: Dict[str, StatusDict] = {
        s["name"]: serialize_fix_dict(s) for s in status
    }
    d["status"] = status_d
    return serialize(d, token=token)


def deserialize_status(
    message: str, token: Optional[str] = None
) -> Tuple[str, Dict[str, Dict[str, Any]]]:
    """
    Deserialize the message sent by a system, containing the status information
    related to all runners executed on the system.

    Returns:
      The name of the system
      The status dictionary for each runner (name of the runner as key)

    Counterpart: [serialize_status]().

    See: [serialize.deserialize]()
    """
    d = deserialize(message, required_keys=("system", "status"), token=token)
    system = d["system"]
    all_status = {
        runner_name: deserialize_fix_dict(status)
        for runner_name, status in d["status"].items()
    }
    return system, all_status


class CamRunnerEntries(RunnerStatusDict, total=False):
    """
    For serializing the status of nightskycam CamRunner
    """

    time_window: str
    use_sun_alt: bool
    use_weather: bool
    active: str
    picture: str
    number_of_pictures_taken: int
    latest_picture: str
    camera_info: Dict[str, str]
    pause: bool


class AsiCamRunnerEntries(RunnerStatusDict, total=False):
    """
    For serializing the status of nightskycam AsiCamRunner
    """

    time_window: str
    use_sun_alt: bool
    use_weather: bool
    active: str
    picture: str
    number_of_pictures_taken: int
    latest_picture: str
    camera_info: Dict[str, str]
    pause: bool


class USBCamRunnerEntries(RunnerStatusDict, total=False):
    """
    For serializing the status of nightskycam USBCamRunner
    """

    time_window: str
    use_sun_alt: bool
    use_weather: bool
    active: str
    picture: str
    number_of_pictures_taken: int
    latest_picture: str
    camera_info: Dict[str, str]
    pause: bool


def get_CamRunner_report(
    sc: CamRunnerEntries, camera_type: str = "camera"
) -> Dict[str, str]:
    """
    Returns a summary of selected information
    """
    entries: Dict[str, str] = {}

    pause = sc.get("pause", False)
    if pause:
        return {camera_type: "paused - restart to reactivate"}

    active = sc.get("active", None)
    entries["active"] = active if active else "unspecified"

    usa = sc.get("use_sun_alt", None)
    entries["use sun altitude"] = "yes" if usa else "no"

    uw = sc.get("use_weather", None)
    entries["use weather"] = "yes" if uw else "no"

    camera_temperature = sc.get("camera_info", {}).get(
        "camera_temperature", None
    )
    entries["camera temperature"] = str(camera_temperature) if camera_temperature is not None else "unknown"

    num_pics = sc.get(
        "number_of_pictures_taken", None
    )
    entries["number of pictures taken (since boot)"] = str(num_pics) if num_pics is not None else "unknown"

    r = "\n".join(f"{k}: {v}" for k, v in entries.items() if v is not None)

    return {camera_type: r}


def get_AsiCamRunner_report(sc: AsiCamRunnerEntries) -> Dict[str, str]:
    return get_CamRunner_report(sc, "ASI camera")


def get_USBCamRunner_report(sc: USBCamRunnerEntries) -> Dict[str, str]:
    return get_CamRunner_report(sc, "USB camera")


class ApertureRunnerEntries(RunnerStatusDict, total=False):
    """
    For serializing the status of nightskycam ApertureRunner
    """

    use: bool
    focus: int
    status: str
    reason: str
    use_zwo_camera: bool
    time_window: str
    pause: bool


def get_ApertureRunner_report(sc: ApertureRunnerEntries) -> Dict[str, str]:
    """
    Returns a summary of selected information
    """
    pause = sc.get("pause", False)
    if pause:
        return {"aperture": "paused - restart to reactivate"}

    if not sc["use"]:
        return {"aperture": "used: no"}
    r: Dict[str, str] = {}
    try:
        focus = sc["focus"]
        r["focus"] = str(focus) if focus is not None else "unknown"
    except KeyError:
        r["focus"] = "not set"
    r["status"] = f"{sc['status']} ({sc['reason']})"
    r["using camera activity"] = "yes" if sc["use_zwo_camera"] else "no"
    if not sc["use_zwo_camera"]:
        r["time window"] = sc["time_window"]
    r["focus"] = str(sc["focus"])
    return {"aperture": "\n".join([f"{k}: {v}" for k, v in r.items()])}


class CommandRunnerEntries(RunnerStatusDict, total=False):
    """
    For serializing the status of nightskycam CommandRunner
    """

    queued_commands: List[int]
    active_command: str
    executed_commands: List[int]


def get_CommandRunner_report(sc: CommandRunnerEntries) -> Dict[str, str]:
    """
    Returns a summary of selected information
    """
    try:
        return {"running command": str(sc["active_command"])}
    except KeyError:
        return {}


class FtpRunnerEntries(RunnerStatusDict, total=False):
    """
    For serializing the status of nightskycam FtpRunner
    """

    uploading: bool
    number_uploaded_files: str
    total_uploaded_files: str
    upload_speed: float
    files_to_upload: str
    latest_uploaded: str


def get_FtpRunner_report(sf: FtpRunnerEntries) -> Dict[str, str]:
    """
    Returns a summary of selected information
    """
    ftp_infos: List[str] = []
    with suppress(KeyError):
        uploading = sf["uploading"]
        if uploading:
            ftp_infos.append("currently uploading: yes")
        else:
            ftp_infos.append("currently uploading: no")
    with suppress(KeyError):
        ftp_infos.append(
            str(
                f"uploaded files: "
                f"{sf['number_uploaded_files']} file(s)"
                f" ({sf['total_uploaded_files']})"
            )
        )
    with suppress(KeyError):
        ftu = sf["files_to_upload"]
        if ftu:
            ftp_infos.append("files to upload: " + str(ftu))
        else:
            ftp_infos.append("no file to upload")
    if not ftp_infos:
        return {}
    return {"ftp": "\n".join(ftp_infos)}


class LocationInfoRunnerEntries(RunnerStatusDict, total=False):
    """
    For serializing the status of nightskycam LocationInfoRunner
    """

    latitude: float
    longitude: float
    name: str
    country: str
    timezone: str
    IPs: str
    local_time: str
    sun_alt: float
    sun_alt_threshold: float
    night: bool
    cloud_cover: int
    weather: str
    temperature: int
    time_stamp: float
    cpu_temperature: int


def get_LocationInfoRunner_report(
    li: LocationInfoRunnerEntries,
) -> Dict[str, str]:
    """
    Returns a summary of selected information
    """

    r: Dict[str, str] = {}
    local_info: Dict[str, str] = {}
    with suppress(KeyError):
        local_info["local time"] = li["local_time"]
    with suppress(KeyError):
        local_info["sun altitude"] = str(
            f"{li['sun_alt']:.2f} "
            f"(threshold: {li['sun_alt_threshold']:.2f})"
        )
    with suppress(KeyError):
        local_info["weather"] = str(
            f"{li['weather']} (cloud cover: {li['cloud_cover']})"
        )
    if local_info:
        r["local info"] = "\n".join(
            [f"{k}: {v}" for k, v in local_info.items()]
        )
    with suppress(KeyError):
        r["IP(s)"] = li["IPs"]

    return r


class ImageProcessRunnerEntries(RunnerStatusDict, total=False):
    """
    For serializing the status of nightskycam ProcessRunner
    """

    number_of_processed_pictures: int
    processes_applied: List[str]
    file_format: str
    last_processed_picture: str


def get_ImageProcessRunner_report(
    sp: ImageProcessRunnerEntries,
) -> Dict[str, str]:
    """
    Returns a summary of selected information
    """
    processes_applied = sp.get("processes_applied", "")
    processes_applied_str = (
        f"{processes_applied}, " if processes_applied else ""
    )
    try:
        return {
            "image process": str(
                f"{sp['number_of_processed_pictures']} image(s) processed "
                f"({processes_applied_str}format: {sp['file_format']})"
            )
        }
    except KeyError:
        return {}


class SleepyPiRunnerEntries(RunnerStatusDict, total=False):
    """
    For serializing the status of nightskycam SleepyPiRunner
    """

    configured_to_sleep: bool
    start_sleep: str
    stop_sleep: str
    wait_for_ftp: bool
    status: str


def get_SleepyPiRunner_report(sp: SleepyPiRunnerEntries) -> Dict[str, str]:
    """
    Returns a summary of selected information
    """
    cs = sp.get("configured_to_sleep", False)
    if not cs:
        return {"sleep mode": "no"}
    else:
        with suppress(KeyError):
            return {
                "sleep mode": f"from {sp['start_sleep']} to {sp['stop_sleep']}\n{sp['status']}"
            }
    return {}


class SpaceKeeperRunnerEntries(RunnerStatusDict, total=False):
    """
    For serializing the status of nightskycam SpaceKeeperRunner
    """

    folder: str
    disk: str
    threshold: str
    deleting: bool
    free_space: float


def get_SpaceKeeperRunner_report(
    sk: SpaceKeeperRunnerEntries,
) -> Dict[str, str]:
    """
    Returns a summary of selected information
    """
    disk = sk["disk"]
    deleting = (
        f"*deleting older files (threshold={sk['threshold']})*"
        if sk["deleting"]
        else None
    )
    return {"disk": "\n".join([s for s in (disk, deleting) if s])}


class StatusRunnerEntries(RunnerStatusDict, total=False):
    """
    For serializing the status of nightskycam StatusRunner
    """

    update: str


class ConfigRunnerEntries(RunnerStatusDict, total=False):
    """
    For serializing the status of nightskycam ConfigUpdateRunner
    """

    updates: Dict[str, str]


def has_runner_status_dict(runner_class_name: str) -> bool:
    """
    Returns True if the runner class has a corresponding implementation
    of RunnerStatusDict, False otherwise.
    """
    class_name = f"{runner_class_name}Entries"
    try:
        globals()[class_name]
        return True
    except KeyError:
        return False


def has_status_entries_report_function(runner_class_name: str) -> bool:
    """
    Returns True if the runner class has a corresponding implementation
    of "get_report" function, False otherwise.
    """
    fn: Callable[[RunnerStatusDict], Dict[str, str]]
    fn_name = f"get_{runner_class_name}_report"
    try:
        fn = globals()[fn_name]
    except KeyError:
        return False
    return isfunction(fn)


def get_runner_status_dict_class(
    runner_class_name: str,
) -> Type[RunnerStatusDict]:
    """
    Returns the corresponding subclass of RunnerStatusDict, assuming
    it is defined in this module and named '{runner class name}Entries'
    """
    try:
        return globals()[f"{runner_class_name}Entries"]
    except KeyError:
        raise TypeError(
            f"Not sublcass of RunnerStatusDict has been implemented for runner {runner_class_name}"
        )


def get_random_status_dict(runner_class_name: str) -> RunnerStatusDict:
    """
    Arguments
      The name of a nightskycam runner class.

    Returns
      An instance of the subclass of RunnerStatusDict corresponding
      to the class name passed as argument.

    Raises
      TypeError if there is no instance of RunnerStatusDict corresponding
      to the class name passed as argument.
    """

    def get_random_int(min_value: int = 0, max_value: int = 20) -> int:
        return random.randint(min_value, max_value)

    def get_random_int_list() -> List[int]:
        return [get_random_int() for _ in range(get_random_int())]

    def get_random_float(
        min_value: float = 0.0, max_value: float = 1.0
    ) -> float:
        return round(random.uniform(min_value, max_value), 2)

    def get_random_bool() -> bool:
        return random.choice([True, False])

    def get_random_str(length: int = 10) -> str:
        return "".join(
            random.choices(string.ascii_letters + string.digits, k=length)
        )

    def get_random_str_list() -> List[str]:
        return [get_random_str() for _ in range(get_random_int())]

    def get_random_dict():
        return {get_random_str(): get_random_str() for _ in range(5)}

    random_fn = {
        int: get_random_int,
        float: get_random_float,
        bool: get_random_bool,
        str: get_random_str,
        typing.Dict[str, str]: get_random_dict,
        typing.List[int]: get_random_int_list,
        typing.List[str]: get_random_str_list,
    }

    runner_dict_class = get_runner_status_dict_class(runner_class_name)
    fields = runner_dict_class.__annotations__
    kwargs = {}
    for field, t in fields.items():
        kwargs[field] = random_fn[t]()  # type: ignore
    return runner_dict_class(**kwargs)


def get_status_entries_report(
    all_status: Dict[str, RunnerStatusDict],  # runner class name: entries
) -> Dict[str, str]:
    """
    Returns a summary reports for all status for which
    a corresponding report function has been implemented using the
    name 'get_{runner_class_name}_report'.

    Arguments
      all_status: key: the runner name, value: the corresponding
        entries dictionary
    """

    def _get_function(
        runner_class_name: str,
    ) -> Callable[[RunnerStatusDict], Dict[str, str]]:
        function_name = f"get_{runner_class_name}_report"
        try:
            return globals()[function_name]
        except KeyError:
            return lambda _: {}

    r: Dict[str, str] = {}

    for runner_name, entries in all_status.items():
        if entries:
            report_fn = _get_function(runner_name)
            report = report_fn(entries)
            for k, v in report.items():
                r[k] = v
    return r


class IntrospectionDict(TypedDict, total=False):
    """
    TypedDict which keys correspond to the
    Introspection django model
    (package nightskycam-server)
    """

    cpu_temperature: int
    camera_temperature: int
    camera_target_temperature: int
    outside_temperature: int
    cooler_on: bool
    upload_speed: float
    free_space: float


def get_introspection_dict(
    status: Dict[str, RunnerStatusDict]
) -> IntrospectionDict:
    """
    Casting to IntrospectionDict
    """
    intro_dict = IntrospectionDict()
    for runner_class, status_dict in status.items():
        if runner_class == RunnerClasses.AsiCamRunner.value:
            cr = cast(CamRunnerEntries, status_dict)
            for key in (
                "camera_temperature",
                "camera_target_temperature",
                "cooler_on",
            ):
                with suppress(KeyError):
                    value = cr["camera_info"][key]
                    intro_dict[key] = value  # type: ignore

        elif runner_class == RunnerClasses.LocationInfoRunner.value:
            lir = cast(LocationInfoRunnerEntries, status_dict)
            with suppress(KeyError):
                cpu = lir["cpu_temperature"]
                intro_dict["cpu_temperature"] = cpu
            with suppress(KeyError):
                outside = lir["temperature"]
                intro_dict["outside_temperature"] = outside

        elif runner_class == RunnerClasses.FtpRunner.value:
            fr = cast(FtpRunnerEntries, status_dict)
            with suppress(KeyError):
                up = fr["upload_speed"]
                intro_dict["upload_speed"] = up

        elif runner_class == RunnerClasses.SpaceKeeperRunner.value:
            skr = cast(SpaceKeeperRunnerEntries, status_dict)
            with suppress(KeyError):
                free = skr["free_space"]
                intro_dict["free_space"] = free

    return intro_dict
