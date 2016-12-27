
import math
import numpy as np
import subprocess
import json

QW='/Users/lkwagner/work/qwalk/mainline/bin//qwalk'
GOSLING='/Users/lkwagner/work/qwalk/mainline/bin//gosling'

class H2Runner:
  def __init__(self):
    self.wavefunction="singlet"
    self.r=2.0
    self.optimize_det=True
    self.results={}
    self.average=""" average { region_fluctuation maxn 2 } 
average { gr } 
"""

#---------------------------------------------------------
  def gen_hf(self,fname):
    f=open(fname,'w')
    if self.wavefunction != 'triplet' or self.optimize_det==False:
      f.write("method { LINEAR total_nstep 250 }\n")
    
    f.write("method { vmc nstep 4000 %s }"%self.average)
    self.gen_sys(f)
    self.gen_orb(open("qw.orb",'w'))
    self.gen_basis(open("qw.basis",'w'))
    f.write("TRIALFUNC { \n")
    self.gen_slater(f,basename="qw")
    f.write("}\n")
    f.close()
    stdout=subprocess.check_output([QW,fname])
    #print(stdout)
    self.results['hf']=json.loads(str(subprocess.getoutput(GOSLING+" -json "+fname+".log")))

#---------------------------------------------------------

  def gen_vmc(self,fname):
    f=open(fname,'w')
    f.write("method { LINEAR total_nstep 250 }\n")
    f.write("method { vmc nstep 4000 %s  }"%self.average)
    
    self.gen_sys(f)
    self.gen_orb(open("qw.orb",'w'))
    self.gen_basis(open("qw.basis",'w'))
    f.write("TRIALFUNC { slater-jastrow \n wf1 { \n")
    self.gen_slater(f,basename="qw")
    f.write("\n} \n wf2 { \n")
    self.gen_jast(f)
    f.write("}\n}\n")
    f.close()
    stdout=subprocess.check_output([QW,fname])
   # print(stdout)
    self.results['vmc']=json.loads(str(subprocess.getoutput(GOSLING+" -json "+fname+".log")))
#---------------------------------------------------------

  def gen_dmc(self,fname,wf_file):
    f=open(fname,'w')
    f.write("method { DMC timestep 0.03 nblock 20 %s}\n"%self.average)
    
    self.gen_sys(f)
    self.gen_orb(open("qw.orb",'w'))
    self.gen_basis(open("qw.basis",'w'))
    f.write("TRIALFUNC { include %s }\n"%wf_file)
    f.close()
    stdout=subprocess.check_output([QW,fname])
   # print(stdout)
    self.results['dmc']=json.loads(str(subprocess.getoutput(GOSLING+" -json "+fname+".log")))

  def run_all(self,basename):
    print("no jastrow")
    self.gen_hf(basename+'.hf')
    print("multiple Slater Jastrow")
    self.gen_vmc(basename+'.vmc')
    print("diffusion Monte Carlo")
    self.gen_dmc(basename+'.dmc',basename+'.vmc.wfout')
    

#----------------------------------------------------------
  def gen_sys(self,f):
    f.write("""
SYSTEM { MOLECULE \n""")
    if self.wavefunction=="singlet":
      f.write(" NSPIN { 1  1 } \n")
    elif self.wavefunction=="triplet":
      f.write(" NSPIN { 2 0 } \n")
    f.write("""
ATOM { H  1  COOR 0   0  0.0 }
ATOM { H  1  COOR 0   0  %g }
} 
    """%self.r )
#-----------------------------------------------------------
  def gen_basis(self,f):
    x=np.linspace(0,20,200)
    y=np.exp(-x)
    f.write("""
BASIS { 
H
AOSPLINE

CUSP -1
SPLINE { S 
""")
    for i,j in zip(x,y):
      f.write("%.10f %.10f\n"%(i,j))
    f.write("}\n}\n")
#----------------------------------------------------------
  def gen_slater(self,f,basename="qwalk"):
    f.write("""SLATER
  ORBITALS {
  CUTOFF_MO
    MAGNIFY 1
    NMO 2
    ORBFILE %s.orb
    INCLUDE %s.basis
    CENTERS { USEATOMS } 
  }
"""%(basename,basename))
    if self.wavefunction=="singlet":
      f.write("""  STATES {
   1 2 
   2 1 
   1 1
   2 2
      } )
      CSF { 1.0 1.0 1.0 } CSF{ 0.9 1.0 1.0 } \n""")
    if self.wavefunction=="triplet":
      f.write("""
      STATES { 1 2 2 1 } 
      CSF { 1.0 1.0 -1.0 } \n""")
    if self.optimize_det==True:
      f.write("OPTIMIZE_DET")
#----------------------------------------------------------

  def gen_orb(self,f):
    f.write("""1 1 1 1
2 1 2 1
COEFFICIENTS
1.0 \n""")


#----------------------------------------------------------
  def gen_jast(self,f):
    f.write("""
  JASTROW2
  GROUP { 
    TWOBODY_SPIN { 
      FREEZE
      LIKE_COEFFICIENTS { 0.25  0   } 
      UNLIKE_COEFFICIENTS { 0  0.5   }  
    } 
    EEBASIS { 
      EE
      CUTOFF_CUSP
      GAMMA 24
      CUSP 1
      CUTOFF 7.5
    }
    EEBASIS { 
      EE
      CUTOFF_CUSP
      GAMMA 24
      CUSP 1
      CUTOFF 7.5
    }
  }
  GROUP { 
    ONEBODY { 
      COEFFICIENTS { H 0. 0. 0. } 
    } 
    TWOBODY { 
      COEFFICIENTS { 0. 0. 0. } 
    } 
    EIBASIS { 
      H
      POLYPADE
      RCUT 7.5
      BETA0 -0.4
      NFUNC 3
    }
    EEBASIS { 
      EE
      POLYPADE
      RCUT 7.5
      BETA0 -0.02
      NFUNC 3
    }
  }
""") 

#----------------------------------------------------------

def generate_dataframe(runners):
  df={'wavefunction':[],
      'r':[],
      'optimize_det':[],
      'slat_en':[],
      'slat_en_err':[],
      'slatgr':[],
      'slatgr_err':[],
      'sj_en':[],
      'sj_en_err':[],
      'sjgr':[],
      'sjgr_err':[],
      'dmc_en':[],
      'dmc_en_err':[],
      'dmcgr':[],
      'dmcgr_err':[],
      'gr_r':[]
      }
  for r in runners:
    df['r'].append(r.r)
    df['optimize_det'].append(r.optimize_det)
    df['wavefunction'].append(r.wavefunction)
    df['slat_en'].append(r.results['hf']['properties']['total_energy']['value'][0])
    df['slat_en_err'].append(r.results['hf']['properties']['total_energy']['error'][0])
    df['sj_en'].append(r.results['vmc']['properties']['total_energy']['value'][0])
    df['sj_en_err'].append(r.results['vmc']['properties']['total_energy']['error'][0])
    df['dmc_en'].append(r.results['dmc']['properties']['total_energy']['value'][0])
    df['dmc_en_err'].append(r.results['dmc']['properties']['total_energy']['error'][0])
    gr_channel='unlike'
    if r.wavefunction=='triplet':
      gr_channel='like'

    df['gr_r'].append(r.results['hf']['properties']['gr']['r'])

    df['slatgr'].append(r.results['hf']['properties']['gr'][gr_channel])
    df['slatgr_err'].append(r.results['hf']['properties']['gr'][gr_channel+'_err'])

    df['sjgr'].append(r.results['vmc']['properties']['gr'][gr_channel])
    df['sjgr_err'].append(r.results['vmc']['properties']['gr'][gr_channel+'_err'])

    df['dmcgr'].append(r.results['dmc']['properties']['gr'][gr_channel])
    df['dmcgr_err'].append(r.results['dmc']['properties']['gr'][gr_channel+'_err'])
    
    for n,d in zip(['slat','sj','dmc'],['hf','vmc','dmc']):
      nm=n+'_double'
      if nm not in df.keys():
        df[nm]=[]
        df[nm+'_err']=[]

      df[nm].append(r.results[d]['properties']['region_fluctuation']['fluctuation data'][4]['value'][1][1])
      df[nm+'_err'].append(r.results[d]['properties']['region_fluctuation']['fluctuation data'][4]['error'][1][1])

  return df


if __name__=="__main__":
  print("hello")
  runner=H2Runner()
  runner.gen_hf("qw.hf")
  runner.gen_vmc("qw.vmc")
  print(runner.results)
  
