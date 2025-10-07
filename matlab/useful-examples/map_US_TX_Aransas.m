% README
%
% =========================================================================
% ## Map Generator for Aransas Bay, TX ##
%
% Author: Koutian Wu
% Date: 2025-10-07
%
% ---
%
% ### Description ###
%
% This script generates a series of satellite maps centered on the `marabwq` 
% station in Aransas Bay, TX. It produces four maps with different zoom 
% levels, corresponding to square areas of 90x90 meters, 200x200 meters, 
% 1x1 kilometers, and 10x10 kilometers.
%
% The script calculates the required latitude and longitude boundaries based
% on the desired area size in meters and saves each map as a high-resolution
% PNG image to a dedicated output directory.
%
% ---
%
% ### Usage ###
%
% 1. Ensure the `Functions` directory is correctly located relative to this
%    script, or update the `addpath` line accordingly.
% 2. Run the script in MATLAB.
% 3. The generated maps will be saved in the `tx-aransas` subdirectory.
%
% ---
%
% ### Configuration ###
%
% - `centerLat`, `centerLon`: GPS coordinates for the map center.
% - `map_sizes_m`: An array defining the width/height of each map in meters.
% - `output_dir`: The folder where the output images will be saved.
%
% =========================================================================

% --- Initial Setup ---
clear all; close all; clc;
% addpath('../../../Functions/');

% --- Configuration ---
% Define center latitude and longitude for Aransas Bay (`marabwq` station)
centerLat = 27.9798;
centerLon = -97.0287;

% Define map area sizes in meters (for square maps)
map_sizes_m = [200, 1000, 5000, 1000]; 

% Define the output directory
output_dir = 'tx-aransas';

% Create the output directory if it doesn't exist
if ~exist(output_dir, 'dir')
   mkdir(output_dir);
   disp(['Created output directory: ' output_dir]);
end

% --- Main Loop to Generate Maps ---
disp('Starting map generation...');

for i = 1:length(map_sizes_m)
    current_size_m = map_sizes_m(i);
    
    fprintf('\nProcessing map for area: %d_m x %d_m\n', current_size_m, current_size_m);

    % --- Convert Map Size from Meters to Degrees ---
    % This conversion is an approximation.
    % 1. Latitude: The distance for one degree of latitude is relatively constant.
    %    Approximately 111,132 meters per degree.
    lat_deg_per_meter = 1 / 111132;
    
    % 2. Longitude: The distance for one degree of longitude depends on the latitude.
    %    It shrinks as one moves from the equator to the poles.
    %    Formula: 111,320 * cos(latitude) meters per degree.
    lon_deg_per_meter = 1 / (111320 * cosd(centerLat));

    % Calculate the delta (half the total width/height) in degrees for the geolimits function.
    lat_delta = (current_size_m / 2) * lat_deg_per_meter;
    lon_delta = (current_size_m / 2) * lon_deg_per_meter;

    % --- Create and Configure Map ---
    fig = figure('Name', ['Map ' num2str(current_size_m) 'm x ' num2str(current_size_m) 'm']);
    gx = geoaxes;

    % Set the geographic limits for the map using the calculated deltas
    geolimits([centerLat - lat_delta, centerLat + lat_delta], [centerLon - lon_delta, centerLon + lon_delta]);

    geobasemap satellite;
    grid on;

    % Format font and labels
    gx.FontName = 'Times New Roman';
    gx.FontSize = 20;
    gx.LongitudeLabel.String = 'Longitude';
    gx.LatitudeLabel.String = 'Latitude';

    % --- Save the Figure ---
    % Create a clean label for the file name (e.g., '90m', '1km')
    if current_size_m >= 1000
        file_label = [num2str(current_size_m/1000) 'km'];
    else
        file_label = [num2str(current_size_m) 'm'];
    end
    
    file_name = ['tx_aransas_' file_label '.png'];
    full_path = fullfile(output_dir, file_name);

    % Save the current figure
    set(gcf, 'Renderer', 'painters');
    print(gcf, full_path, '-dpng', '-r300');
    disp(['Figure saved: ' full_path]);
    
    close(fig); % Close the figure to free memory before the next loop iteration
end

disp('---');
disp('All maps generated successfully.');
