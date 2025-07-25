



% font 都改成times new roman
% 在0，30, 60纬度度加一下虚线


clear all; close all; clc
addpath 'D:\0lrn\00Res\Functions'
% addpath 'D:\0lrn\00Res\Functions\m_map'

% Update meteor parameters
directoryPath = 'D:\0lrn\00Res\Data\';
baseFilename = 'A0_Stations_Para_';
WKT_runLatestVersion(directoryPath, baseFilename);
load('D:\0lrn\00Res\Data\MR_Stations_Para.mat');

fsz = [12 13];
MRFontColor = 'yellow';

for k1 = 1: length(STs)
    if strcmp(string(STs{k1}), 'MCMR') || ...
            strcmp(string(STs{k1}), 'ALOMR') || ...
            strcmp(string(STs{k1}), 'ASSMR') || ...
            strcmp(string(STs{k1}), 'KEPMR') || ...
            strcmp(string(STs{k1}), 'SVMR') || ...
            strcmp(string(STs{k1}), 'TRMR') || ...
            strcmp(string(STs{k1}), 'MHMR') || ...
            strcmp(string(STs{k1}), 'BJMR') || ...
            strcmp(string(STs{k1}), 'BPMR') || ...
            strcmp(string(STs{k1}), 'WHMR') || ...
            strcmp(string(STs{k1}), 'KMMR') || ...
            strcmp(string(STs{k1}), 'FKMR') || ...
            strcmp(string(STs{k1}), 'KTMR') || ...
            strcmp(string(STs{k1}), 'TRMR') || ...
            strcmp(string(STs{k1}), 'DWMR') || ...
            strcmp(string(STs{k1}), 'DVMR')
        % do  nothing
    else
        STs{k1} = '';
        sites{k1} = '';
        lons(k1) = NaN;
        lats(k1) = NaN;
        freqs(k1) = NaN;
    end
end

% STs

figure;
whitefig;
figpos([1 1])

%% proj
gx = geoaxes;
geolimits([-75 80], [-179.999 179.999]) %LAT, LON
% geolimits([-80 80], [-179.999 179.999]) %LAT, LON
% geobasemap colorterrain
% geobasemap landcover
geobasemap satellite
grid off


GridWidth = 0.5
PlotLim = 210
hold on
geoplot([0 0], [-PlotLim PlotLim], 'Color', [0.5 0.5 0.5], 'LineWidth', GridWidth); % 0°
hold on
geoplot([30 30], [-PlotLim PlotLim], 'Color', [0.5 0.5 0.5], 'LineWidth', GridWidth); % 30°
hold on
geoplot([60 60], [-PlotLim PlotLim], 'Color', [0.5 0.5 0.5], 'LineWidth', GridWidth); % 60°

hold on
geoplot([-30 -30], [-PlotLim PlotLim], 'Color', [0.5 0.5 0.5], 'LineWidth', GridWidth); % 30°
hold on
geoplot([-60 -60], [-PlotLim PlotLim], 'Color', [0.5 0.5 0.5], 'LineWidth', GridWidth); % 60°


set(gx, 'TickLabelFormat', 'dd')
gx.FontName =  'Times New Roman';
gx.FontSize =  fsz(1);
% gx.LatitudeLabel.FontName = 'Times New Roman';
% gx.LongitudeLabel.FontSize = fsz(1);
% set(gx, 'TickDir', 'out')
% gx.TickLabelFormat = 'dd';
gx.LongitudeLabel.String = 'Geographic Longitude';
gx.LatitudeLabel.String  = 'Geographic Latitude';

if(0)
    %% TG Volcano
    cities = {'Hunga-Tonga Volcano'};
    TGlon = -175.38+360;
    TGlat = -20.536;
    TGfsz = 12; % Example font sizes
    hold on;
    text(TGlat, TGlon + 6, string(cities), 'FontSize', TGfsz, 'FontWeight', 'bold', 'Color', 'r');

    % {'▲'};
    markerSizes = 1:11; % Array of marker sizes
    for markerSize = markerSizes
        geoplot(TGlat, TGlon, 'r^', 'MarkerSize', markerSize);
    end


    %% antipode
    cities={'Antipode'};
    ATGlon = TGlon -180;
    ATGlat = -TGlat ;
    ATGfsz = 12; % Example font sizes
    hold on;
    text(ATGlat, ATGlon + 5, string(cities), 'FontSize', ATGfsz, 'FontWeight', 'bold', 'Color', 'b');

    % {'▽'};
    markerSizes = 1:11; % Array of marker sizes
    for markerSize = markerSizes
        geoplot(ATGlat, ATGlon, 'bv', 'MarkerSize', markerSize);
    end

    %% Meteor radars Great Circle distance from TG
    dist = zeros(length(sites), 1);
    N = 1000; % N greater, the more precise
    for k1=1:length(sites)
        [dist(k1), ~, ~] = m_lldist([TGlon lons(k1)], [TGlat lats(k1)], N);
    end

    % % % % % % % [string(sites{k1})+' ('+string(STs{k1})+', '+num2str(freqs(k1))+' MHz)']
end

%% Meteor radars stations, StaNames, distance, PRF
for k1=1:length(sites)
    % [range, ln, lt]=m_lldist([-123-6/60, lons(k)], [49+13/60, lats(k)], 40);
    if lons(k1)>0 % longitude in E zone
        if strcmp(string(STs{k1}), 'MCMR')
            hold on;
            text(lats(k1)+2, lons(k1)-3.001, sprintf('%s (%s, %.1f MHz)', sites{k1}, STs{k1}, freqs(k1)), 'FontSize', fsz(1), 'FontName', 'Times New Roman', 'FontWeight', 'bold', 'Color', MRFontColor, 'HorizontalAlignment', 'right');
            hold on;
            geoplot(lats(k1), lons(k1), 'r.', 'MarkerSize', 20);
        elseif strcmp(string(STs{k1}), 'SVMR')
            hold on;
            text(lats(k1)-3, lons(k1), sprintf('%s (%s, %.1f MHz)', sites{k1}, STs{k1}, freqs(k1)), 'FontSize', fsz(1), 'FontName', 'Times New Roman', 'FontWeight', 'bold', 'Color', MRFontColor, 'HorizontalAlignment', 'center');
            hold on;
            geoplot(lats(k1), lons(k1), 'r.', 'MarkerSize', 20);
        elseif strcmp(string(STs{k1}), 'DVMR')
            hold on;
            text(lats(k1)+5, lons(k1), sprintf('%s (%s, %.1f MHz)', sites{k1}, STs{k1}, freqs(k1)), 'FontSize', fsz(1), 'FontName', 'Times New Roman', 'FontWeight', 'bold', 'Color', MRFontColor, 'HorizontalAlignment', 'center');
            hold on;
            geoplot(lats(k1), lons(k1), 'r.', 'MarkerSize', 20);
        elseif strcmp(string(STs{k1}), 'BPMR') | strcmp(string(STs{k1}), 'DWMR')
            hold on;
            text(lats(k1), lons(k1)-3.001, sprintf('%s (%s, %.1f MHz)', sites{k1}, STs{k1}, freqs(k1)), 'FontSize', fsz(1), 'FontName', 'Times New Roman', 'FontWeight', 'bold', 'Color', MRFontColor, 'HorizontalAlignment', 'right');
            hold on;
            geoplot(lats(k1), lons(k1), 'r.', 'MarkerSize', 20);
        else
            hold on;
            text(lats(k1), lons(k1)+3.001, sprintf('%s (%s, %.1f MHz)', sites{k1}, STs{k1}, freqs(k1)), 'FontSize', fsz(1), 'FontName', 'Times New Roman', 'FontWeight', 'bold', 'Color', MRFontColor);
            hold on;
            geoplot(lats(k1), lons(k1), 'r.', 'MarkerSize', 20);
        end

    else
        if strcmp(string(STs{k1}), 'ALOMR') | strcmp(string(STs{k1}), 'ASSMR') | strcmp(string(STs{k1}), 'KEPMR')
            hold on;
            text(lats(k1), lons(k1)-3.001, sprintf('%s (%s, %.1f MHz)', sites{k1}, STs{k1}, freqs(k1)), 'FontSize', fsz(1), 'FontName', 'Times New Roman', 'FontWeight', 'bold', 'Color', MRFontColor, 'HorizontalAlignment', 'right');
            hold on;
            geoplot(lats(k1), lons(k1), 'r.', 'MarkerSize', 20);
        else
            hold on;
            text(lats(k1), lons(k1)+3.001, sprintf('%s (%s, %.1f MHz)', sites{k1}, STs{k1}, freqs(k1)), 'FontSize', fsz(1), 'FontName', 'Times New Roman', 'FontWeight', 'bold', 'Color', MRFontColor);
            hold on;
            geoplot(lats(k1), lons(k1), 'r.', 'MarkerSize', 20);
        end
    end
end

error;

%% EXPORT FIG ==============================================================
% Set renderer to "painters"
set(gcf, 'Renderer', 'painters');
print(gcf, ['Map_-75_+80'], '-dpng', '-r600');
disp('Figure Saved.');


function [dist, lons, lats] = m_lldist(long, lat, N)
% M_LLDIST Spherical earth distance between points in long/lat coordinates.
%   RANGE=M_LLDIST(LONG, LAT) gives the distance in kilometers between
%   successive points in the vectors LONG and LAT, computed
%   using the Haversine formula on a spherical earth of radius
%   6378.137km. Distances are probably good to better than 1% of the
%   "true" distance on the ellipsoidal earth
%
%   [RANGE, LONGS, LATS]=M_LLDIST(LONG, LAT, N) computes the N-point geodesics
%   between successive points. Each geodesic is returned on its
%   own row of length N+1.
%
%   See also M_XYDIST

% Rich Pawlowicz (rich@ocgy.ubc.ca) 6/Nov/00
% This software is provided "as is" without warranty of any kind. But
% it's mine, so you can't sell it.
%
% 30/Dec/2005 - added n-point geodesic computations, based on an algorithm
%               coded by Jeff Barton at Johns Hopkins APL in an m-file
%               I looked at at mathworks.com.


pi180=pi/180;
earth_radius=6378.137;

m=length(long)-1;

long1=reshape(long(1:end-1), m, 1)*pi180;
long2=reshape(long(2:end)  , m, 1)*pi180;
lat1= reshape(lat(1:end-1) , m, 1)*pi180;
lat2= reshape(lat(2:end)   , m, 1)*pi180;

dlon = long2 - long1;
dlat = lat2 - lat1;
a = (sin(dlat/2)).^2 + cos(lat1) .* cos(lat2) .* (sin(dlon/2)).^2;
angles = 2 * atan2( sqrt(a), sqrt(1-a) );
dist = earth_radius * angles;


if nargin==3 && nargout>1   % Compute geodesics.

    % Cartesian unit vectors in rows of v1, v2
    v1=[cos(long1).*cos(lat1)   sin(long1).*cos(lat1)   sin(lat1) ];
    v2=[cos(long2).*cos(lat2)   sin(long2).*cos(lat2)   sin(lat2) ];

    % We want to get a unit vector tangent to the great circle.
    n1=cross(v1, v2, 2);
    t1=cross(n1, v1, 2);
    t1=t1./repmat(sqrt(sum(t1.^2, 2)), 1, 3);

    lons=zeros(m, N+1);
    lats=zeros(m, N+1);
    for k=1:m

        % Radials for all points
        p1=v1(k, :)'*cos(angles(k)*[0:N]/N) + t1(k, :)'*sin(angles(k)*[0:N]/N);

        lons(k, :)=atan2(p1(2, :), p1(1, :))/pi180;
        lats(k, :)=asin(p1(3, :))/pi180;

    end

end
end
