function corr_covid_19()
%读取数据
data=csvread('corr_data.csv',1,2);
x = data(:,1:6); % 新增确诊、治愈、死亡，累计确诊、治愈、死亡数据
y = data(:,7:13);% 迁入、迁出、温度、湿度、aqi、卫生人员、人口
%[A,B,r,U,V,stats]=canoncorr(x,y);
coef = corr(x,y)
xlabel = ["new_con","new_cured","new_dead","all_con","all_cured","all_dead"];
ylabel = ["move_in", "move_out", "temp", "hum", "aqi", "hospital", "pop"];
disp(ylabel)
disp(coef)
end