import requests
import pandas as pd
import numpy as np
from f1.fetch import get, get_cached, endpoint_reference, top_drivers


def calculate_curvature(session_key, driver_number):
    """Calculate curvature of the racing line for a given session and driver. Bigger curvature values indicate sharper corners, while smaller values indicate straighter sections of the track."""
   
    # Fetch location data for the specified session and driver
    location_Data_XY = get("location", session_key=session_key, driver_number=driver_number)

    # Sort the data by timestamp to ensure correct order and resets row indices after sorting
    location_Data_XY = location_Data_XY.sort_values("date").reset_index(drop=True)

    # Curviture array to store curvature values for each point
    curvatures = []

    # Calculate curviture using 3 (x,y) points in a row curviture corrensponds to the middle point of the 3 points used to calculate it.
    for i in range(1, len(location_Data_XY) - 1):
        # Need 1 point before and 1 point after to calculate curvature

        # Put the 3 points into numpy arrays for easier calculations
        p1 = np.array([location_Data_XY.loc[i-1, "x"], location_Data_XY.loc[i-1, "y"]])
        p2 = np.array([location_Data_XY.loc[i, "x"], location_Data_XY.loc[i, "y"]])
        p3 = np.array([location_Data_XY.loc[i+1, "x"], location_Data_XY.loc[i+1, "y"]])

        # Find side lenghts of the triangle formed by the 3 points
        a = np.linalg.norm(p2 - p3)
        b = np.linalg.norm(p1 - p3)
        c = np.linalg.norm(p1 - p2)

        # Find the area of the triangle formed by the 3 points
        A = 0.5 * np.abs(p1[0] * (p2[1] - p3[1]) + p2[0] * (p3[1] - p1[1]) + p3[0] * (p1[1] - p2[1]))

        # Caluclate curvature using k = 4A / (abc)
        if a * b * c == 0:
            curvature = 0
        else:
            curvature = 4 * A / (a * b * c)

        # Add curvatures to curvature array
        curvatures.append(curvature)

    # Remove first and last rows as they don't have curvature values
    location_Data_XY = location_Data_XY.iloc[1:-1].copy()

    # Add curvature values to the dataframe
    location_Data_XY["curvature"] = curvatures
    
    return location_Data_XY 


def identify_corners(curvature_data, curvature_threshold=0.01):
    """Identifies corners in the curvature data based on a curvature threshold. Returns a list of corner indices."""
    # Need to identify curvature threshold to identify corners, need to look at data to find a good threshold, maybe 0.01 is a good starting point.
    
    # Return a boolean column indicating whether each point is part of a corner based on the curvature threshold
    curvature_data["corner"] = (curvature_data["curvature"] >= curvature_threshold)

    return curvature_data

def find_apex(corner, x, y):
    # Find the approximate apex of a corner
    pass

def get_apex_velocity(apex_time, speed_data):
    # Find speed closest to apex timestamp
    pass