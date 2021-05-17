function  countsAFMYoungHeigthNotNormPlanned(saveDir,matrixOriginal,matrixPlanned,minHeigth,maxHeigth,numDivisions)
mkdir(saveDir)
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% countsAFMYoungHeigthPlanned : Calculate the correlation between heigth
% and young's modulus considering the heigth from the tsv but not normilized
%
% Input
%       saveDir:        string with the path to save the figures
%       matrixOriginal: matrix with all the information from the .tsv file
%       matrixYoung:    matrix with the young's modulus
%       matrixPlanned:  matrix with planned heigth
%       numDivisions:   number of intervals the data will be divided
%
% Ouput
%      nothing to do
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% call function to split the data

[~,~,matrixYoung]=splitMatrixFromAFMData(matrixPlanned,matrixOriginal);

%% determine the intervals for histograms
% matrixHeigthTmp=matrixOriginal(:,9); % taking only the information of Height
% minHeigth=min(min(matrixHeigthTmp));
% maxHeigth=max(max(matrixHeigthTmp));
% matrixHeigthNorm=(matrixHeigthTmp-minHeigth)/(maxHeigth-minHeigth);

% matrixYoungTmp=matrixOriginal(:,11); % taking only the information of Young Modulus

 figure; histogram(matrixPlanned)
 outFile =[saveDir,filesep,'histogramHeigthNorm'];
figH = gcf;
saveas(figH,outFile,'fig');
saveas(figH,outFile,'png');

 figure;histogram(matrixYoung)
 outFile =[saveDir,filesep,'histogramYoung'];
figH = gcf;
saveas(figH,outFile,'fig');
saveas(figH,outFile,'png');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% show the relation between Height and young's modulus

% inside the cell
[xpos,ypos]=find(matrixYoung<5*10^4);
figure
imshow(matrixPlanned,[])
hold
plot(ypos',xpos,'bx')
legend('youngs Modulus<5*10⁴')
title('Normalized Height Removing <0.12')

outFile =[saveDir,filesep,'insideCellHeigthYoung'];
figH = gcf;
saveas(figH,outFile,'fig');
saveas(figH,outFile,'png');

% ouside of the cells
[xpos,ypos]=find(matrixYoung>5*10^4);
figure
imshow(matrixPlanned,[])
hold
plot(ypos',xpos,'rx')
legend('youngs Modulus>5*10⁴')
title('Normalized Height Removing <0.12')

outFile =[saveDir,filesep,'outsideCellHeigthYoung'];
figH = gcf;
saveas(figH,outFile,'fig');
saveas(figH,outFile,'png');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% show the relation between H and YM only considering the inside of the cell

% save the matrix planned
matrixPlannedNew=matrixPlanned;

% make matrix a vector
matrixPlanned=matrixPlanned(:);

% create a vector of NaNs to fill with the values related with inside the
% cell
matrixPlannedNaN=nan(length(matrixPlanned),1);


young2keep=find(matrixYoung<5*10^4);
matrixPlannedNaN(young2keep)=matrixPlanned(young2keep);
matrixYoungCell=matrixYoung(young2keep);
matrixHeigthCell=matrixPlanned(young2keep);

% plot only the relation between heigth and young inside the cell
figure
plot(matrixHeigthCell,matrixYoungCell,'bo')
ylabel('Youngs Modulus')
xlabel('Height')
title('inside the cell')
outFile =[saveDir,filesep,'scatterPlotInsideCell'];
figH = gcf;
saveas(figH,outFile,'fig');
saveas(figH,outFile,'png');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% % %% identify the column that appears in the scatter plot
% % valsInside=-0.4*10^-7<=matrixPlannedNaN & matrixPlannedNaN<=0.4*10^-7;
% % valsOutside=-(valsInside-1);
% % valsOutside=find(valsOutside);
% % matrixPlannedNaN(valsOutside)=NaN;
% % % returm to a matrix form
% % matrixPlannedNaN=reshape(matrixPlannedNaN,80,60);
% % matrixPlannedNewReshape=reshape(matrixPlanned,80,60);
% % % find x and y where the matrix is not NaN
% % [xVal,yVal]=find(~isnan(matrixPlannedNaN));
% % figure
% % imshow(matrixPlannedNewReshape,[])
% % hold
% % plot(xVal,yVal,'bo')
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%



%% outside of the cell
matrixYoungOutCell=matrixYoung;
matrixYoungOutCell((young2keep))=[];
matrixHeigthOutCell=matrixPlanned;
matrixHeigthOutCell((young2keep))=[];

% plot only the relation between heigth and young
figure
plot(matrixHeigthOutCell,matrixYoungOutCell,'ro')
ylabel('Youngs Modulus')
xlabel('Height')
title('Outside the cell')
outFile =[saveDir,filesep,'scatterPlotOutsideCell'];
figH = gcf;
saveas(figH,outFile,'fig');
saveas(figH,outFile,'png');

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
valsOutside=find(-0.5*10^-7<=matrixHeigthOutCell & matrixHeigthOutCell<=0.5*10^-7);
figure
plot(matrixHeigthOutCell(valsOutside),matrixYoungOutCell(valsOutside),'ro')

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
% now use the Heights to count the young's modulus

valuesHeight=unique(matrixPlanned);
countsHeightCell=histcounts(matrixPlanned,valuesHeight);
figure; bar(valuesHeight(1:end-1),countsHeightCell)


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% relation between heigth and young's modulus
% determine some intervals for the heigth and determine the mean young's modulus in
% this interval

%% determine the max and min values of heigth and divide into 15 intervals

% maxHeigth=max(max(matrixHeigthCell));
% minHeigth=min(min(matrixHeigthCell));

heigthStep=(maxHeigth-minHeigth)/numDivisions;
heigthInterval=minHeigth:heigthStep:maxHeigth;
% save the heigth interval
save([saveDir,filesep,'heigthInterval'],'heigthInterval','-v7.3');
% determine which are the pixels that have the determined heigth
% initiate the matrix to save the mean and std

meanStdYoungIntervalHigth=nan(length(heigthInterval)+1,2);


% calculate all that are smaller than the first number 
indexHeigth= minHeigth>matrixHeigthCell;
youngIntervalHigth=matrixYoungCell(indexHeigth);
meanStdYoungIntervalHigth(1,1)=mean(youngIntervalHigth);
meanStdYoungIntervalHigth(1,2)=std(youngIntervalHigth);

for i=1:length(heigthInterval)-1
    indexHeigth= heigthInterval(i)<matrixHeigthCell & heigthInterval(i+1)>matrixHeigthCell;   
    youngIntervalHigth=matrixYoungCell(indexHeigth);
    meanStdYoungIntervalHigth(i+1,1)=mean(youngIntervalHigth);
    meanStdYoungIntervalHigth(i+1,2)=std(youngIntervalHigth);
end

% calculate all that are greater than the last number 
indexHeigth= maxHeigth<matrixHeigthCell;
youngIntervalHigth=matrixYoungCell(indexHeigth);
meanStdYoungIntervalHigth(size(meanStdYoungIntervalHigth,1),1)=mean(youngIntervalHigth);
meanStdYoungIntervalHigth(size(meanStdYoungIntervalHigth,1),2)=std(youngIntervalHigth);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
figure
bar(meanStdYoungIntervalHigth(:,1))
ax = gca;
if numDivisions==20
ax.XTick = [0 5 10 15 22];
ax.XTickLabel = {'-0.010-0.125','0.512-0.642','1.165-1.295','1.817-1.947','2.339-2.470'};
elseif numDivisions==10
ax.XTick = [0 2 4 6 8 11];
ax.XTickLabel = {'-0.010-0.251','0.512-0.773','1.034-1.295','1.817-1.2078','2.339-2.600'};   
end
% h.XTick = 1:19;
% h.XTickLabel = {'10^-8<','10^-8-2.22*10^⁻7','2.22*10^⁻7-4.35*10^⁻7', 4.35333333333333e-07 6.48000000000000e-07 8.60666666666667e-07 1.07333333333333e-06 1.28600000000000e-06 1.49866666666667e-06 1.71133333333333e-06 1.92400000000000e-06 2.13666666666667e-06 2.34933333333333e-06 2.56200000000000e-06 2.77466666666667e-06 2.98733333333333e-06 3.20000000000000e-06]};
ylabel('Mean Youngs Modulus')
xlabel('Heigth intervals (\mum)')
axis([0 numDivisions+5 0 6*10^4])
hold on

errorbar(meanStdYoungIntervalHigth(:,1),meanStdYoungIntervalHigth(:,2), '.k')


hold off
% save figure
outFile =[saveDir,filesep,'histogramHeigthxYoungInsideTheCell'];
figH = gcf;
saveas(figH,outFile,'fig');
saveas(figH,outFile,'png');

close all