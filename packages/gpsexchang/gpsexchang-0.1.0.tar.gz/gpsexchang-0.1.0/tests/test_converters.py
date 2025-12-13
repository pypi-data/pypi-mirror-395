import os
import tempfile
import datetime as dt

from gpsexchang.converters import gpx_to_fit, fit_to_gpx, semicircles_to_degrees, degrees_to_semicircles
from fit_tool.fit_file_builder import FitFileBuilder
from fit_tool.profile.messages.file_id_message import FileIdMessage
from fit_tool.profile.messages.record_message import RecordMessage
from fit_tool.profile.messages.session_message import SessionMessage
from fit_tool.profile.profile_type import FileType, Manufacturer, Sport
from fit_tool.fit_file import FitFile
import gpxpy
import gpxpy.gpx


def _make_sample_gpx() -> str:
    gpx = gpxpy.gpx.GPX()
    gpx.nsmap["gpxtpx"] = "http://www.garmin.com/xmlschemas/TrackPointExtension/v2"
    trk = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(trk)
    seg = gpxpy.gpx.GPXTrackSegment()
    trk.segments.append(seg)
    t0 = dt.datetime.utcnow().replace(microsecond=0)
    pts = [
        (37.7749, -122.4194, 10.0, 100, 2.5),
        (37.7750, -122.4195, 10.5, 101, 2.6),
        (37.7751, -122.4196, 11.0, 102, 2.7),
    ]
    import xml.etree.ElementTree as ET
    for i, (lat, lon, ele, hr, sp) in enumerate(pts):
        p = gpxpy.gpx.GPXTrackPoint(latitude=lat, longitude=lon, elevation=ele, time=t0 + dt.timedelta(seconds=i))
        ext = ET.Element("gpxtpx:TrackPointExtension")
        hr_el = ET.SubElement(ext, "gpxtpx:hr")
        hr_el.text = str(hr)
        sp_el = ET.SubElement(ext, "gpxtpx:speed")
        sp_el.text = str(sp)
        p.extensions = [ext]
        seg.points.append(p)
    return gpx.to_xml()


def test_gpx_to_fit_and_back():
    with tempfile.TemporaryDirectory() as tmp:
        src = os.path.join(tmp, "sample.gpx")
        dst_fit = os.path.join(tmp, "sample.fit")
        dst_gpx = os.path.join(tmp, "roundtrip.gpx")
        with open(src, "w", encoding="utf-8") as f:
            f.write(_make_sample_gpx())
        gpx_to_fit(src, dst_fit)
        ff = FitFile.from_file(dst_fit)
        recs = [r for r in ff.records]
        assert len(recs) >= 3
        fit_to_gpx(dst_fit, dst_gpx)
        with open(dst_gpx, "r", encoding="utf-8") as f:
            parsed = gpxpy.parse(f)
        pts = parsed.tracks[0].segments[0].points
        assert len(pts) >= 3
        assert abs(pts[0].latitude - 37.7749) < 0.001
        assert abs(pts[0].longitude - -122.4194) < 0.001


def test_semicircle_conversion():
    deg = 37.7749
    semi = degrees_to_semicircles(deg)
    back = semicircles_to_degrees(semi)
    assert abs(back - deg) < 1e-6
