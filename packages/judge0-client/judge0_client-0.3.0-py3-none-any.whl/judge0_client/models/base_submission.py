from abc import ABC, abstractmethod
from typing import Any, Self
from pydantic import BaseModel, Field
from ..utils.base64_utils import base64_encode


class BaseSubmission(BaseModel, ABC):
    """Request model for creating a submission in Judge0."""

    compiler_options: str | None = Field(
        default=None, description="Options for the compiler (i.e. compiler flags)", max_length=512
    )
    command_line_arguments: str | None = Field(
        default=None, description="Command line arguments for the program", max_length=512
    )
    stdin: str | None = Field(default=None, description="Input for program")
    expected_output: str | None = Field(
        default=None, description="Expected output of program. Used when you want to compare with stdout"
    )
    cpu_time_limit: float | None = Field(
        default=None, description="Default runtime limit for every program (seconds)"
    )
    cpu_extra_time: float | None = Field(
        default=None,
        description="When a time limit is exceeded, wait for extra time, before killing the program (seconds)"
    )
    wall_time_limit: float | None = Field(
        default=None, description="Limit wall-clock time in seconds (seconds)"
    )
    memory_limit: float | None = Field(default=None, description="Limit address space of the program (kilobytes)")
    stack_limit: int | None = Field(default=None, description="Limit process stack (kilobytes)")
    max_processes_and_or_threads: int | None = Field(
        default=None, description="Maximum number of processes and/or threads program can create"
    )
    enable_per_process_and_thread_time_limit: bool | None = Field(
        default=None, description="If true then cpu_time_limit will be used as per process and thread"
    )
    enable_per_process_and_thread_memory_limit: bool | None = Field(
        default=None, description="If true then memory_limit will be used as per process and thread"
    )
    max_file_size: int | None = Field(
        default=None, description="Limit file size created or modified by the program (kilobytes)"
    )
    redirect_stderr_to_stdout: bool | None = Field(
        default=None, description="If true standard error will be redirected to standard output"
    )
    enable_network: bool | None = Field(default=None, description="	If true program will have network access")
    number_of_runs: int | None = Field(
        default=None, description="Run each program number_of_runs times and take average of time and memory"
    )
    callback_url: str | None = Field(
        default=None,
        description="URL on which Judge0 will issue PUT request with the submission in a request body after submission has been done"
    )

    @abstractmethod
    def to_body(self) -> dict[str, Any]:
        pass
