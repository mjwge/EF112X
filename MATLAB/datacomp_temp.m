% Creation of input vectors when linear estimator for temperature is
% applied. 


weekvec =[1 2 3 4 5 6 7]';
weekvec = weekvec/7;
days = 90;
%en iteration gör en komplett input vektor
name = [2017 06 21];
day_index = 3;
for i=1:days
    if ismember(name(2), [10 11 12]) && ismember(name(3),[1 2 3 4 5 6 7 8 9])    
        str = num2str(name(1)) + "-" + num2str(name(2)) + "-0" + num2str(name(3)) + ".mat";        
    elseif not(ismember(name(2), [10 11 12])) && ismember(name(3),[1 2 3 4 5 6 7 8 9])
        str = num2str(name(1)) + "-0" + num2str(name(2)) + "-0" + num2str(name(3)) + ".mat";       
    elseif ismember(name(2), [10 11 12]) && not(ismember(name(3),[1 2 3 4 5 6 7 8 9]))
        str = num2str(name(1)) + "-" + num2str(name(2)) + "-" + num2str(name(3)) + ".mat";
    else
        str = num2str(name(1)) + "-0" + num2str(name(2)) + "-" + num2str(name(3)) + ".mat";
    end
    load_adress = ['data_v7\' + str];
    save_adress = ['datasets_temp\' + str];
    load(load_adress);
   disp([load_adress, save_adress])
%     time = 0; %faktor av tiden för mätning
%     temperature = zeros(2,1); %temperatur för varje minut (1440,1)
    weekday = weekvec(day_index);
    if day_index == 7
        day_index = 1;
    else
        day_index = day_index + 1;
    end
    
    % tempkomp compensates the temperature in a linear fashion
    raw_data = tempkomp(W1_raw_samples, current_factors, temperatures);
   
    input = [raw_data(1:6:8630)];
    save(save_adress, 'input','-v7');
    if ismember(name(2), [1 3 5 7 8 10 12]) && name(3) == 31
        name(2) = name(2)+1;
        name(3) = 1;
    elseif ismember(name(2), [4 6 9 11]) && name(3) == 30
        name(2) = name(2)+1;
        name(3) = 1;
    elseif name(2) == 2 && name(3) == 28
        name(2) = name(2)+1;
        name(3) = 1;
    else
        name(3) = name(3)+1;

    end
    if name(2) == 13
        name(2) = 1;
    end
%     disp(input)
end
