


% font 都改成times new roman
% 在0，30, 60纬度度加一下虚线
% 
clear all; close all; clc
addpath '../../../Functions/'
clear all; close all; clc;

% Define center latitude and longitude
centerLat = 46.2420;
centerLon = -89.3477;

% Define delta
delta = 0.01;

% Set up geographic axes for the small region
figure;
gx = geoaxes;
geolimits([centerLat - delta, centerLat + delta], [centerLon - delta, centerLon + delta]); % Use variables

geobasemap satellite; % Use satellite basemap
grid on;

% Add dashed reference lines at 0°, 30°, and 60° latitude
hold on;
geoplot([0 0], [-180 180], 'k--', 'LineWidth', 0.5); % Equator
hold on
geoplot([30 30], [-180 180], 'k--', 'LineWidth', 0.5);
hold on
geoplot([60 60], [-180 180], 'k--', 'LineWidth', 0.5);

% Format font
gx.FontName = 'Times New Roman';
gx.FontSize = 20;
gx.LongitudeLabel.String = 'Longitude';
gx.LatitudeLabel.String = 'Latitude';

% Save the figure
set(gcf, 'Renderer', 'painters');
print(gcf, 'map_zoomed_region_US_Syv', '-dpng', '-r300');
disp('Figure Saved.');
