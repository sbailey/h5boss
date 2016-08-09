#include"compound_copy.h"
#include"parse_node.h"
#include<stdio.h>
#include<hdf5.h>
#include<stdlib.h>
#include<string.h>



void compound_rw(char * src_file,char * dst_file, char * path_table,void * data, bool write){
  int i;
  hid_t ifile=-1;
  herr_t itable=-1;
  hid_t igroup=-1;
  heer_t ierr=-1;
  hsize_t  nfields, nrecords;
  size_t * field_sizes;
  size_t * field_offsets;
  size_t record_size=0;
  ifile= H5Fopen(src_file,H5F_ACC_RDONLY,H5P_DEFAULT);
  //split keys into group/dataset_table
  char **gt=path_split(path_table);
  igroup= H5Gopen(ifile,gt[0]);
  //ierr=H5TBget_field_info (igroup, gt[1], field_names,field_sizes, field_offsets, type_size);
  ierr=H5TBget_table_info (igroup, gt[1], &nfields, &nrecords);
  //allocate the buffer and read the table in memory
  char tag1[10];
  char tag2[10];
  char tag3[10];
  strcpy(tag1,"coadd");
  strcpy(tag2,"b");
  strcpy(tag3,"r");
  if(strcmp(gt[1],tag1)==0){
   record_size=COADD_REC_SIZE;
   fields_sizes=coadd_sizes;
  }
  else if(strcmp(gt[1],tag3)==0||strcmp(tag2,gt[1])==0){
   record_size=EXPOSURE_REC_SZIE;
   fields_sizes=exposure_sizes;
  }
  data = malloc(nrecords * record_size);
  ierr=H5TBread_table(igroup, gt[1], 0,record_size, field_sizes, data )
  for (i=0;i<nrecords;i++){
   printf ("%f %f %f %d %d %f %f %f",
    data[i].WAVE,
    data[i].FLUX;
    data[i].IVAR;
    data[i].AND_MASK;
    data[i].OR_MASK;
    data[i].WAVEDISP;
    data[i].SKY;
    data[i].MODEL;
   )
   printf("\n");
  }
  //H5TBwrite_records();
  if(!write) return data;
    
}
