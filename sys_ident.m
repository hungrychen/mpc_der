clear; clc; clf

data = readmatrix("data.txt");
data(:,3:4) = data(:,3:4) / 480;

time = data(:,1);
ctrl = data(:,2);
y_pos = data(:,4);

figure(1);
yyaxis left;
plot(time, ctrl);
yyaxis right;
plot(time, y_pos);

query = 1:0.05:58;
vq_ctrl = interp1(time, ctrl, query);
vq_y_pos = interp1(time, y_pos, query);

query = query(:);
vq_ctrl = vq_ctrl(:);
vq_y_pos = vq_y_pos(:);

figure(2);
yyaxis left;
plot(query, vq_ctrl)
yyaxis right;
plot(query, vq_y_pos);


