#define _GNU_SOURCE
#include "parse_node.h"
#include<stdio.h>
#include<stdlib.h>
#include <string.h>
#include <assert.h>


void main(int argc, char ** argv){
   if(argc!=2) {
     printf("usage: %s filename\n",argv[0]);
     exit(EXIT_FAILURE);
   }
   int j;
   const char sep=':';
   struct Nodes_pair * dl=dataset_list(argv[1],sep);
   //parse_nodes(argv[1]);
   char **pf;
   for(j=0;j<dl->count;j++){
    printf("parsed line %d: %s, %s\n",j,dl->keys[j],dl->values[j]);
    pf=path_split(dl->keys[j]);
    printf("path:%s, file:%s\n",pf[0],pf[1]);
    char str1[10];
    strcpy(str1,"2");
    if(strcmp(pf[1],str1)==0) printf("ha");
   }
   exit(EXIT_SUCCESS);
}
