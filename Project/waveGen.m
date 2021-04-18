clc, clear, close all

t = [0:0.02:15]';
format = '%f\n';
S = sim('noisyStep',t);

sig = S.signal(:,1);

plot(t,sig)
xlabel("Time (s)")
ylabel("Valve Position (degrees)")

f = fopen('test.txt','w+');
fprintf(f,format,sig);
fclose('all');

g = fopen('polyfit.txt','w+');
Y = polyfit(t,sig,6);
fprintf(g,format,Y);
    