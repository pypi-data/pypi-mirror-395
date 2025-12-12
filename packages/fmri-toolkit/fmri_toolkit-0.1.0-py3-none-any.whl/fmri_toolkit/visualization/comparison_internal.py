import pandas as pd
import numpy as np
from plotnine import ggplot, aes, geom_col, theme, element_text, labs
def fmri_pval_comparison_internal(p_val1,p_val2,names = ["p_val1", "p_val2"],breaks = 10):
    # keys1=[]
    # keys2=[]
    # p_val1=p_val1.reshape((-1))
    # p_val2=p_val2.reshape((-1))
    # for i in range(len(p_val1)):
    #     keys1.append(names[0])
    #     keys2.append(names[1])
    # keys=np.concatenate((keys1,keys2),axis=0)
    # values=np.concatenate((p_val1,p_val2),axis=0)
    # df=pd.DataFrame({"p_value_name":keys,"p_values":values})
    # mx=np.max(values)
    # mn=np.min(values)
    # bins=[mn+((mx-mn)*i/breaks) for i in range(breaks+1)]  
    # df['bin'] = pd.cut(df["p_values"], bins)
    # # df.groupby(["p_value_name","bin"])["p_values"].count().reset_index(name="freq")
    # df2=df.groupby(["p_value_name","bin"])["p_values"].transform("count")
    # df["freq"]=df2
    # df["bin"]=df["bin"].astype(str)
    # plotval=[ -1*df.iloc[i,3] if df.iloc[i,0]==names[0] else df.iloc[i,3] for i in range(df.shape[0])]
    # df["plotval"]=plotval
    # plot=ggplot(df,aes(x="bin",y="plotval",fill="p_value_name"))+geom_col()+ggtitle("Comparison between"+names[0]+"and"+names[1])+theme(plot_title=element_text(weight="bold",ha="center"),axis_text_x=element_text(ha="center",rotation=90))
    # print(plot)
    # return plot
    p_val1 = np.asarray(p_val1).reshape(-1)
    p_val2 = np.asarray(p_val2).reshape(-1)

    # Long dataframe
    df = pd.DataFrame({
        "p_value_name": [names[0]] * len(p_val1) + [names[1]] * len(p_val2),
        "p_values": np.concatenate([p_val1, p_val2])
    })

    # Build bins over the data range
    mn, mx = df["p_values"].min(), df["p_values"].max()
    bins = np.linspace(mn, mx, breaks + 1)
    df["bin"] = pd.cut(df["p_values"], bins=bins, include_lowest=True)

    # Aggregate frequencies by group/bin
    freq = (df.groupby(["p_value_name", "bin"], observed=True)
              .size().reset_index(name="freq"))

    # Mirror bars: first series negative, second positive
    freq["plotval"] = np.where(freq["p_value_name"].eq(names[0]), -freq["freq"], freq["freq"])
    freq["bin"] = freq["bin"].astype(str)

    plot = (
        ggplot(freq, aes(x="bin", y="plotval", fill="p_value_name"))
        + geom_col()
        + labs(title=f"Comparison between {names[0]} and {names[1]}",
               x="p-value bin", y="Frequency (mirrored)")
        + theme(
            plot_title=element_text(weight="bold", ha="center"),
            axis_text_x=element_text(ha="center", rotation=90)
        )
    )

    return plot


# p_val1=np.random.rand(160)
# p_val2=np.random.rand(160)
# fmri_pval_comparison_internal(p_val1,p_val2)

    
    