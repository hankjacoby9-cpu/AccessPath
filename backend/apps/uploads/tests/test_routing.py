from apps.uploads.routing import route_for


def test_routing():
    assert route_for("PDF") == "markitdown"
    assert route_for(".pptx") == "markitdown"
    assert route_for("png") == "image"
    assert route_for("mp4") == "audio_video"
    assert route_for("exe") == "reject"
