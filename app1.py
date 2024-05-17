
####################
#functions

#function gia na diabasei protaseis
#ανοιγμα και διαβασμα αρχειου
def get_words_from_text():
    with open("reading.txt",encoding='utf-8')as f :
        text=f.read()

        #replace whitespaces
        text=' '.join(text.split())

        text=text.lower()
        simeia_stixis='''|-!()[]{}:;\'\",<>./?#@#%^&*_'''

        for i in text:
            if i in simeia_stixis or i.isdigit():
                text=text.replace(i, '')

        text=' '.join(text.split())

    words=text.split()
    return words
            
def get_number_of_unique_words():
    #metatropo ti lista se synolo,oste na paro tis monadikes lexeis
    return len(set(words))

def get_number_of_words():
    #return the amount of the words
    return len(words)

import operator

def get_5_least_frequent_words(words):
    #dimiourgia lexikou exei key tis lexeis k value ti syxnotita
    dict_of_occurrences={}
    for item in words:
        if item in dict_of_occurrences:
            dict_of_occurences[item]+=1
        else:
            dict_of_occurences[item]=1

        #taxinomisi tou lexikou me basi to value
    sorted_list=sorted(dict_of_occurrences.items(),key=operator.itemgetter(1))
    #epistrefei pleiada taxinomimeni
    final_list=sorted_list[:5]

    least_words=[]

    for key,value in final_list:
        least_words.append(key)
        
    return least_words

def graph_add_node(v1,v2):
    #elegxos an einai 2 sunexomenes lexeis
    if v1==v2:
        reurn
    #elegxos an i korifi v1 uparxei hdh
    if v1 in my_graph:
        #check if v2 exists
        if v2 in my_graph[v1]:
            #euresi tou index tou barous tou zeygous
            w_index=my_graph[v1].index(v2)+1
            #auxisi tou barous kata 1
            my_graph[v1][w_index]=my_graph[v1][w_index]+1
        else:
            #pristhiki neon korufon
            temp_dict={
                v1:[v2,1]
                }
            my_graph.update(temp_dict)


    
###############
#main program
            
#dimiourgia kenou grafou
my_graph={}

#eisagogi korifon k upologismos twn baron sto grafo
for i in range(len(allwords)):
    #prosthetei seiriaka ta zeygoi lexewn sto grafo
    #afinei ektos tin teleutaia lexi pou den akolouthite apo alli
    if i!=len(allwords)-1:
        graph_add_node(allwords[i],allwords[i+1])
    else:
        if allword[i] in my_graph:
            continue
        else:
            temp_dict={
                allwords[i]: []
                }
            my_graph.update(temp_dict)
            


