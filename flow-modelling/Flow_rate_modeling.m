T = readtable("load-cell-data_4W.csv");
data = table2array(T);

plot(data(:,3),data(:,1),'k')
hold on
f = @(t) 38*(1-exp(-0.18*t)); % first order fit to 4 Watt data
fplot(f,[0 30],'r')
hold off

%%
close all; clc

K = 467;
tau = 6.1;

f = @(t) K*(1-exp(-t/tau)) / 1000;
fplot(f, [0,30])

%% 
clear all; close all; clc

% second order model params
% mass
density_ecoflex = 1070; % kg/m3
h = 3.3 / 1000; % m
ro = 16.4 / 1000; % m
ri = 12.6 / 1000; % m
m = density_ecoflex * (h*pi*(ro^2 - ri^2)); % kg
% spring stiffness
Y_ecoflex = 0.1 * 1e6; % 0.1 MPa
a = 3.3*3.8 / 1e6; % cross sectional area, m^2
l = 2*pi*14.5 / 1000; % circumference, m
k = Y_ecoflex * a / l;
% damping
b = 0.1*sqrt(4*k*m);

% first order input params
K = 467; % mN
tau = 6.1;
f = @(t) K*(1-exp(-t/tau)) / (1000); % input force (N)

tspan = 0:.1:30;
r0 = [0; 0];
[t,r] = ode45(@(t,r) modelling(r,m,k,b,f(t)),tspan,r0);

hold on
plot(t,r(:,1)) % 'radius'
% plot(t,r(:,2)) % change in radius
ylabel("radius (m)")

for i = 1:length(t)
    a_dot(i) = 2*pi*r(i,1)*r(i,2);
    v_dot(i) = 2*pi*h*r(i,1)*r(i,2);
end

adot_mm = a_dot*1e6;
vdot_ml = v_dot*1e6;

writematrix(vdot_ml, 'vdot_model.csv')

figure
plot(t, vdot_ml)
xlabel('Time (sec)')
% ylabel("dA/dt mm2/s")
ylabel('V_{dot} (mL/sec)')

%% Volumetric flow rate using pixel change of a cylindrical cell

X = readtable("donut_data_60fps.csv");  % read raw data
time = X{:,1};  % seconds
area = X{:,4};  % mm^2
height = 3.8;   % mm
vol = height*area;  % mm^3

n = length(time);
% determine volumetric flow rate 
dVol(1) = (vol(2)-vol(1))/(time(2)-time(1));  
for i = 2:(n-1) % forward finite difference
    dVol(i) = (vol(i+1)-vol(i))/(time(i+1)-time(i));  
end
dVol(n) = (vol(n)-vol(n-1))/(time(n)-time(n-1));    % backward finite diff  
B = smoothdata(dVol);   % smooth data

figure
subplot(2,1,1)
plot(time,vol)
xlabel('Time (sec)')
xlim([0 25])
ylabel('Volume (mm^{3})')

subplot(2,1,2)
plot(time,dVol)
xlabel('Time (sec)')
xlim([0 25])
ylabel('Volume (mm^{3}/sec)')
ylim([-500 500])
