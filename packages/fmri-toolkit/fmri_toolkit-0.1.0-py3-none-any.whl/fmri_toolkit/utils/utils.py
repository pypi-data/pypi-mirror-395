
import numpy as np
import math
def floor_dec(x,level=1):
            return round(x - 5*10^(-level-1), level)
                
def ceiling_dec(x,level=1):
            return round(x+5*10^(-level-1), level)
# def fmri_stimulus(scans = 1,onsets = [1],durations = [1],TR = 2,times = False,sliceorder = None,type = ["canonical", "gamma", "boxcar", "user"],par = None,scale = 10,hrf = None,verbose = False):
#     if(not times):
#         onsets=onsets*TR
#         duration=duration*TR
#     slicetiming=np.isnan(sliceorder)
#     if(slicetiming):
#         nslices=len(sliceorder)
#         scale=max(scale,nslices)
#         slicetimes=[a for a in range(1,nslices)][sliceorder]/(TR*scale)
#     onsets=onsets*scale
#     durations=durations*scale
#     scans=scans*TR*scale
#     TR=TR/scale
#     slicetiming=not(np.isnan(sliceorder))
#     if(slicetiming):
#         nslices=len(sliceorder)
#         slicetimes=math.ceil([a for a in range(1,nslices)][sliceorder]/(nslices*scale))
#     no=len(ofset)
#     if(ke(durations)==1):
#         durations=np.repeat(durations,no)
#     elif(len(durations)!=no):
#         print("Length of duration vector does not match a number of offsets")

#     if(slicetiming):
#         stimulus=np.zeros((math.ceil(scans)),nslices)
#         for j in range(nslices):
#             for i in range(no):
#                 stimulus[max(1,)]
#     else:
#         stimulus=np.zeros((math.ceil(scans))
#         for i in range(no):
            



    