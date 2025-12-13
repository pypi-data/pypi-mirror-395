import json
import logging
import re
from enum import Enum
from typing import Annotated, BinaryIO, Iterator, Optional, TextIO, Union

import grpc
import numpy as np
import soundfile as sf
import typer
from google.protobuf.duration_pb2 import Duration
from google.protobuf.json_format import MessageToDict, Parse, ParseError
from google.rpc.error_details_pb2 import BadRequest, ErrorInfo
from grpc_status import rpc_status
from phonexia.grpc.common.core_pb2 import (
    Audio,
    RawAudioConfig,
    TimeRange,
)
from phonexia.grpc.technologies.speech_to_text.v1.speech_to_text_pb2 import (
    ListAllowedSymbolsRequest,
    ListAllowedSymbolsResponse,
    RequestedAdditionalWord,
    ResultType,
    TranscribeConfig,
    TranscribeRequest,
    TranscribeResponse,
)
from phonexia.grpc.technologies.speech_to_text.v1.speech_to_text_pb2_grpc import (
    SpeechToTextStub,
)


class LogLevel(str, Enum):
    CRITICAL = "critical"
    ERROR = "error"
    WARNING = "warning"
    INFO = "info"
    DEBUG = "debug"


class OutputFormat(str, Enum):
    JSON = "json"
    TEXT = "text"


def time_to_duration(time: Optional[float]) -> Optional[Duration]:
    if time is None:
        return None
    duration = Duration()
    duration.seconds = int(time)
    duration.nanos = int((time - duration.seconds) * 1e9)
    return duration


def make_transcribe_request(
    file: BinaryIO,
    start: Optional[float],
    end: Optional[float],
    use_raw_audio: bool,
    preferred_phrases: list[str],
    additional_words: list[RequestedAdditionalWord],
    result_types: list[ResultType],
) -> Iterator[TranscribeRequest]:
    time_range = TimeRange(start=time_to_duration(start), end=time_to_duration(end))
    transcribe_config: TranscribeConfig | None = TranscribeConfig(
        preferred_phrases=preferred_phrases,
        additional_words=additional_words,
        result_types=result_types,
    )
    chunk_size = 1024 * 100
    if use_raw_audio:
        with sf.SoundFile(file) as r:
            raw_audio_config = RawAudioConfig(
                channels=r.channels,
                sample_rate_hertz=r.samplerate,
                encoding=RawAudioConfig.AudioEncoding.PCM16,
            )
            for data in r.blocks(blocksize=r.samplerate, dtype="float32"):
                int16_info = np.iinfo(np.int16)
                data_scaled = np.clip(
                    data * (int16_info.max + 1), int16_info.min, int16_info.max
                ).astype("int16")
                yield TranscribeRequest(
                    audio=Audio(
                        content=data_scaled.flatten().tobytes(),
                        raw_audio_config=raw_audio_config,
                        time_range=time_range,
                    ),
                    config=transcribe_config,
                )
                time_range = None
                raw_audio_config = None
                transcribe_config = None

    else:
        while chunk := file.read(chunk_size):
            yield TranscribeRequest(
                audio=Audio(content=chunk, time_range=time_range), config=transcribe_config
            )
            time_range = None
            transcribe_config = None


def print_json(output_file: TextIO, message: dict) -> None:
    json.dump(message, output_file, indent=2, ensure_ascii=False)


def write_result(
    output_file: TextIO,
    response: Union[TranscribeResponse, ListAllowedSymbolsResponse],
    output_format: OutputFormat = OutputFormat.JSON,
) -> None:
    logging.debug(f"Writing response to '{output_file.name}'")

    if output_format == OutputFormat.JSON:
        print_json(
            output_file,
            MessageToDict(
                response,
                always_print_fields_with_no_presence=True,
                preserving_proto_field_name=True,
            ),
        )
    else:
        if not isinstance(response, TranscribeResponse):
            raise ValueError("Response is not a TranscribeResponse")

        response: TranscribeResponse = response
        if "one_best" not in response.result:
            raise ValueError("The result does not contain 'one_best'")

        for segment in response.result.one_best.segments:
            output_file.write(segment.text + "\n")


def transcribe(
    channel: grpc.Channel,
    file: BinaryIO,
    output: TextIO,
    output_format: OutputFormat,
    preferred_phrases: Optional[TextIO],
    additional_words: Optional[TextIO],
    return_onebest: bool,
    return_nbest: bool,
    return_confusion_network: bool,
    start: Optional[float],
    end: Optional[float],
    use_raw_audio: bool,
    metadata: Optional[list],
) -> None:
    logging.info(f"Transcribing {file.name} -> {output.name}")

    result_types: list[ResultType] = []
    if return_nbest:
        result_types.append(ResultType.RESULT_TYPE_N_BEST)
    if return_confusion_network:
        result_types.append(ResultType.RESULT_TYPE_CONFUSION_NETWORK)
    if return_onebest or len(result_types) == 0:
        result_types.append(ResultType.RESULT_TYPE_ONE_BEST)

    preferred_phrases_list: list[str] = []
    if preferred_phrases is not None:
        preferred_phrases_list = preferred_phrases.read().splitlines()

    additional_words_list: list[RequestedAdditionalWord] = []
    if additional_words is not None:
        transcribe_config: TranscribeConfig = Parse(
            text=additional_words.read(), message=TranscribeConfig()
        )
        additional_words_list = transcribe_config.additional_words

    response_it = make_transcribe_request(
        file=file,
        preferred_phrases=preferred_phrases_list,
        additional_words=additional_words_list,
        result_types=result_types,
        start=start,
        end=end,
        use_raw_audio=use_raw_audio,
    )

    stub = SpeechToTextStub(channel)
    for response in stub.Transcribe(response_it, metadata=metadata):
        write_result(output, response, output_format)


def run_list_allowed_symbols(channel: grpc.Channel, output: TextIO, metadata: Optional[list]):
    logging.info("Listing allowed symbols")
    stub = SpeechToTextStub(channel)
    response: ListAllowedSymbolsResponse = stub.ListAllowedSymbols(
        ListAllowedSymbolsRequest(), metadata=metadata
    )

    write_result(output, response)


def handle_grpc_error(e: grpc.RpcError):
    err_msg = f"gRPC call failed with status code: {e.code()}"

    if e.code() == grpc.StatusCode.UNAVAILABLE:
        err_msg += "\n\nService is unavailable. Please try again later."
    elif e.code() == grpc.StatusCode.INVALID_ARGUMENT:
        err_msg += "\n\nInvalid arguments were provided to the RPC."
    elif e.code() == grpc.StatusCode.DEADLINE_EXCEEDED:
        err_msg += "\n\nThe RPC deadline was exceeded."
    else:
        err_msg += f"\n\nAn unexpected error occurred: {e.code()} - {e.details()}"

    status = rpc_status.from_call(e)
    if status is not None and status.details is not None:
        for detail in status.details:
            if detail.Is(ErrorInfo.DESCRIPTOR):
                info = ErrorInfo()
                detail.Unpack(info)
                err_msg += f"\n\nError info: {info.reason}\n  Domain: {info.domain}"
                if info.metadata:
                    err_msg += "\n  Metadata: {info.metadata}"
            elif detail.Is(BadRequest.DESCRIPTOR):
                info = BadRequest()
                detail.Unpack(info)
                err_msg += "\n\nBad request:\nField violations:\n["
                for fv in info.field_violations:
                    err_msg += f"\n  {{\n    Field: {fv.field}\n    Description: {fv.description}\n    Reason: {fv.reason}\n  }},"
                err_msg += "\n]"
            else:
                err_msg += f"\n\nUnexpected detail: {detail}"

    raise typer.BadParameter(err_msg)


app = typer.Typer(context_settings={"help_option_names": ["-h", "--help"]}, no_args_is_help=True)


def _parse_time_range(time_range: str) -> tuple[Optional[float], Optional[float]]:
    if time_range is None:
        return None, None

    if len(time_range) == 0:
        raise typer.BadParameter("Parameter 'time_range' must be of the form '[START]:[END]'.")

    # Regex pattern to match [START]:[END] format where START and END are positive floats
    pattern = r"^(\d+(?:\.\d+)?)?:(\d+(?:\.\d+)?)?$"
    match = re.match(pattern, time_range.strip())

    if not match:
        raise typer.BadParameter(
            "Parameter 'time_range' must be of the form '[START]:[END]' where START and END are positive float numbers."
        )

    # Parse START and END from regex groups
    start_str = match.group(1)
    end_str = match.group(2)

    start = float(start_str) if start_str is not None else None
    end = float(end_str) if end_str is not None else None

    if start is not None and end is not None and start >= end:
        raise typer.BadParameter("Parameter 'end' must be larger than 'start'.")

    return (None if start == 0.0 else start, end)


def _parse_metadata_callback(
    ctx: typer.Context, metadata_list: Optional[list[str]]
) -> list[tuple[str, str]]:
    if ctx.resilient_parsing or metadata_list is None:
        return []

    params = []
    for item in metadata_list:
        t = tuple(item.split("=", 1))
        if len(t) != 2:
            raise typer.BadParameter(f"Metadata must be in format 'KEY=VALUE': {item}")
        params.append(t)
    return params


@app.command()
def cli(
    # file must be None by default because ListAllowedSymbols does not require an input file
    file: Annotated[
        Optional[typer.FileBinaryRead],
        typer.Argument(
            help="Input audio file. '-' to read audio bytes from standard input.", lazy=False
        ),
    ] = None,
    output: Annotated[
        typer.FileTextWrite,
        typer.Option(
            "--output", "-o", help="Output file path. If omitted, prints to stdout.", lazy=False
        ),
    ] = "-",
    output_format: Annotated[
        OutputFormat,
        typer.Option(
            "-f",
            "--out-format",
            help="Forced output format.",
        ),
    ] = OutputFormat.JSON,
    preferred_phrases: Annotated[
        Optional[typer.FileText],
        typer.Option(
            "-p",
            "--preferred-phrases",
            help="Path to a file containing a list of preferred phrases, each on its separate line.",
            lazy=False,
        ),
    ] = None,
    additional_words: Annotated[
        Optional[typer.FileText],
        typer.Option(
            "-a",
            "--additional-words",
            help="Path to a file containing a list of words to be added to the transcription dictionary. "
            "You can generate reference list by running this client with '--example-additional-words' argument.",
            lazy=False,
        ),
    ] = None,
    list_allowed_symbols: Annotated[
        bool,
        typer.Option(
            "--list-allowed-symbols",
            is_flag=True,
            help="List graphemes and phonemes allowed for new words.",
        ),
    ] = False,
    return_onebest: Annotated[
        bool,
        typer.Option(
            "--return-onebest",
            is_flag=True,
            help="Return onebest transcription result. If no result types are specified, onebest is returned by default.",
        ),
    ] = False,
    return_nbest: Annotated[
        bool,
        typer.Option(
            "--return-nbest",
            is_flag=True,
            help="Return nbest transcription result.",
        ),
    ] = False,
    return_confusion_network: Annotated[
        bool,
        typer.Option(
            "--return-confusion-network",
            is_flag=True,
            help="Return confusion network transcription result.",
        ),
    ] = False,
    example_additional_words: Annotated[
        bool,
        typer.Option(
            "--example-additional-words",
            is_flag=True,
            help="Generate example additional words list.",
        ),
    ] = False,
    host: Annotated[
        str,
        typer.Option("--host", "-H", help="Server address (host:port)."),
    ] = "localhost:8080",
    log_level: Annotated[
        LogLevel, typer.Option("--log-level", "-l", help="Logging level.")
    ] = LogLevel.ERROR,
    metadata: Annotated[
        Optional[list[str]],
        typer.Option(
            "--metadata",
            metavar="KEY=VALUE",
            help="Custom client metadata.",
            show_default=False,
            callback=_parse_metadata_callback,
        ),
    ] = None,
    plaintext: Annotated[
        bool,
        typer.Option(
            "--plaintext", help="Use plain-text HTTP/2 when connecting to server (no TLS)."
        ),
    ] = False,
    time_range: Annotated[
        Optional[str],
        typer.Option(
            "-t",
            "--time-range",
            callback=_parse_time_range,
            metavar="[START]:[END]",
            help=(
                "Time range in seconds using format [START]:[END] where START and END are positive float numbers. "
                "START can be omitted to process from beginning, END can be omitted to process to the end of the recording. "
                "Examples: --time-range :10 (0 to 10), --time-range 10.1: (10.1 to end), --time-range 5:10 (5 to 10)."
            ),
        ),
    ] = None,
    use_raw_audio: Annotated[
        bool,
        typer.Option(
            "--use-raw-audio",
            help="Send raw audio in chunks. Enables continuous audio processing with less server memory usage.",
            is_flag=True,
        ),
    ] = False,
) -> None:
    """Transcribe speech to text from an input audio file or standard input."""

    logging.basicConfig(
        level=log_level.value.upper(),
        format="[%(asctime)s.%(msecs)03d] [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    try:
        logging.info(f"Connecting to {host}")
        with (
            grpc.insecure_channel(target=host)
            if plaintext
            else grpc.secure_channel(target=host, credentials=grpc.ssl_channel_credentials())
        ) as channel:
            if list_allowed_symbols:
                run_list_allowed_symbols(
                    channel=channel,
                    output=output,
                    metadata=metadata,
                )

            elif example_additional_words:
                additional_words = {
                    "additional_words": [
                        {
                            "spelling": "frumious",
                            "pronunciations": ["f r u m i o s", "f r u m i u s"],
                        },
                        {
                            "spelling": "flibbertigibbet",
                            "pronunciations": [
                                "f l i b r t i j i b i t",
                                "f l i b r t i j i b e t",
                            ],
                        },
                    ]
                }
                print_json(output, additional_words)

            else:
                if not file:
                    raise typer.BadParameter(  # noqa: TRY301
                        "Input file must be specified when transcribing."
                    )

                if not (return_onebest or return_nbest or return_confusion_network):
                    return_onebest = True

                transcribe(
                    channel=channel,
                    file=file,
                    output=output,
                    output_format=output_format,
                    preferred_phrases=preferred_phrases,
                    additional_words=additional_words,
                    return_onebest=return_onebest,
                    return_nbest=return_nbest,
                    return_confusion_network=return_confusion_network,
                    start=time_range[0],
                    end=time_range[1],
                    use_raw_audio=use_raw_audio,
                    metadata=metadata,
                )

    except grpc.RpcError as e:
        handle_grpc_error(e)
        raise typer.Exit(code=1) from None
    except ParseError as e:
        logging.error(f"Error while parsing additional words list: {e}")  # noqa: TRY400
        raise typer.Exit(code=1) from None
    except ValueError as e:
        logging.error(f"Error while writing result: {e}")  # noqa: TRY400
        raise typer.Exit(code=1) from None
    except (typer.Exit, typer.BadParameter):
        raise
    except Exception:
        logging.exception("Unknown error")
        raise typer.Exit(code=1) from None


if __name__ == "__main__":
    app()
