# C function definitions for the FFI
CDEF = """
typedef struct {
  double rij[3];
  double eij;
  double cceij;
} PairData;
typedef struct {
  int **index_xyz_array; // LMAX1**4 pointers to index_xyz
  int **non0ctr;
  int **sortedidx;
  int nbas;
  double **log_max_coeff;
  PairData *
      *pairdata; // NULL indicates not-initialized, NO_VALUE can be skipped
} CINTOpt;
typedef struct {
  int *atm;
  int *bas;
  double *env;
  int *shls;
  int natm;
  int nbas;

  int i_l;
  int j_l;
  int k_l;
  int l_l;
  int nfi; // number of cartesian components
  int nfj;
  // in int1e_grids, the grids_offset and the number of grids
  union {
    int nfk;
    int grids_offset;
  };
  union {
    int nfl;
    int ngrids;
  };
  int nf;        // = nfi*nfj*nfk*nfl;
  int rys_order; // = nrys_roots for regular ERIs. can be nrys_roots/2 for SR
                  // ERIs
  int x_ctr[4];

  int gbits;
  int ncomp_e1;     // = 1 if spin free, = 4 when spin included, it
  int ncomp_e2;     // corresponds to POSX,POSY,POSZ,POS1, see cint.h
  int ncomp_tensor; // e.g. = 3 for gradients

  /* values may diff based on the g0_2d4d algorithm */
  int li_ceil; // power of x, == i_l if nabla is involved, otherwise == i_l
  int lj_ceil;
  int lk_ceil;
  int ll_ceil;
  int g_stride_i; // nrys_roots * shift of (i++,k,l,j)
  int g_stride_k; // nrys_roots * shift of (i,k++,l,j)
  int g_stride_l; // nrys_roots * shift of (i,k,l++,j)
  int g_stride_j; // nrys_roots * shift of (i,k,l,j++)
  int nrys_roots;
  int g_size; // ref to cint2e.c g = malloc(sizeof(double)*g_size)

  int g2d_ijmax;
  int g2d_klmax;
  double common_factor;
  double expcutoff;
  double rirj[3]; // diff by sign in different g0_2d4d algorithm
  double rkrl[3];
  double *rx_in_rijrx;
  double *rx_in_rklrx;

  double *ri;
  double *rj;
  double *rk;
  // in int2e or int3c2e, the coordinates of the fourth shell
  // in int1e_grids, the pointer for the grids coordinates
  union {
    double *rl;
    double *grids;
  };

  int (*f_g0_2e)();
  void (*f_g0_2d4d)();
  void (*f_gout)();
  CINTOpt *opt;

  /* values are assigned during calculation */
  int *idx;
  double ai[1];
  double aj[1];
  double ak[1];
  double al[1];
  double fac[1];
  double rij[3];
  double rkl[3];
} CINTEnvVars;
int CINTlen_cart(const int l);
int CINTlen_spinor(const int bas_id, const int *bas);
int CINTcgtos_cart(const int bas_id, const int *bas);
int CINTcgtos_spheric(const int bas_id, const int *bas);
int CINTcgtos_spinor(const int bas_id, const int *bas);
int CINTcgto_cart(const int bas_id, const int *bas);
int CINTcgto_spheric(const int bas_id, const int *bas);
int CINTcgto_spinor(const int bas_id, const int *bas);
int CINTtot_pgto_spheric(const int *bas, const int nbas);
int CINTtot_pgto_spinor(const int *bas, const int nbas);
int CINTtot_cgto_cart(const int *bas, const int nbas);
int CINTtot_cgto_spheric(const int *bas, const int nbas);
int CINTtot_cgto_spinor(const int *bas, const int nbas);
void CINTshells_cart_offset(int ao_loc[], const int *bas, const int nbas);
void CINTshells_spheric_offset(int ao_loc[], const int *bas, const int nbas);
void CINTshells_spinor_offset(int ao_loc[], const int *bas, const int nbas);
double *CINTc2s_bra_sph(double *sph, int nket, double *cart, int l);
double *CINTc2s_ket_sph(double *sph, int nket, double *cart, int l);
double *CINTc2s_ket_sph1(double *sph, double *cart, int lds, int ldc, int l);
double CINTgto_norm(int n, double a);
void CINTinit_2e_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env);
void CINTinit_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env);
void CINTdel_2e_optimizer(CINTOpt **opt);
void CINTdel_optimizer(CINTOpt **opt);
int cint2e_cart(double *opijkl, int *shls, int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt);
void cint2e_cart_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env);
int cint2e_sph(double *opijkl, int *shls, int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt);
void cint2e_sph_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env);
int cint2e(double *opijkl, int *shls, int *atm, int natm, int *bas, int nbas, double *env, CINTOpt *opt);
void cint2e_optimizer(CINTOpt **opt, int *atm, int natm, int *bas, int nbas, double *env);
void CINTc2s_ket_spinor_sf1(double _Complex *gspa, double _Complex *gspb, double *gcart, int lds, int ldc, int nctr, int l, int kappa);
void CINTc2s_iket_spinor_sf1(double _Complex *gspa, double _Complex *gspb, double *gcart, int lds, int ldc, int nctr, int l, int kappa);
void CINTc2s_ket_spinor_si1(double _Complex *gspa, double _Complex *gspb, double *gcart, int lds, int ldc, int nctr, int l, int kappa);
void CINTc2s_iket_spinor_si1(double _Complex *gspa, double _Complex *gspb, double *gcart, int lds, int ldc, int nctr, int l, int kappa);
"""
