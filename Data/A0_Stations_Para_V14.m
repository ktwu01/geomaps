




clear all; clc; close all;

% Prompt: sort out the following stations by latitude (show in lons), 
% from high to low latitude. keep the original matlab format of all stations

% configuration rules: (the same as m_map)
% latitude: south hemis --> lon < 0, north hemis --> lon >0
% longitude: from 0 deg --> 90E --> 180 --> 90W  --> 0
% lon: from 0 --> 90 --> 180 --> 360-90  --> 360

%% create
% Station information
STs = {};
sites = {};
lons = [];
lats = [];
freqs = []; % frequencies, MHz
PRFs = []; % Hz
PPW = []; % Peak Power, kW

% % Svalbard (SVMR, 78.3°N, 16°E)
% STs = [STs, 'SVMR'];
% sites = [sites, 'Svalbard'];
% lons = [lons, 16];
% lats = [lats, 78.3];

% SVA (Svalbard) 78.17°N 15.99°E
STs = [STs, 'SVMR'];
sites = [sites, 'Svalbard'];
lons = [lons, 15.99];
lats = [lats, 78.17];
freqs = [freqs, 31]; % MHz
PRFs = [PRFs, nan]; % Hz

% Alta (ALT, 70.0° N, 23.3° E) Norway
STs = [STs, 'ALTMR'];
sites = [sites, 'Alta'];
lons = [lons, 23.3];
lats = [lats, 70.0];
freqs = [freqs, 31]; % MHz
PRFs = [PRFs, 430]; % Hz

% Tromsø (TRMR, 69.59°N, 19.2°E) Norway
STs = [STs, 'TRMR'];
sites = [sites, 'Tromsø'];
lons = [lons, 19.2];
lats = [lats, 69.59];
freqs = [freqs, 30.3]; % MHz
PRFs = [PRFs, 500]; % Hz

% 450 MHz Poker flat incoherent scatter radar (PFISR) in Alaska (65N, 147W)

% PKF (Poker flat) 65.13°N 147.5°W
STs = [STs, 'PKFMR'];
sites = [sites, 'Pokerflat'];
lons = [lons, 360-147.5];
lats = [lats, 65.13];
freqs = [freqs, nan]; % MHz
PRFs = [PRFs, nan]; % Hz

% Mohe (MHMR, 53.5°N, 122.33°E)
STs = [STs, 'MHMR'];
sites = [sites, 'Mohe'];
lons = [lons, 122+20/60];
lats = [lats, 53+30/60];
freqs = [freqs, 38.9]; % MHz
PRFs = [PRFs, nan]; % Hz

% COL (Collm) 51.31°N 13.0°E
STs = [STs, 'COLMR'];
sites = [sites, 'Collm'];
lons = [lons, 13.0];
lats = [lats, 51.31];
freqs = [freqs, nan]; % MHz
PRFs = [PRFs, nan]; % Hz

% CMO (CMOR) 43.26°N 80.77°W
STs = [STs, 'CMOR'];
sites = [sites, 'CMOR'];
lons = [lons, 360-80.77];
lats = [lats, 43.26];
freqs = [freqs, nan]; % MHz
PRFs = [PRFs, nan]; % Hz

% Beijing (BJMR, 40.3°N, 116.2°E)
STs = [STs, 'BJMR'];
sites = [sites, 'Beijing'];
lons = [lons, 116.2];
lats = [lats, 40.3];
freqs = [freqs, 38.9]; % MHz
PRFs = [PRFs, nan]; % Hz

% Mengcheng (MCMR, 33.36°N, 116.49°E)
STs = [STs, 'MCMR'];
sites = [sites, 'Mengcheng'];
lons = [lons, 116.49];
lats = [lats, 33.36];
freqs = [freqs, 38.9]; % MHz
PRFs = [PRFs, 430]; % Hz

% Wuhan (WHMR, 30.5°N, 114.4°E)
STs = [STs, 'WHMR'];
sites = [sites, 'Wuhan'];
lons = [lons, 114.4];
lats = [lats, 30.5];
freqs = [freqs, 38.9]; % MHz
PRFs = [PRFs, nan]; % Hz

% Kunming (KMMR, 25.6°N 103.8°N)
STs = [STs, 'KMMR'];
sites = [sites, 'Kunming'];
lons = [lons, 103.8];
lats = [lats, 25.6];
freqs = [freqs, 37.5]; % MHz
PRFs = [PRFs, nan]; % Hz

        % Fuke (FKMR, 19.5°N, 109.1°E)
        STs = [STs, 'FKMR'];
        sites = [sites, 'Fuke'];
        lons = [lons, 109.1];
        lats = [lats, 19.5];
        freqs = [freqs, 38.9]; % MHz
        PRFs = [PRFs, nan]; % Hz

        % Sanya (SYMR, 18.3°N, 109.6°E)
        STs = [STs, 'SYMR'];
        sites = [sites, 'Sanya'];
        lons = [lons, 109.6];
        lats = [lats, nan];
        freqs = [freqs, nan]; % MHz
        PRFs = [PRFs, nan]; % Hz

        % Ledong (LDMR, 18.4°N,109°E)
        STs = [STs, 'LDMR'];
        sites = [sites, 'Ledong'];
        lons = [lons, 109];
        lats = [lats, 18.4];
        freqs = [freqs, 38.9]; % MHz
        PRFs = [PRFs, nan]; % Hz

% Kototabang (KTMR, 0.2°S, 100.3°E)
STs = [STs, 'KTMR'];
sites = [sites, 'Kototabang'];
lons = [lons, 100.3];
lats = [lats, -0.2];
freqs = [freqs, 37.7]; % MHz
PRFs = [PRFs, nan]; % Hz

% CAR (Cariri) 7.38°S 36.53°W
STs = [STs, 'CARMR'];
sites = [sites, 'Cariri'];
lons = [lons, 360-36.53];
lats = [lats, -7.38];
freqs = [freqs, nan]; % MHz
PRFs = [PRFs, nan]; % Hz

% Ascension Island (ASSMR, 7.9°S, 14.4°W)
STs = [STs, 'ASSMR'];
sites = [sites, 'Ascension Island'];
lons = [lons, 360-14.4];
lats = [lats, -7.9];
freqs = [freqs, 43.5]; % MHz
PRFs = [PRFs, nan]; % Hz

% Darwin (DWMR, 12.3°S, 130.8°E),
STs = [STs, 'DWMR'];
sites = [sites, 'Darwin'];
lons = [lons, 130.8];
lats = [lats, -12.3];
freqs = [freqs, 33.2]; % MHz
PRFs = [PRFs, nan]; % Hz

% Andes Lidar Observatory (ALOMR, 30.25°S, 70.74°W)
% http://lidar.erau.edu/instrument/mr/index.php
% CONDOR (ALO) was in normal operation with both remote receiver systems at the Southern Cross Observatory (SCO) 
% and at Las Campanas Observatory (LCO)
% https://www.google.com/maps/place/Cerro+Tololo+Inter-American+Observatory/@-30.1641844,-70.8252553,8365m?entry=ttu
STs = [STs, 'ALOMR'];
sites = [sites, 'Andes Lidar Observatory'];
lons = [lons, 360-70.74];
lats = [lats, -30.40];
freqs = [freqs, 35.2]; % MHz
PRFs = [PRFs, 430]; % Hz

% Southern Cross Observatory (SCO) 
% A remote receive system was installed at Southern Cross Observatory (SCO) near Cambarbala, Chile and became operational on 7/15/2019.
% Google map: Southern Cross Observatory
% https://www.google.com/maps/place/Observatorio+Cruz+del+sur/@-31.2012201,-71.0004169,241m/?entry=ttu
% from bottom of https://www.observatoriocruzdelsur.cl/observatorio/telescopios/
% Coordenadas: 31°12'04.2"S 71°00'02.3"W
STs = [STs, 'SCOMR'];
sites = [sites, 'Southern Cross Observatory'];
lons = [lons, 360-71];
lats = [lats, -31.2];
freqs = [freqs, nan]; % MHz
PRFs = [PRFs, nan]; % Hz

% Las Campanas Observatory (LCO)
% A second remote receive system was installed at Las Campanas Observatory (LCO) in February 2020 and became operational on 2/20/2020.
% https://www.google.com/maps/place/Las+Campanas+Observatory/@-29.0164274,-70.6954792,4222m?entry=ttu
STs = [STs, 'LCOMR'];
sites = [sites, 'Las Campanas Observatory'];
lons = [lons, 360-70.69];
lats = [lats, -29.01];
freqs = [freqs, nan]; % MHz
PRFs = [PRFs, 430]; % Hz

% Buckland Park (BPMR)	34.6°S, 138.5°E	55 MHz	40 kW
STs = [STs, 'BPMR'];
sites = [sites, 'Buckland Park'];
lons = [lons, 138.5];
lats = [lats, -34.6];
freqs = [freqs, 55]; % MHz
PRFs = [PRFs, nan]; % Hz

% TDF (Tierra del Fuego) 53.79°S 67.75°W
STs = [STs, 'TDFMR'];
sites = [sites, 'Tierra del Fuego'];
lons = [lons, 360-67.75];
lats = [lats, -53.79];
freqs = [freqs, nan]; % MHz
PRFs = [PRFs, nan]; % Hz

% King Edward Point Station (KEPMR, 54.3° S, 36.5°W)
STs = [STs, 'KEPMR'];
sites = [sites, 'King Edward Point'];
lons = [lons, 360-36.5];
lats = [lats, -54.3];
freqs = [freqs, 35.2]; % MHz
PRFs = [PRFs, nan]; % Hz

% ROT (Rothera) 67.57°S 68.12°W
STs = [STs, 'RTMR'];
sites = [sites, 'Rothera Station'];
lons = [lons, 360-68.12];
lats = [lats, -67.57];
freqs = [freqs, nan]; % MHz
PRFs = [PRFs, nan]; % Hz

% Davis Station (DVMR, 68.58°S, 77.97°E)
STs = [STs, 'DVMR'];
sites = [sites, 'Davis'];
lons = [lons, 77.97];
lats = [lats, -68.58];
freqs = [freqs, 33.2]; % MHz
PRFs = [PRFs, nan]; % Hz

% McMurdo Station (MMMR, 77.85°S, 166.72°E)
STs = [STs, 'MMMR'];
sites = [sites, 'McMurdo Station'];
lons = [lons, 166.72];
lats = [lats, -77.85];
freqs = [freqs, nan]; % MHz
PRFs = [PRFs, nan]; % Hz

%% TG Volcano
TGlon = -175.38+360;
TGlat = -20.536;
% TGfsz = 12; % Example font sizes

%% antipode
ATGlon = TGlon -180;
ATGlat = -TGlat;
% ATGfsz = 12; % Example font sizes

save('D:\0lrn\00Res\Data\MR_Stations_Para.mat', ...
    'STs', 'sites', 'lons', 'lats', 'freqs', 'PRFs');
disp('Stations Para saved');

%% back up
% clear all; clc; close all;
% load('D:\0lrn\00Res\Data\MR_Stations_Para.mat');

% %% Meteor radars Great Circle distance from TG
% dist = zeros(length(sites),1);
% N = 10000; % N greater, the more precise
% 
% for ST_id=1:length(sites)
%     [dist(ST_id),~,~] = WKT_TG_lldist([TGlon lons(ST_id)], [TGlat lats(ST_id)], N);
%     % disp([string(sites{ST_id})+' ('+string(STs{ST_id})+', '+ ...
%     %     string(round(dist(ST_id)))+' km, ' ...
%     %     string(Dt_Fr_0000Jan14(ST_id))+' h from 04:35 UT Jan 10' ...
%     %     +num2str(freqs(ST_id))+' MHz)'])
%     disp([string(sites{ST_id})+' ['+string(STs{ST_id})+', '+string((lons(ST_id)))+' (WE0-360) '+', '+string((lats(ST_id)))+' (N+/S-) '+', '+string(round(dist(ST_id)))+' km, '+num2str(freqs(ST_id))+' MHz]']);
% end
% 
% disp({'';'';'';''})
% 
% % %% This code first sorts the Dt_Fr_0000Jan14 array in ascending order
% % % and obtains the indices of the sorting. 
% % % Then, it sorts the sites cell array based on the 
% % % obtained sorting indices. 
% % % Finally, it displays the sorted information. 
% % 
% % % Sort Dt_Fr_0000Jan14 in ascending order
% % [sorted_Dt_Fr_0000Jan14, sorting_indices] = sort(Dt_Fr_0000Jan14);
% % 
% % % Sort all other unsorted arguments based on the sorting_indices
% % sorted_sites = sites(sorting_indices);
% % sorted_STs = STs(sorting_indices);
% % sorted_dist = dist(sorting_indices);
% % sorted_freqs = freqs(sorting_indices);
% % 
% % % Display sorted information
% % for ST_id = 1:length(sorted_sites)
% %     disp([string(sorted_sites{ST_id})+' ['+string(sorted_STs{ST_id})+', '+string(round(sorted_dist(ST_id)))+' km]']);
% %     % disp(sprintf('%s\t(%s,\t%.2f km,\t%.2f h\tfrom 00:00 UT Jan 10,\t%.2f MHz)', ...
% %     % string(sorted_sites{ST_id}), string(sorted_STs{ST_id}), (sorted_dist(ST_id)), ...
% %     % (sorted_Dt_Fr_0000Jan14(ST_id)), sorted_freqs(ST_id)));
% % 
% % end
% % 
% % % variables = {};
% 
% % save('D:\0lrn\00Res\Data\MR_Stations_Para.mat', ...
% %     'STs', 'sites', 'lons', 'lats', 'freqs', 'PRFs', ...
% %     'dist');