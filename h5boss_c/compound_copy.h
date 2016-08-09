#ifndef COMPOUND_COPY_H_
#define COMPOUND_COPY_H_

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
};

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
}

size_t COADD_REC_SIZE=sizeof(COADD);
size_t EXPOSURE_REC_SIZE=sizeof(EXPOSURE);
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
size_t exposure_sizes[NFIELDS] ={sizeof(float),
                               sizeof(float),
                               sizeof(float),
                               sizeof(int),
                               sizeof(float),
                               sizeof(float),
                               sizeof(float),
                               sizeof(float)};
#endif

