# NSNT  
Natural Stimulus Neuroimaging Toolbox(NSNT) is aimed to provide toolbox 
to analysis fMRI data which was induced by natural stimulus.


# TODO List(can be thought as doc)
### algorithms  
Undertake major calculation.  
Main function:
1. Cal ISFC, ISC, FC and others.
2. Cal info of data and result, like global waveform.
3. Evaluate the parcellation/clustering results.

### iofunc
Load data from file, save data into file.<br>
Main function:
1. Read brain data and data info(like golbal_waveform.dat file). (Note: should specify the input arg.)
2. Save result as brain map.
3. Read result.
4. Save image into file.
5. Save movie into file.
6. Create label by vertex or index(based on atlas).
7. Read data by label.
8. Specify io function in every file.

### plot  
Plot image based on defferent input arg.  
Main function:
1. plot brain map.
2. plot global waveform and meanval.
3. plot head motion parameters.

### utils  
Provide small but necessary function.  
Main function:
1. adjacency tools, returning faces, edges adj matrix and so on.
2. data stats, show the stats of data and some func to operate data.
3. matrix tools, operating adj matrix or time series matrix.
4. utils, other tools.
5. others that need to be specified.
