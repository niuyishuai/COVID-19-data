function corr_covid_19()
%读取数据
namelist = ["Hubei","notHubei"];
for i =1:2
    name = namelist(i);
    filename = ['corr_',char(name),'.csv'];
    data=csvread(filename,1,2);
    x = data(:,1:6); % 新增确诊、治愈、死亡，累计确诊、治愈、死亡数据
    y = data(:,7:14);% 迁入、迁出、温度、湿度、aqi、医疗救治医院、发热门诊、人口
    %[A,B,r,U,V,stats]=canoncorr(x,y);
    coef = corr(x,y);
    sum_coef = sum(abs(coef(1:3,:)));
    xlabel = ["new_con  ","new_cured","new_dead ","all_con  ","all_cured","all_dead "];
    ylabel = ["        ","move_in ", "move_out", "temp    ", "hum    ", "aqi    ", "hospital","fever   ", "pop     "];
    fid = fopen([char(name),'.txt'],'a');
    for j = 1:9
        fprintf(fid,'%s\t',ylabel(j));
    end
    fprintf(fid,'\r\n');
    for i = 1:6
        fprintf(fid,'%s\t',xlabel(i));
        for j = 1:8
            fprintf(fid,'%.5f\t',coef(i,j));
        end
        fprintf(fid,'\r\n');
    end
    fprintf(fid,'\r\n');
    fprintf(fid,'new_sum\t');
    for j = 1:8
        fprintf(fid,'%.5f\t',sum_coef(j));
    end
    fclose(fid);
end
end