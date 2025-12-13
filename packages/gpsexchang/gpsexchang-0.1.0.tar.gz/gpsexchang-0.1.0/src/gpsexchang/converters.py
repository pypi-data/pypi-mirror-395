import os
import math
import datetime as dt
from typing import List, Optional, Tuple

import gpxpy
import gpxpy.gpx
from fit_tool.fit_file_builder import FitFileBuilder
from fit_tool.profile.messages.file_id_message import FileIdMessage
from fit_tool.profile.messages.session_message import SessionMessage
from fit_tool.profile.messages.lap_message import LapMessage
from fit_tool.profile.messages.record_message import RecordMessage
from fit_tool.profile.profile_type import FileType, Manufacturer, Sport
import fitparse


def semicircles_to_degrees(value: int) -> float:
    return float(value) * 180.0 / (2**31)


def degrees_to_semicircles(value: float) -> int:
    return int(round(float(value) * (2**31) / 180.0))


def haversine_m(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    R = 6371000.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


class TrackPoint:
    def __init__(self, lat: float, lon: float, ele: Optional[float], time: Optional[dt.datetime], hr: Optional[int], speed: Optional[float]):
        self.lat = lat
        self.lon = lon
        self.ele = ele
        self.time = time
        self.hr = hr
        self.speed = speed


def _parse_gpx_points(path: str) -> List[TrackPoint]:
    with open(path, "r", encoding="utf-8") as f:
        gpx = gpxpy.parse(f)
    points: List[TrackPoint] = []
    for track in gpx.tracks:
        for segment in track.segments:
            for p in segment.points:
                hr = None
                speed = None
                if p.extensions:
                    for ext in p.extensions:
                        for child in ext:
                            tag = child.tag.lower()
                            if tag.endswith("hr"):
                                try:
                                    hr = int(float(child.text))
                                except Exception:
                                    hr = None
                            if tag.endswith("speed"):
                                try:
                                    speed = float(child.text)
                                except Exception:
                                    speed = None
                points.append(TrackPoint(p.latitude, p.longitude, p.elevation, p.time, hr, speed))
    for i in range(1, len(points)):
        a = points[i - 1]
        b = points[i]
        if b.speed is None and a.time and b.time:
            dt_s = (b.time - a.time).total_seconds()
            if dt_s > 0:
                d_m = haversine_m(a.lat, a.lon, b.lat, b.lon)
                b.speed = d_m / dt_s
    return points


def gpx_to_fit(source_path: str, dest_path: str, sport: Sport = Sport.RUNNING) -> None:
    points = _parse_gpx_points(source_path)
    if not points:
        raise ValueError("No GPX track points found")
    start_time = points[0].time or dt.datetime.utcnow()
    start_ms = round(start_time.timestamp() * 1000)
    file_id = FileIdMessage()
    file_id.type = FileType.ACTIVITY
    file_id.manufacturer = Manufacturer.DEVELOPMENT.value
    file_id.product = 0
    file_id.time_created = start_ms
    session = SessionMessage()
    session.sport = sport
    session.sub_sport = sport.value
    session.start_time = start_ms
    lap = LapMessage()
    lap.start_time = start_ms
    builder = FitFileBuilder(auto_define=True, min_string_size=50)
    builder.add(file_id)
    builder.add(session)
    builder.add(lap)
    distance = 0.0
    last: Optional[TrackPoint] = None
    for tp in points:
        msg = RecordMessage()
        if tp.time:
            msg.timestamp = round(tp.time.timestamp() * 1000)
        msg.position_lat = float(tp.lat)
        msg.position_long = float(tp.lon)
        if tp.ele is not None:
            msg.altitude = float(tp.ele)
            msg.enhanced_altitude = float(tp.ele)
        if tp.speed is not None:
            msg.speed = float(tp.speed)
            msg.enhanced_speed = float(tp.speed)
        if tp.hr is not None:
            msg.heart_rate = int(tp.hr)
        if last:
            distance += haversine_m(last.lat, last.lon, tp.lat, tp.lon)
            msg.distance = distance
        builder.add(msg)
        last = tp
    fit_file = builder.build()
    fit_file.to_file(dest_path)


def fit_to_gpx(source_path: str, dest_path: str) -> None:
    fitfile = fitparse.FitFile(source_path, data_processor=fitparse.StandardUnitsDataProcessor())
    gpx = gpxpy.gpx.GPX()
    gpx.nsmap["gpxtpx"] = "http://www.garmin.com/xmlschemas/TrackPointExtension/v2"
    track = gpxpy.gpx.GPXTrack()
    gpx.tracks.append(track)
    segment = gpxpy.gpx.GPXTrackSegment()
    track.segments.append(segment)
    for record in fitfile.get_messages("record"):
        fields = {d.name: d.value for d in record}
        lat = fields.get("position_lat")
        lon = fields.get("position_long")
        if lat is None or lon is None:
            continue
        if isinstance(lat, int):
            lat_deg = semicircles_to_degrees(lat)
            lon_deg = semicircles_to_degrees(lon)
        else:
            lat_deg = float(lat)
            lon_deg = float(lon)
        ele = fields.get("enhanced_altitude") or fields.get("altitude")
        speed = fields.get("enhanced_speed") or fields.get("speed")
        hr = fields.get("heart_rate")
        ts = fields.get("timestamp")
        point = gpxpy.gpx.GPXTrackPoint(latitude=lat_deg, longitude=lon_deg, elevation=float(ele) if ele is not None else None, time=ts if isinstance(ts, dt.datetime) else None)
        exts = []
        if hr is not None or speed is not None:
            ns = "gpxtpx"
            import xml.etree.ElementTree as ET
            tpe = ET.Element(f"{ns}:TrackPointExtension")
            if hr is not None:
                hr_el = ET.SubElement(tpe, f"{ns}:hr")
                hr_el.text = str(int(hr))
            if speed is not None:
                sp_el = ET.SubElement(tpe, f"{ns}:speed")
                sp_el.text = str(float(speed))
            exts.append(tpe)
        point.extensions = exts if exts else None
        segment.points.append(point)
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(gpx.to_xml())


def convert(source_path: str, source_fmt: str, dest_fmt: str, dest_path: Optional[str] = None) -> str:
    source_fmt = source_fmt.lower()
    dest_fmt = dest_fmt.lower()
    if dest_path is None:
        base = os.path.splitext(os.path.basename(source_path))[0]
        dest_path = os.path.join(os.path.dirname(source_path), f"{base}.{dest_fmt}")
    if source_fmt == "gpx" and dest_fmt == "fit":
        gpx_to_fit(source_path, dest_path)
    elif source_fmt == "fit" and dest_fmt == "gpx":
        fit_to_gpx(source_path, dest_path)
    else:
        raise ValueError("Unsupported conversion")
    return dest_path
