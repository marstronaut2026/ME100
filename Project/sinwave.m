clc, clear, close all

X = 1:60;

Y = 4*sin(X/30*pi)+7;
n = find(Y < 7)';
plot(X,Y)
grid on
axis equal