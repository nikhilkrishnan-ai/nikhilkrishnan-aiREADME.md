import json
import math
import argparse
import sys
import apache_beam as beam
from apache_beam.options.pipeline_options import PipelineOptions
from datetime import datetime

# Handle unicode encoding for Windows console
sys.stdout.reconfigure(encoding='utf-8')

def parse_coords(point_str):
    """Parse coordinates from format: '24.3198761°, 54.5381226°'"""
    point_str = point_str.replace('Â°', '°').replace('Â', '').replace('', '')
    parts = point_str.split('°, ')
    if len(parts) == 1 and '°' not in point_str:
        parts = point_str.split(', ')
    lat = float(parts[0].replace('°', ''))
    lon = float(parts[1].replace('°', '').strip())
    return (lat, lon)

def haversine_distance(coord1, coord2):
    """Calculate distance between two GPS coordinates in kilometers"""
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    R = 6371  # Earth radius in km
    phi1 = math.radians(lat1)
    phi2 = math.radians(lat2)
    delta_phi = math.radians(lat2 - lat1)
    delta_lambda = math.radians(lon2 - lon1)
    a = math.sin(delta_phi/2) ** 2 + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def time_diff_minutes(time1, time2):
    t1 = datetime.strptime(time1[11:19], '%H:%M:%S')
    t2 = datetime.strptime(time2[11:19], '%H:%M:%S')
    return abs((t2 - t1).total_seconds() / 60)

class ExtractPathPairsFn(beam.DoFn):
    def process(self, entry):
        # Entry is a dictionary representing one timeline block
        points = entry.get('timelinePath', [])
        # We need consecutive pairs
        for i in range(len(points) - 1):
            yield (entry['startTime'], points[i], points[i+1])

class DetectAnomaliesFn(beam.DoFn):
    def process(self, element):
        start_time, current_point, next_point = element
        
        current_coords = parse_coords(current_point['point'])
        next_coords = parse_coords(next_point['point'])
        
        distance_km = haversine_distance(current_coords, next_coords)
        distance_m = distance_km * 1000
        
        time_minutes = time_diff_minutes(current_point['time'], next_point['time'])
        velocity_kmh = 0
        if time_minutes > 0:
            velocity_kmh = (distance_km / time_minutes) * 60
            
        # Spoofing indicators: jump > 50 meters
        if distance_m > 50:
            yield {
                'from_time': current_point['time'][11:19],
                'to_time': next_point['time'][11:19],
                'distance_m': round(distance_m, 2),
                'velocity_kmh': round(velocity_kmh, 2),
                'from_point': current_point['point'],
                'to_point': next_point['point']
            }

def run(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='input', default='Timelineapril7.json', help='Input JSON file')
    parser.add_argument('--output', dest='output', default='dataflow_anomalies_output', help='Output file prefix')
    known_args, pipeline_args = parser.parse_known_args(argv)

    # Naming the pipeline "GeoSense By NK" as requested
    pipeline_options = PipelineOptions(pipeline_args, job_name='geosense-by-nk')

    with open(known_args.input, 'r', encoding='utf-8') as f:
        timeline_data = json.load(f)

    with beam.Pipeline(options=pipeline_options) as p:
        anomalies = (
            p
            | 'ReadData' >> beam.Create(timeline_data)
            | 'ExtractPairs' >> beam.ParDo(ExtractPathPairsFn())
            | 'DetectAnomalies' >> beam.ParDo(DetectAnomaliesFn())
        )
        
        # Write to JSON Lines
        (anomalies 
         | 'FormatJSON' >> beam.Map(json.dumps)
         | 'WriteOutput' >> beam.io.WriteToText(known_args.output, file_name_suffix='.jsonl'))

if __name__ == '__main__':
    run()
