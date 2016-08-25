#ifndef PARSE_NODES_H_
#define PARSE_NODES_H_

struct Nodes_pair{
    int count;
    char ** keys;
    char ** values;
};

//split a string by delimiter, return a char **
char ** str_split(char* a_str, const char a_delim);
char ** parse_nodes(char * file,int numline);
struct Nodes_pair * dataset_list (char * file,const char sep,int numline);
char ** path_split(char* path);


#endif
