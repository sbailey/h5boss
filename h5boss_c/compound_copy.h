#ifndef COMPOUND_COPY_H_
#define COMPOUND_COPY_H_
#include<hdf5.h>
typedef struct COADD
{
 float WAVE;
 float FLUX;
 float IVAR;
 int   AND_MASK;
 int   OR_MASK;
 float WAVEDISP;
 float SKY;
 float MODEL; 
}COADD;

typedef struct EXPOSURE
{
 float WAVE;
 float FLUX;
 float IVAR;
 int   MASK;
 float WAVEDISP;
 float SKY;
 float X;
 float CALIB;
}EXPOSURE;

//typedef enum { false, true } bool;
void compound_read(char * src_file,hid_t dst_file, char * path_table, int write,int rank);
void compound_write(hid_t dst_file,char * grp, const char * table_name, hsize_t nrecords,size_t type_size, const size_t * field_offsets, const size_t * field_sizes,void * data);
//void compound_read(char * src_file,char * dst_file, char * path_table, bool write);
//void compound_write(char * dst_file,char * grp, const char * table_name, hsize_t nrecords,size_t type_size, const size_t * field_offsets, const size_t * field_sizes,void * data);
void print_record_cad(hsize_t nrecords,COADD * data);
void print_record_exp(hsize_t nrecords,EXPOSURE * data);
#endif

