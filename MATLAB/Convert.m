% Program for changing the version of .mat file for easy handling in
% python. 

clear all

daysLinghem = 90;
daysNykvarn = 4;
name = [2017 06 21];

% Conditionals in order to correctly load relevant files. 
for i = 1:daysLinghem
    if ismember(name(2), [10 11 12]) && ismember(name(3),[1 2 3 4 5 6 7 8 9])    
        str = num2str(name(1)) + "-" + num2str(name(2)) + "-0" + num2str(name(3)) + ".mat";        
    elseif not(ismember(name(2), [10 11 12])) && ismember(name(3),[1 2 3 4 5 6 7 8 9])
        str = num2str(name(1)) + "-0" + num2str(name(2)) + "-0" + num2str(name(3)) + ".mat";       
    elseif ismember(name(2), [10 11 12]) && not(ismember(name(3),[1 2 3 4 5 6 7 8 9]))
        str = num2str(name(1)) + "-" + num2str(name(2)) + "-" + num2str(name(3)) + ".mat";
    else
        str = num2str(name(1)) + "-0" + num2str(name(2)) + "-" + num2str(name(3)) + ".mat";
    end
    disp(i)
        disp(str);
        save_adress = ['data_v7\' + str];
        load_adress = ['Linghem\' + str];
        disp(save_adress)
        load(load_adress)
        disp([load_adress, save_adress])
        % Save all data as version 7. 
        save(save_adress,'current_factors', 'indexes', 'timestamps', ...
            'temperatures', 'W1_raw_samples', 'W2_raw_samples',...
            'W3_raw_samples','number_of_measures', '-v7');
        
        % Determine name of next relevant file. 
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
    
    
    
    
end

