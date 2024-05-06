import seaborn
import seaborn.objects as so
import pandas

def normalized_percent_graphs(df, columns, plot_filename, include_null=False,
                              prints=False,xlabel='Source'):
    """
    Takes dataframes and columns (either a list or a dict
    wherein the key is the real column name and the values are
    the name to use in the figure, if different) and returns
    a graph of per-question normalized percents. Defaults to not 
    including null results but can. Makes a couple useful prints
    along the way
    """
    if type(columns)==list:
        columns = {x:x for x in columns}

    if include_null:
        fill = 'Not answered'
    else:
        fill = ''
    df.fillna(fill,inplace=True)
    if prints:
        print(f"Original shape: {df.shape}")

    #subset to rows which have an answer in any row
    rows_with_answers = '(`'+'`  != "") | (`'.join(columns)+'`  != "")'
    df = df.query(rows_with_answers)
    if prints:
        print(f"Shape after filtering: {df.shape}")

    df_list = []
    for eachcol in columns.keys():
        if not include_null:
            sub_df=df.query(f'`{eachcol}` != ""')
        else:
            sub_df=df
        if prints:
            print(sub_df.shape,sub_df[eachcol].value_counts())
        normed_df = sub_df[eachcol].value_counts(normalize=True)
        normed_df = normed_df.rename(columns[eachcol])# have to do it here, newlines in the query are sad :(
        df_list.append(normed_df)
    normed_df = pandas.concat(df_list,axis=1)
    if not include_null:
        normed_df.fillna(0,inplace=True)

    melted = normed_df.melt(ignore_index=False)
    melted = melted.reset_index(names='percent')
    melted = melted.sort_values(by=['percent']).reset_index(drop=True)
    if prints:
        print("Melted results",melted)
    melted

    p = (so.Plot(melted,x='variable',y='value',color='percent')
        .add(so.Bar(), so.Stack())
        .layout(size=(8,4))
        .label(x="Source",y="Fraction of answers",legend='Budget fraction')
        )
    p.save(loc=plot_filename, bbox_inches="tight")