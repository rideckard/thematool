import dbB
import numpy as np
import scipy.spatial as ss



def get_clusterscores(feature_dict,taste,top5000_meta,low5000_meta):
    ''' schraenkt die anzahl filme in den Cluster Scores ein nach den Features'''   
    if feature_dict["top5000"]:
    	df = top5000_meta[~top5000_meta["id"].isin(taste)]
    else:
    	df = low5000_meta
    if "genre" in feature_dict:
    	df = df[df["genres"].apply(lambda x: bool(set(x) & set(feature_dict["genre"])))]
    	if "director" in feature_dict:
            df = df[df["director"].apply(lambda x: bool(set(x) & set(feature_dict["director"])))]
    elif "director" in feature_dict:
        df = df[df["director"].apply(lambda x: bool(set(x) & set(feature_dict["director"])))]
    
    return(df[["C"+str(i) for i in range(100)] + ["id","title"]])
        
    
    
    
        
def calc_similar(x,y,anz_clusters=100):
    ''' Berechnet Similarity Spalte der Filme aus x mit dem Filmgeschmack y'''
    zur_df = x.copy()
    cl_c = x.iloc[:,0:anz_clusters].to_numpy()
    #print(cluster_scores.shape,y.shape)
    
    z = ss.distance.cdist(cl_c,np.array([y]), metric='jensenshannon')
    zur_df["similar"] = z
    return(zur_df)
    #print(z.shape)

def calc_mean_cl_score(i,x,anz_clusters=100):
    ''' Berechnet den Durchschnittsclusterscore der in id liste i gegebenen Filme 
    aus den Cluster scores in x. alle ids in i muessen in x enthalten sein'''
    ar = x[x["id"].isin(i)].iloc[:,0:anz_clusters].to_numpy()
    return( ar.sum(axis=0)/len(i) )
    
    
def get_movies(i,feature_dict,top5000_meta,low5000_meta):
    '''Holt Filme mit ids aus i aus sql datenbank'''
    if feature_dict["top5000"]:
    	return(top5000_meta[top5000_meta["id"].isin(i)])
    else:
    	return(low5000_meta[low5000_meta["id"].isin(i)])
    	



def movie_link(movietitle):
    ''' helper Funktion for datafram apply'''
    movie_url = "https://www.amazon.de/s?k=" + "+".join(movietitle.split(" ")) + "+ Film"
    return(movie_url)


def add_amazon_links(movies):
    movies_ret = movies.copy()
    movies_ret["amazon_link"] = movies["title"].apply(movie_link)
    return(movies_ret)
    
    
def prime_flow(feature_dict, movie_taste, all_scores,top5000_meta, low5000_meta,anz=10, anz_c=100):
    '''erwartet feature dict
                 feature_dict = {top : True/False
                 bottom: True/False
                director : list of directors
                 genre: list of genres
                   }
        movie_taste: list of ids
        anz: maximale anzahl zurueckgegebener Filme
        gibt DataFrame mit Filmen zurueck
    '''
    
    ## Berechne movie_taste_scores
    y = calc_mean_cl_score(movie_taste,all_scores,anz_clusters = anz_c)
    #print(y)
    
    ## Hole Auswahlpool
    cluster_scores_to_compare = get_clusterscores(feature_dict,movie_taste,top5000_meta,low5000_meta)
    
    
    ## Berechne Similarity in Auswahlpool 
    df = calc_similar(cluster_scores_to_compare,y,anz_clusters = anz_c)
    
    ## Hole anz ids mit top similarities
    id_list = list(df.sort_values("similar").head(anz)["id"])
    
    ## Hole Movies zu ids
    movies = get_movies(id_list,feature_dict, top5000_meta,low5000_meta)
    
    ## Amazon Links dranmachen
    movies = add_amazon_links(movies)
    
    return(movies)   
