/*Reads datasets from sources files, write to existing file, both in parallel
 *Jialin Liu, Aug 8 2016
 *Jalnliu@lbl.gov
 */
#include "stdlib.h"
#include "hdf5.h"
#include "getopt.h"
#include "parse_node.h"
#include "compound_copy.h"
#include<stdio.h>
#include <string.h>
#include <assert.h>
#include<time.h>
#define NAME_MAX 255
char filename[NAME_MAX];
char csvfile[NAME_MAX];

int main(int argc, char **argv){
  int      mpi_size, mpi_rank;
  MPI_Comm comm = MPI_COMM_WORLD;
  MPI_Info info;
  MPI_Init(&argc, &argv);
  MPI_Comm_size(comm, &mpi_size);
  MPI_Comm_rank(comm, &mpi_rank);
  printf("argc:%d\n",argc);
  if (argc != 5){
    printf("usage: %s -f output -m csv\n",argv[0]);
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
  hid_t fapl,file;
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
  struct Nodes_pair * dl=dataset_list(csvfile,sep);
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
  int i;
  double t0=MPI_Wtime();
  for(i=rank_start;i<rank_end;i++){
   compound_read(dl->values[i],file, dl->keys[i], true);
  }
  MPI_Barrier(comm);
  double t1 = MPI_Wtime()-t0;
  if(mpi_rank==0||mpi_rank==mpi_size-1){ 
  printf("\nRank %d, read time %.2fs\n",mpi_rank,t1);
  }
  H5Fclose(file);
  
  MPI_Finalize();
  return 0;
}
