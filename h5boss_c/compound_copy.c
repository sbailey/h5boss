#include"compound_copy.h"
#include"parse_node.h"
#include<stdio.h>
#include<hdf5.h>
#include<stdlib.h>
#include<string.h>
#include<hdf5_hl.h>//this is needed for using the hdf5 table api
size_t COADD_REC_SIZE=sizeof(struct COADD);
size_t EXPOSURE_REC_SIZE=sizeof(struct EXPOSURE);
#define NFIELDS   (hsize_t) 8
#define TABLE_COADD_NAME "coadd"
#define TABLE_EXPOSURE_B_NAME "b"
#define TABLE_EXPOSURE_R_NAME "r"

size_t coadd_sizes[NFIELDS] = {sizeof(float),
                               sizeof(float),
                               sizeof(float),
                               sizeof(int),
                               sizeof(int),
                               sizeof(float),
                               sizeof(float),
                               sizeof(float)};
size_t coadd_offset[NFIELDS] = {
				HOFFSET( COADD, WAVE ),
				HOFFSET( COADD, FLUX ),
				HOFFSET( COADD, IVAR ),
				HOFFSET( COADD, AND_MASK ),
				HOFFSET( COADD, OR_MASK ),
				HOFFSET( COADD, WAVEDISP ),
				HOFFSET( COADD, SKY ),
				HOFFSET( COADD, MODEL ),
				};
size_t exposure_offset[NFIELDS] = {
                                HOFFSET( EXPOSURE, WAVE ),
                                HOFFSET( EXPOSURE, FLUX ),
                                HOFFSET( EXPOSURE, IVAR ),
                                HOFFSET( EXPOSURE, MASK ),
                                HOFFSET( EXPOSURE, WAVEDISP ),
                                HOFFSET( EXPOSURE, SKY ),
                                HOFFSET( EXPOSURE, X),
                                HOFFSET( EXPOSURE, CALIB ),
                                };
size_t exposure_sizes[NFIELDS] ={sizeof(float),
                               sizeof(float),
                               sizeof(float),
                               sizeof(int),
                               sizeof(float),
                               sizeof(float),
                               sizeof(float),
                               sizeof(float)};

void print_record_cad(hsize_t nrecords,COADD * data){
  hsize_t i;
  for (i=0;i<nrecords;i++){
   printf ("%lld:%f %f %f %d %d %f %f %f\n",i,
    data[i].WAVE,
    data[i].FLUX,
    data[i].IVAR,
    data[i].AND_MASK,
    data[i].OR_MASK,
    data[i].WAVEDISP,
    data[i].SKY,
    data[i].MODEL
   );
  }
}
void print_record_exp(hsize_t nrecords,EXPOSURE * data){
  hsize_t i;
  for (i=0;i<nrecords;i++){
   printf ("%lld:%f %f %f %d %f %f %f %f\n", i,
    data[i].WAVE,
    data[i].FLUX,
    data[i].IVAR,
    data[i].MASK,
    data[i].WAVEDISP,
    data[i].SKY,
    data[i].X,
    data[i].CALIB
   );
  }
}
//void compound_read(char * src_file,char * dst_file, char * path_table, bool write){
void compound_read(char * src_file, hid_t dst_file, char * path_table, int write,int rank){
  hid_t ifile=-1;
  hid_t igroup=-1;
  hid_t fapl_id=-1;
  herr_t ierr=-1;
  hsize_t  nfields, nrecords;
  size_t * field_sizes;
  size_t * field_offsets;
  size_t record_size=0;
  //hbool_t is_collective=false;
  //fapl_id = H5Pcopy(H5P_FILE_ACCESS);
  //H5Pset_all_coll_metadata_ops(fapl_id,is_collective);
  //ifile= H5Fopen(src_file,H5F_ACC_RDONLY,fapl_id);
  ifile= H5Fopen(src_file,H5F_ACC_RDONLY,H5P_DEFAULT);
  //H5Pclose(fapl_id);
//printf("ifile = %d / %0x\n", (int)ifile, (unsigned)ifile);
  if(ifile<0) printf("srcfile '%s' open error in rank %d\n",src_file,rank);
  //else printf("srcfile '%s' open correctly rank %d\n",src_file, rank);

  //split keys into group/dataset_table
  char **gt=path_split(path_table);
  igroup= H5Gopen(ifile,gt[0],H5P_DEFAULT);
  if(igroup<0) printf("group '%s' open error rank: %d\n",gt[0],rank);
  //ierr=H5TBget_field_info (igroup, gt[1], field_names,field_sizes, field_offsets, type_size);
  ierr=H5TBget_table_info (igroup, gt[1], &nfields, &nrecords);
  if(ierr<0) printf("ierr of get table info:%d in rank %d\n",ierr,rank);
  //allocate the buffer and read the table in memory
  char tag1[10];
  char tag2[10];
  char tag3[10];
  strcpy(tag1,"coadd");
  strcpy(tag2,"b");
  strcpy(tag3,"r");
  if(strcmp(gt[1],tag1)==0){
   record_size=COADD_REC_SIZE;
   field_sizes=coadd_sizes;
   field_offsets=coadd_offset;
   COADD * data = malloc(nrecords * record_size);
   ierr=H5TBread_table(igroup, gt[1], record_size, field_offsets, field_sizes, data);
   if(ierr<0) printf("ierr of read table info:%d\n",ierr);
   //print_record_cad(nrecords,data); 
   //printf("number of records:%ld\n",nrecords);
   if(write) {
    compound_write(dst_file,gt[0],gt[1], nrecords, record_size, field_offsets, field_sizes,data);
   }
   if(data!=NULL) free(data);
  }
  else if(strcmp(gt[1],tag3)==0||strcmp(tag2,gt[1])==0){
   record_size=EXPOSURE_REC_SIZE;
   field_sizes=exposure_sizes;
   field_offsets=exposure_offset;
   EXPOSURE * data = malloc(nrecords * record_size);
   ierr=H5TBread_table(igroup, gt[1], record_size, field_offsets, field_sizes, data);
   //print_record_exp(nrecords,data);
   
   if(write) {
    compound_write(dst_file,gt[0],gt[1], nrecords, record_size,field_offsets, field_sizes,data);
   }
   if(data!=NULL) free(data);
  }
  H5Gclose(igroup);
  H5Fclose(ifile);  
}

//void compound_write(char * dst_file,char * grp, const char * table_name, hsize_t nrecords,size_t type_size, const size_t * field_offsets, const size_t * field_sizes,void * data){
void compound_write(hid_t dst_file,char * grp, const char * table_name, hsize_t nrecords,size_t type_size, const size_t * field_offsets, const size_t * field_sizes,void * data){
  herr_t ierr=-1;
  hid_t igroup=-1;
  hid_t ifile=-1;
  //ifile= H5Fopen(dst_file,H5F_ACC_RDWR,H5P_DEFAULT);
  //if(ifile<0) printf("file open error:%s",dst_file);
  ifile=dst_file;
  igroup= H5Gopen(ifile,grp,H5P_DEFAULT);
  ierr=H5TBwrite_records ( igroup, table_name, 0, nrecords, type_size, field_offsets, field_sizes, data);
  if(ierr<0) printf("write records error\n");
  if(igroup>=0) H5Gclose(igroup);
  //if(ifile>=0)  H5Fclose(ifile);
}
