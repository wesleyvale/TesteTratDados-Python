function [matrixHeigthNorm,matrixHeigth,matrixYoung]=splitMatrixFromAFMData(matrixPlanned,matrixOriginal)
%% script to ordinate the matrix with heigth information

% determine the number of columns and rows, now I am using the information
% of the information from the planned image
[numRows,numColuns]=size(matrixPlanned);

matrixHeigthTmp=matrixOriginal(:,9); % taking only the information of heigth
matrixYoungTmp=matrixOriginal(:,47); % taking only the information of Young Modulus

columnsInterval=1:numColuns:length(matrixHeigthTmp);

for i=1:numRows-1
    matrixHeigth(i,1:numColuns)=matrixHeigthTmp(columnsInterval(i):columnsInterval(i+1)-1);
    matrixYoung(i,1:numColuns)=matrixYoungTmp(columnsInterval(i):columnsInterval(i+1)-1);
end

% include last row
matrixHeigth(numRows,1:numColuns)=matrixHeigthTmp(columnsInterval(end):end);
matrixYoung(numRows,1:numColuns)=matrixYoungTmp(columnsInterval(end):end);


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% alternetive using reshape

%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%


%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
%% normalize the heigths between 0 and 1
minHeigth=min(min(matrixHeigth));
maxHeigth=max(max(matrixHeigth));
matrixHeigthNorm=(matrixHeigth-minHeigth)/(maxHeigth-minHeigth);