from gemini_cli_sdk import OutputFormat, RunOptions


def test_run_options_to_argv_basic() -> None:
    opts = RunOptions(
        model="gemini-2.5-pro",
        prompt="hi",
        output_format=OutputFormat.JSON,
        yolo=True,
        include_directories=["a", "b"],
        extensions=["ext1", "ext2"],
        resume=1,
    )
    argv = opts.to_argv()

    assert "--model" in argv
    assert "--prompt" in argv
    assert ["--output-format", "json"] in [argv[i : i + 2] for i in range(len(argv) - 1)]
    assert "--yolo" in argv
    assert argv.count("--include-directories") == 2
    assert argv.count("--extensions") == 2
    assert ["--resume", "1"] in [argv[i : i + 2] for i in range(len(argv) - 1)]
