import numpy as np
def fmri_simulate_func(dim_data,mask=None,ons=[1,21,41,61,81,101,121,141],dur=[10,10,10,10,10,10,10,10]):
    
    dimx=dim_data[0]
    dimy=dim_data[1]
    dimz=dim_data[2]
    motor_3d=np.ones(dim_data)
    r_motor=int((min(dimx,dimy,dimz)+1)/11)
    if(mask is not None):
        for x in range(dimx):
            for y in range(dimy):
                for z in range(dimz):
                    x0=int((1+dimx)/2)
                    y0=int((1+dimy)/2)
                    z0=int((1+dimy)/2)
                    x1=x0
                    y1=y0
                    z1=int((1+dimz)/4)
                    x2=x0-int((1+dimx)/4)
                    y2=y0
                    z2=z0
                    x3=x0+r_motor
                    y3=y0+r_motor
                    z3=z0+r_motor
                    norm=(x-x1)**2+(y-y1)**2+(z-z1)**2
                    norm2=(x-x2)**2+(y-y2)**2+(z-z2)**2
                    norm3=(x-x3)**2+(y-y3)**2+(z-z3)**2
                    rm2=r_motor**2
                    if(norm<=rm2 or norm2<=rm2 or norm3<=rm2):
                        motor_3d[x,y,z]=0

    else:
        r_mask=int((min(dimx,dimy,dimz)-2)/2)
        mask=np.zeros(dim_data)
        for x in range(dimx):
            for y in range(dimy):
                for z in range(dimz):
                    x0=int((1+dimx)/2)
                    y0=int((1+dimy)/2)
                    z0=int((1+dimy)/2)
                    x1=x0
                    y1=y0
                    z1=int((1+dimz)/4)
                    x2=x0-int((1+dimx)/4)
                    y2=y0
                    z2=z0
                    x3=x0+r_motor
                    y3=y0+r_motor
                    z3=z0+r_motor
                    norm0=(x-x0)**2+(y-y0)**2+(z-z0)**2
                    norm=(x-x1)**2+(y-y1)**2+(z-z1)**2
                    norm2=(x-x2)**2+(y-y2)**2+(z-z2)**2
                    norm3=(x-x3)**2+(y-y3)**2+(z-z3)**2
                    rm2=r_motor**2
                    if(norm0<=r_mask**2):
                        mask[x,y,z]=1
                    if(norm<=rm2 or norm2<=rm2 or norm3<=rm2):
                        motor_3d[x,y,z]=0
    ons=np.array(ons)
    tspan=ons[-1]+2*dur[-1]-1
    print(tspan)
    data4d=np.random.uniform(0,15,dimx*dimy*dimz*tspan)
    data4d=data4d.reshape((dimx,dimy,dimz,tspan))
    on_time=[]
    t_range=[a for a in range(tspan)]
    off_time=[]
    for i in range(len(dur)):
        on_st=ons[i]
        on_st=int(on_st)
        # print(on_st)
        on_end=ons[i]+dur[i]-1
        on_end=int(on_end)
        on_time_pts=[a for a in range(on_st,on_end+1)]
        off_st=ons[i]+dur[i]
        off_end=ons[i]+2*dur[i]-1
        off_time_pts=[a for a in range(off_st,off_end+1)]
        on_time=[on_time,on_time_pts]
        off_time=[off_time,off_time_pts]

    for t in t_range:
        data4d[:,:,:,t]=data4d[:,:,:,t]*mask
        if(t in on_time):
            on_motor_data=np.random.uniform(12,18,(dimx*dimy*dimz))
            on_motor_data=on_motor_data.reshape(dim_data)
            data4d[:,:,:,t]=data4d[:,:,:,t]*motor_3d+on_motor_data*(1-motor_3d)

    return {"fmridata":data4d,"mask":mask,"ons":ons,"dur":dur,"on_time":on_time}

# x=fmri_simulate_func(dim_data = [64, 64, 40], mask = None, 
#                                    ons = [1, 21, 41, 61, 81, 101, 121, 141], 
#                                    dur = [10, 10, 10, 10, 10, 10, 10, 10])
# print(x["fmridata"].shape)