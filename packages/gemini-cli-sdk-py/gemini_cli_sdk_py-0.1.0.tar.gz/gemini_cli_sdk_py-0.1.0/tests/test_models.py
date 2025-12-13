import json

from gemini_cli_sdk import HeadlessResponse, parse_stream_event_json


def test_headless_response_validation() -> None:
    payload = {
        "response": "The capital of France is Paris.",
        "stats": {
            "models": {
                "gemini-2.5-pro": {
                    "api": {"totalRequests": 2, "totalErrors": 0, "totalLatencyMs": 5053},
                    "tokens": {
                        "prompt": 24939,
                        "candidates": 20,
                        "total": 25113,
                        "cached": 21263,
                        "thoughts": 154,
                        "tool": 0,
                    },
                }
            },
            "tools": {
                "bash": {
                    "count": 1,
                    "success": 1,
                    "fail": 0,
                    "durationMs": 1881,
                    "decisions": {"accept": 0, "reject": 0, "modify": 0, "auto_accept": 1},
                }
            },
            "files": {"totalLinesAdded": 0, "totalLinesRemoved": 0},
        },
    }
    parsed = HeadlessResponse.model_validate(payload)
    assert parsed.response.startswith("The capital")
    assert "gemini-2.5-pro" in parsed.stats.models


def test_stream_event_parsing() -> None:
    line = json.dumps(
        {
            "type": "message",
            "role": "assistant",
            "content": "Here are the files...",
            "delta": True,
            "timestamp": "2025-10-10T12:00:04.000Z",
        }
    )
    ev = parse_stream_event_json(line)
    assert ev.type == "message"
