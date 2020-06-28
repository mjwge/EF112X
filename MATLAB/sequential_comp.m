% Program for compensating all 6 factors in a sequential fashion, using a
% separate linear estimator for each one. 


first = false;  % variable to decide if all data needs to be loaded or if it is 
                % already in the workspace. 
dvar = false;

if first
factors = readtable ('C:\Users\mjwge\Documents\kex\Measurement_data\tryck_klor_flode_jun_sep.csv');

load 'C:\Users\mjwge\Documents\kex\Measurement_data\Linghem\2017-06-21'

date = table2array(factors(6:end,1));
inFlow = table2array(factors(6:end,3));
outFlow = table2array(factors(6:end,5));
inPressure = table2array(factors(6:end,7));
outPressure = table2array(factors(6:end,9));
chlorine = table2array(factors(6:end,11));
chlorine = strrep(chlorine, ',', '.');
inFlow = strrep(inFlow, ',', '.');
outFlow = strrep(outFlow, ',', '.');
inPressure = strrep(inPressure, ',', '.');
outPressure = strrep(outPressure, ',', '.');

% chlorine = cell2mat(chlorine);
chlorine = str2double(chlorine);
inFlow = str2double(inFlow);
outFlow = str2double(outFlow);
inPressure = str2double(inPressure);
outPressure = str2double(outPressure);

end


meas = W1_raw_samples(101,1:6:end)*current_factors(1);
% meas = (meas-mean(meas))/var(meas);
og = meas;
%------------------------------------------------
% Tempcomp
N2 = size(W1_raw_samples);
N2 = N2(2)/6;
A2=zeros(2,N2);
A2(1,:) = temperatures(1:6:end);
A2(2,:) = 1;
A2=A2';

tmp2 = (A2'*meas')\(A2'*A2);
C = meas'-A2*tmp2';
C = (C-mean(C));
if dvar
    C = C/var(C);
end
% size(C)
meas = C;
%-------------------------------------------------------
%Chlorine comp
N2 = size(W1_raw_samples);
N2 = N2(2)/6;
A2=zeros(2,N2);
A2(1,:) = chlorine(28146:28146+1440-1);
A2(2,:) = 1;
A2=A2';

tmp2 = (A2'*meas)\(A2'*A2);
% size(C)
C = meas-A2*tmp2';
C = (C-mean(C));
if dvar
    C = C/var(C);
end
meas = C;
% size(C)
%-------------------------------------------------------
%outFlow comp
N2 = size(W1_raw_samples);
N2 = N2(2)/6;
A2=zeros(2,N2);
A2(1,:) = outFlow(28146:28146+1440-1);
A2(2,:) = 1;
A2=A2';

tmp2 = (A2'*meas)\(A2'*A2);
C = meas-A2*tmp2';
C = (C-mean(C));
if dvar
    C = C/var(C);
end
meas = C;

% -----------------------------------------------------------
% inFlow comp
N2 = size(W1_raw_samples);
N2 = N2(2)/6;
A2=zeros(2,N2);
A2(1,:) = inFlow(28146:28146+1440-1);
A2(2,:) = 1;
A2=A2';

tmp2 = (A2'*meas)\(A2'*A2);
C = meas-A2*tmp2';
C = (C-mean(C));
if dvar
    C = C/var(C);
end
%------------------------------------------------------------
% inPressure comp
N2 = size(W1_raw_samples);
N2 = N2(2)/6;
A2=zeros(2,N2);
A2(1,:) = inPressure(28146:28146+1440-1);
A2(2,:) = 1;
A2=A2';

tmp2 = (A2'*meas)\(A2'*A2);
C = meas-A2*tmp2';
C = (C-mean(C));
if dvar
    C = C/var(C);
end

% yyaxis left
% plot(og)
% ylabel('Original data, [\mu A]')
% 
% hold on;
% yyaxis right
% plot(C)
% ylabel('Compensated data, [\mu A]')
% 
% xlabel('Time, [minutes]')
% 
% legend( ' Original ', ' Compensated ' )



