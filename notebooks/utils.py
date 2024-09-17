import matplotlib.pyplot as plt
import pandas
import seaborn as sns
import seaborn.objects as so
import wordcloud
from wordcloud import WordCloud, STOPWORDS

def normalized_percent_graphs(df, columns, plot_filename, include_null=False,
                              prints=False,xlabel='Source',cmap=False):
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

    if not cmap:
        cmap="deep"

    p = (so.Plot(melted,x='variable',y='value',color='percent')
        .add(so.Bar(), so.Stack())
        .layout(size=(8,4))
        .scale(color=cmap)
        .label(x=xlabel,y="Fraction of answers",legend='Budget fraction')
        )
    if plot_filename[-4]!='.': #if we haven't given an extension, assume you want both png and svg
        p.save(loc=plot_filename+'.svg', bbox_inches="tight")
        p.save(loc=plot_filename+'.png', bbox_inches="tight")
    else:
        p.save(loc=plot_filename, bbox_inches="tight")

def select_all_that_apply_hist_facet(df,question_col,plot_filename,options_dict=False,
                                     facet_col=False, drop_empty=True,how='facet',delim=", ",
                                     ylabel='Options',create_other=False,**kwargs):
    """
    Make a faceted (or not) graph from a "select all that apply" column
    You can drop just empties in the facet col ('facet'), question('question'),
    neither(False) or all (True). You can choose to show facet as colors or columns,
    and optionally rename the column names with shortnames. 
    """
    df.fillna('',inplace=True)
    if drop_empty==False:
        facet_drop = False
        q_drop = False
    elif drop_empty=='facet':
        facet_drop=True
        q_drop=False
    elif drop_empty=='question':
        facet_drop=False
        q_drop=True
    else:
        facet_drop=True
        q_drop=True
    df_list = []
    if facet_col:
        facet_vals = list(set(df[facet_col]))
        if facet_drop:
            facet_vals.remove('')
    else:
        facet_vals = [0]
    for facet in facet_vals:
        if facet_col:
            sub_df = df.query(f'`{facet_col}` == "{facet}"')
        else:
            sub_df=df
        if q_drop:
            sub_df = sub_df.query(f'`{question_col}` != ""')
        flat_list = []
        for x in sub_df[question_col]:
            #messy to handle delims that are fancy, like parentheses
            if delim[0]!= ",":
                to_append = delim.split(",")[0]
                split_x = x.split(delim)
                sub_split = [x+to_append for x in split_x[:-1]]
                flat_list+= sub_split+[split_x[-1]]
            else:
                flat_list+=(x.split(delim))
        if options_dict:
            flat_list = [options_dict[x] for x in flat_list]
        if create_other:
            kept_flat_list = [x for x in flat_list if x in create_other]
            flat_list = kept_flat_list + ['Other']*(len(flat_list)-len(kept_flat_list))
        flat_series = pandas.Series(flat_list,name=facet)
        value_counts = flat_series.value_counts(normalize=True)
        value_counts.rename(facet,inplace=True)
        df_list.append(value_counts)
    normed_df = pandas.concat(df_list,axis=1)

    melted = normed_df.melt(ignore_index=False)
    melted = melted.reset_index(names='percent')
    melted = melted.sort_values(by=['variable','percent']).reset_index(drop=True)
    if how=='facet':
        g = sns.catplot(melted,y='percent',x='value',col='variable',kind='bar',**kwargs)
        g.set_axis_labels("Fraction of answers",ylabel)
        g.set_titles(col_template=f"{facet_col} = "+"{col_name}")
    elif how=='color':
        g = sns.catplot(melted,y='percent',x='value',hue='variable',kind='bar', **kwargs)
        g.legend.set_title(facet_col)
        plt.ylabel(ylabel)
        plt.xlabel("Fraction of answers")
    if plot_filename[-4]!='.': #if we haven't given an extension, assume you want both png and svg
        plt.savefig(plot_filename+'.png')
        plt.savefig(plot_filename+'.svg')
    else:
        plt.savefig(plot_filename)

def wordcloud_func(col_name,new_stop_list,plot_filename,df,**kwargs):
    """wrapper around https://amueller.github.io/word_cloud/generated/wordcloud.WordCloud.html
    See that documentation for more kwargs to pass (colors, max words, etc)
    """
    all_stopwords = list(STOPWORDS)+new_stop_list+col_name.split(' ')
    wordcloud_words = ' '.join(list(df[col_name].dropna())).lower()

    wc = WordCloud(background_color='white',min_word_length=4,min_font_size=34,
                   stopwords=all_stopwords,regexp=r"\w[\w'\/]+",**kwargs
                  ).generate(wordcloud_words)
    plt.title(col_name+"\n",wrap=True)
    plt.axis('off')
    plt.imshow(wc)
    plt.savefig(plot_filename, bbox_inches='tight')