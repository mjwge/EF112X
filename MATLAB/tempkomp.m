% Function for eliminating temperature from measurements using a linear
% estimator. 

function Cprim = tempkomp(W1_raw_samples,current_factors,...
                            temperatures)
N = size(W1_raw_samples);
N = N(2);
A=zeros(2,N);
A(2,:) = temperatures;
A(1,:) = 1;
A=A';

C = W1_raw_samples(101,:).*current_factors(1);
C = C';
tmp = (A'*C)\(A'*A);
% tmp = [0.3969,0.0567 ];
Cprim = C-A*tmp';
Cprim = (Cprim - mean(Cprim))/var(Cprim);
% figure()
% plot(Cprim)
% hold on;
% plot(C, 'rp')
% hold on;
% axis([0 N -1 3]);