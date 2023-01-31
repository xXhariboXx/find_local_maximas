import argparse
import json
import logging
from dataclasses import asdict, dataclass
from typing import List, Tuple

import matplotlib.pyplot as plt
import numpy as np
from dacite.core import from_dict
from scipy.signal import argrelextrema


@dataclass
class MeasurementData:
    time: float
    data: float


def find_maximas(measurements: List[MeasurementData], maximum_window: int) -> List[MeasurementData]:
    measurement_data = np.array([measurement.data for measurement in measurements])
    result_index = argrelextrema(measurement_data, np.greater_equal, order=maximum_window)[0]
    if not len(result_index):
        return []
    logging.info(f"Founded: {len(result_index)} maximas with window: {maximum_window}")
    return [measurements[i] for i in list(result_index)]


def load_measurements(file_path: str) -> List[MeasurementData]:
    measurements = []
    with open(file_path) as file:
        json_data = json.load(file)
        for entry in json_data:
            measurements.append(from_dict(MeasurementData, entry))
    logging.info(f"Loaded measurements from file: {file_path}. Number of measurements: {len(measurements)}")
    return measurements


def save_measurements(file_path: str, measurements: List[MeasurementData]):
    with open(file_path, "w") as f:
        f.write(json.dumps([asdict(maximum) for maximum in measurements]))
    logging.info(f"Saved measurements to file: {file_path}. Number of measurements: {len(measurements)}")


def plot_data_and_maximas(measurements: List[MeasurementData], maximas: List[MeasurementData]):
    plt.plot([measurement.time for measurement in measurements], [measurement.data for measurement in measurements])
    plt.plot(
        [measurement.time for measurement in maximas], [measurement.data for measurement in maximas], "o", color="red"
    )
    plt.show()


def parse_arguments() -> Tuple[str, str, int]:
    """Parser script parameters.
    Accepted parameters:
    * '-input': input file path
    * '-output': output file path
    * '-window': window size
    Returns:
        str: input file path
        str: output file path
        int: window size
    """
    parser = argparse.ArgumentParser(description="Script for Finding local maximas in json data")
    parser.add_argument("-input", type=str, help="Path with (file name) for input file")
    parser.add_argument("-output", type=str, help="Path with (file name) for output file")
    parser.add_argument("-window", type=int, help="Size of window for searching maximas")
    args = parser.parse_args()
    logging.info(f"Parameters: {args}")
    return args.input, args.output, args.window


def main():
    input_path, output, window = parse_arguments()
    measurements = load_measurements(input_path)
    maximas = find_maximas(measurements, window)
    save_measurements(output, maximas)
    plot_data_and_maximas(measurements, maximas)


def setup_logger():
    logging.basicConfig(format="%(levelname)s:\t%(message)s", level=logging.INFO)


if __name__ == "__main__":
    setup_logger()
    main()
