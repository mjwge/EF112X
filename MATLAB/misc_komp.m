%% Chlorine komp

% Trying to compensate the influence of chlorine excess.  

% factors = readtable ('C:\Users\mjwge\Documents\kex\Measurement_data\tryck_klor_flode_jun_sep.csv');
date = table2array(factors(6:end,1));
inFlow = table2array(factors(6:end,3));
outFlow = table2array(factors(6:end,5));
inPressure = table2array(factors(6:end,7));
outPressure = table2array(factors(6:end,9));
chlorine = table2array(factors(6:end,11));
chlorine = strrep(chlorine, ',', '.');
% chlorine = cell2mat(chlorine);
chlorine = str2double(chlorine);

N = size(W1_raw_samples);
N = N(2);
A=zeros(2,N);
A(1,:) = temperatures;
A(2,:) = 1;
A=A';

C = W1_raw_samples(101,:).*current_factors(1);
C = C';
tmp = (A'*C)\(A'*A);
% tmp = [0.3969,0.0567 ];
Cprim = C-A*tmp';

N = size(W1_raw_samples)/6;
N = N(2);
A=zeros(2,N);
A(1,:) = chlorine(28146:28146+1440-1);
A(2,:) = 1;
A=A';


% C = W1_raw_samples(101,:).*current_factors(1);
% C = C(1:6:end);
% C = C';
C1 = Cprim(1:6:end);
figure(12) 
plot(C1, 'r')
hold on;

tmp = (A'*C1)\(A'*A);
% tmp = [0.3969,0.0567 ];
Cprim = C1-A*tmp';
Cprim = Cprim;
plot(Cprim, 'b')
hold on;
plot(C(1:6:end), 'g')
legend('tempkomp', 'chlorine komp', 'og')
%



% C = W1_raw_samples(101,:).*current_factors(1);
% C = C(1:6:end);
% plot(timestamps(1:6:end), C, 'r') 
% hold on;
% plot(timestamps(1:6:end), chlorine(28146:28146+1440-1).*200, 'b')
%Notera att cell-arrayer indexeras med {}

%% Complete comp

% Attempting to eliminate influence from all factors in one go, using one
% iteration of a linear estimator. 

first = false;
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


figure(11) 
%plot(C, 'r')
hold on;
%-----------------------------------------------------------------
N = size(W1_raw_samples)/6;
N = N(2);
A=zeros(N,7);
A(:,1) = 1;
A(:,2) = temperatures(1:6:end);
A(:,3) = chlorine(28146:28146+1440-1);
A(:,4) = inFlow(28146:28146+1440-1);
A(:,5) = outFlow(28146:28146+1440-1);
A(:,6) = inPressure(28146:28146+1440-1);
A(:,7) = outPressure(28146:28146+1440-1);
A=A';
C1 = meas;


tmp = (A*C1')\(A*A');
Cprim = C1-(A'*tmp')';
Cprim = (Cprim-mean(Cprim));
if dvar
    Cprim = Cprim/var(Cprim);
end

% yyaxis right
% plot(Cprim)
% hold on;
% og = (meas);
% 
% yyaxis left
% plot(og)
% legend('Measured current response', 'Compensated currentresponse' )
% ylabel('Measured current, [\mu A]')
% yyaxis right
% ylabel('Compensated current response, [\mu A]')
% xlabel('Time, [minutes]')
