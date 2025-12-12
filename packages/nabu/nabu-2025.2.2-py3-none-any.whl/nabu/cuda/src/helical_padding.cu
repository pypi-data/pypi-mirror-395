
// see  nabu/pipeline/helical/filtering.py for details


__device__  float adjustment_by_integration( int my_rot,  int two_rots , float  *data, int y, int y_mirror, int Nx_padded, int integration_radius, float my_rot_float, float two_rots_float) {
  
  float sigma = integration_radius/3.0f;
  float sum_a=0.0;
  float sum_w_a = 0.0;
  float sum_w_b = 0.0;
  float sum_b=0.0;  
  for(int my_ix = my_rot - integration_radius; my_ix <= my_rot +  integration_radius ; my_ix++) {

    float d = (my_ix - my_rot_float) ;
    float w_a = exp( - (  d*d )/sigma/sigma/2.0f) ; 
    
    sum_a +=    data[ y*Nx_padded + my_ix ] * w_a;
    sum_w_a+= w_a;
    
    int x_mirror = two_rots - my_ix ;

    d = (x_mirror - (two_rots_float -my_rot_float)) ;
    float w_b = exp( - (  d*d )/sigma/sigma/2.0f);
    
    sum_b  +=    data[ y_mirror*Nx_padded + x_mirror ] * w_b;
    sum_w_b += w_b;
  }
  float adjustment  = (sum_b/sum_w_b - sum_a/sum_w_b)   ;
  return adjustment ;
}
  

__global__ void padding(
    float* data,
    int* mirror_indexes,
    
#if defined(MIRROR_CONSTANT_VARIABLE_ROT_POS) || defined(MIRROR_EDGES_VARIABLE_ROT_POS)
    float *rot_axis_pos,
#else
    float rot_axis_pos,    
#endif
    int Nx,
    int Ny,
    int Nx_padded,
    int pad_left_len,
    int pad_right_len
#if defined(MIRROR_CONSTANT) || defined(MIRROR_CONSTANT_VARIABLE_ROT_POS)
    ,float pad_left_val,
    float pad_right_val    
#endif
) {
  
  int x = blockDim.x * blockIdx.x + threadIdx.x;
  int y = blockDim.y * blockIdx.y + threadIdx.y;
    
  if ((x >= Nx_padded) || (y >= Ny) || x < Nx) return;
    
  int idx = y*Nx_padded  +  x;

  int y_mirror = mirror_indexes[y];
  
  int x_mirror =0 ; 
 
#if defined(MIRROR_CONSTANT_VARIABLE_ROT_POS) || defined(MIRROR_EDGES_VARIABLE_ROT_POS)
  float two_rots = rot_axis_pos[y] + rot_axis_pos[y_mirror];
  float my_rot = rot_axis_pos[y];
    
#else
  float two_rots = 2*rot_axis_pos ;
  float my_rot = rot_axis_pos;
#endif

  int two_rots_int = __float2int_rn(two_rots) ;
  int my_rot_int = __float2int_rn(my_rot);


  
  if( two_rots_int > Nx)  {
    int integration_radius =  min( 30,  Nx-1 - max(my_rot_int, two_rots_int - my_rot_int   )  )   ; 
    x_mirror = two_rots_int - x ;
    if (x_mirror  < 0 ) {
#if defined(MIRROR_CONSTANT) || defined(MIRROR_CONSTANT_VARIABLE_ROT_POS)
      if( x < Nx_padded - pad_left_len) {
	data[idx] = pad_left_val;
      } else {
	data[idx] = pad_right_val; 
      }
#else
      if( x < Nx_padded - pad_left_len) {
	float adjustment = adjustment_by_integration( my_rot_int,  two_rots_int , data, y, y_mirror, Nx_padded, integration_radius, my_rot, two_rots);
	
	data[idx] = data[y_mirror*Nx_padded  + 0] - adjustment;
      } else {
	data[idx] = data[y*Nx_padded  +  0];
      }
#endif

    } else {
      float adjustment = adjustment_by_integration( my_rot_int,  two_rots_int , data, y, y_mirror, Nx_padded, integration_radius, my_rot, two_rots);

      data[idx] = data[y_mirror*Nx_padded  +  x_mirror]-adjustment;
    }
  } else {
    int integration_radius =  min( 30,  min(my_rot_int, two_rots_int - my_rot_int) -1)     ;   
    x_mirror = two_rots_int - (x - Nx_padded) ;
    if (x_mirror  > Nx-1 ) {
#if defined(MIRROR_CONSTANT) || defined(MIRROR_CONSTANT_VARIABLE_ROT_POS)
      if( x < Nx_padded - pad_left_len) {
	data[idx] =  pad_left_val ;
      } else {
	data[idx] = pad_right_val;
      }
#else
      if( x < Nx_padded - pad_left_len) {
	data[idx] = data[y*Nx_padded  + Nx - 1 ];
      } else {
	float adjustment = adjustment_by_integration( my_rot_int,  two_rots_int , data, y, y_mirror, Nx_padded, integration_radius, my_rot, two_rots);

	data[idx] = data[y_mirror*Nx_padded  +  Nx-1]-adjustment;
      }
#endif

    } else {
      float adjustment = adjustment_by_integration( my_rot_int,  two_rots_int, data, y, y_mirror, Nx_padded, integration_radius, my_rot, two_rots);
      
      data[idx] = data[y_mirror*Nx_padded  +  x_mirror] - adjustment;
    }
  }
  return;
}

