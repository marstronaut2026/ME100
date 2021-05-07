clc, clear, close all

F = load("data2.txt");
t = F(:,1);
s = F(:,2);
p = F(:,3);

yyaxis left
plot(t,p)
ylabel("Pressure (psi)")
ylim([0 200])
xlabel("Time (s)")

yyaxis right
plot(t,s)
ylabel("Valve Position (deg)")
ylim([-10 100])
legend("Pressure (psi)","Valve Position (deg)")