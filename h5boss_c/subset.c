/*Reads datasets from sources files, write to existing file, both in parallel
 *Jialin Liu, Aug 8 2016
 *Jalnliu@lbl.gov
 */
#include "stdlib.h"
#include "hdf5.h"
#include "getopt.h"
#include <string.h>
#include "parse_node.h"

#define NAME_MAX 255
char filename[NAME_MAX];
char csvfile[NAME_MAX];
struct Nodes_pari * dl;

int main(int argc, char **argv){
  int      mpi_size, mpi_rank;
  MPI_Comm comm = MPI_COMM_WORLD;
  MPI_Info info;
  MPI_Init(&argc, &argv);
  MPI_Comm_size(comm, &mpi_size);
  MPI_Comm_rank(comm, &mpi_rank);
  if (argc != 3){
    printf("usage: %s output csv",argv[0]);
    return 0;
  }
  int c;
  opterr = 0;
  strncpy(filename, "fiber.h5", NAME_MAX);
  strncpy(csvfile, "fiberlist.txt",NAME_MAX);
  /***input arguments****/ 
  //f: output, m:csv   
  while ((c = getopt (argc, argv, "f:m:")) != -1)
    switch (c)
      {
      case 'f':
	strncpy(filename, optarg, NAME_MAX);
	break;
      case 'm':
	strncpy(csvfile, optarg, NAME_MAX);
      default:
	break;
      }

  MPI_Info_create(&info); 
  //Open file/dataset
  hid_t fapl,file,dataset;
  fapl = H5Pcreate(H5P_FILE_ACCESS);
  H5Pset_fapl_mpio(fapl, comm, info);
  file= H5Fopen(filename, H5F_ACC_RDWR, fapl);
  H5Pclose(fapl);
  if(mpi_rank==0) {
	if(file<0){
	  printf("File %s open error\n",filename); 
	  return 0;
	}
	else {
	  printf("File %s open ok\n",filename);
	}
  }
  const char sep=':';
  dl=dataset_list(argv[1],sep); 
  int total_nodes=dl->count;
  int step = total_nodes /mpi_size +1;
  int rank_start=mpi_rank*step;
  int rank_end=rank_start+step;
  if(mpi_rank == mpi_size-1){
    rank_end=total_nodes;
    if(rank_start>total_nodes){
      rank_start=total_nodes;
    }
  }
 
  hid_t memspace;
  for(i=0; i<rank; i++){  
   rankmemsize*=count[i];
  }
  
 memspace = H5Screate_simple(rank,count,NULL);
  float totalsizegb=mpi_size * rankmemsize / 1024.0 / 1024.0 / 1024.0;
  //alloc buffer for each rank
 //printf("mpisize %d, rankmemsize %d\n",mpi_size,rankmemsize); 
   double * data_t=(double *)malloc(sizeof(double)*rankmemsize);
  if(data_t == NULL){
    printf("Memory allocation fails mpi_rank = %d",mpi_rank);
    for (i=0; i< rank; i++){
    printf("Dim %d: %d, ",i,count[i]);
    }
    exit(1);
    return -1;
  }
 
  MPI_Barrier(comm);
  double t0 = MPI_Wtime();  
  if(mpi_rank == 0){
    if(col==1)
    printf("IO: Collective Read\n");
    else 
    printf("IO: Independent Read\n");
  }
  hid_t plist;
  if(col==1){
   plist = H5Pcreate(H5P_DATASET_XFER);
   H5Pset_dxpl_mpio(plist, H5FD_MPIO_COLLECTIVE);
   H5Dread(dataset, H5T_NATIVE_DOUBLE, memspace,dataspace, plist, data_t);
   //H5Pclose(plist);
  }
  else
   H5Dread(dataset, H5T_NATIVE_DOUBLE, memspace, dataspace, H5P_DEFAULT, data_t);
  //printf("\n\n\ndata_t[0],%f\n\n\n",data_t[0]);  
  MPI_Barrier(comm);
  double t1 = MPI_Wtime()-t0;
  if(mpi_rank==0||mpi_rank==mpi_size-1){ 
  //H5D_mpio_actual_io_mode_t * actual_io_mode;
  //H5Pget_mpio_actual_io_mode(plist, actual_io_mode);
  //uint32_t * local_no_collective_cause=malloc(sizeof(uint32_t));
  //uint32_t * global_no_collective_cause=malloc(sizeof(uint32_t)); 
  //H5Pget_mpio_no_collective_cause( plist, local_no_collective_cause, global_no_collective_cause);
  //printf("actual io mode:%s\n",actual_io_mode); 
  //printf("no collective io local cause %f, global cause %f\n",local_no_collective_cause, global_no_collective_cause);
  printf("\nRank %d, read time %.2fs\n",mpi_rank,t1);
  for(i=0; i<rank; i++){
    printf("Start_%d: %d, Count_%d: %d\n",i,offset[i],i,count[i]);
  }
   printf("\n");
  }
  if(data_t!=NULL)
  free(data_t);
  
  H5Sclose(dataspace);
  H5Sclose(memspace);
  H5Dclose(dataset);
  H5Fclose(file);
  
  MPI_Finalize();
}
