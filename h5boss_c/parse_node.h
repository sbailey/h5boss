#ifndef PARSE_NODES_H_
#define PARSE_NODES_H_

struct Fiber{
    int count;     // number of counts, e.g., 188000
    char ** keys;  // a list of fiber dataset name, e.g., 5732/56326/936/coadd
    char ** values;// a list of file path, /global/cscratch1/sd/jialin/h5boss/5732-56326.hdf5
}; 
struct Catalog{
    int count;       // number of catalog rows, e.g., 19800
    char ** plate_mjd;// a list of plate/mjd pair, e.g., 3690/55182
    char ** fiber_id; // a list of fiber id, e.g., 181 
    char ** filepath; // a list of file path, e.g., global/cscratch1/sd/jialin/h5boss/3690-55182.hdf5
    char ** fiber_offset; // a list of fiber offsets, e.g., 0
};
//split a string by delimiter, return a char **
char ** str_split(char* a_str, const char a_delim);
char ** parse_nodes(char * file,int numline);
struct Fiber * dataset_list (char * file,const char sep,int numline);
struct Catalog * catalog_list (char * file, const char sep, int numline);
char ** path_split(char* path);


#endif
