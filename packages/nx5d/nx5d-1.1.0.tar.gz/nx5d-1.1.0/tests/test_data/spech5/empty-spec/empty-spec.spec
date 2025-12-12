#F /home/data/2023/231-cw7-12082-roessle/231-cw7-12083-roessle.spec
#E 1676364643
#D Tue Feb 14 09:50:43 2023
#C fourc  User = specuser
#O0 TwoTheta     Theta       Chi       Phi         Z         X         Y     FBeam
#O1    NBeam  XBeamMon1  XBeamMon2  laser_lens_x  laser_lens_y  laser_lens_foc  pinhole_horiz  pinhole_vert
#O2 PilatusYOffset    R2HGap  R2HOffset  PSVertGap  PSVertOff  SSHorGap  SSHorOff  SSVertGap
#O3 SSVertOff    delay1  duration1    delay2  duration2    delay3  duration3    delay4
#O4 duration4    delmot    delayf    delayn  absorber     monoE    monobr  DMM1_rock
#O5   DMM1_z    DMM1_y  DMM1_screen  DMM2_rock  DMM2_roll    DMM2_z    DMM2_y  DMM2_screen
#O6     FE_x      FE_y      FE_z     APD_x       M1X     M1Yaw       M1Z   M1Pitch
#O7      M2X     M2Yaw       M2Z   M2Pitch  

#S 1  ascan  z -6 -6  1 1
#D Tue Feb 14 10:16:26 2023
#T 1  (Seconds)
#G0 0 0 0 0 0 1 0 0 0 0 0 0 50 0 0.1 0 68 68 50 -1 1 1 3.13542 3.13542 0 463.6 838.8
#G1 1.54 1.54 1.54 90 90 90 4.079990459 4.079990459 4.079990459 90 90 90 1 0 0 0 1 0 60 30 0 0 0 0 60 30 0 -90 0 0 1.54 1.54 0 0
#G3 4.079990459 -6.561207576e-16 -6.561207576e-16 0 -4.079990459 2.498273628e-16 0 0 -4.079990459
#G4 0 0 0 1.54 0 0 0 90 0 0 0 0 0 0 0 0 -180 -180 -180 -180 -180 -180 -180 -180 -180 0
#Q 0 0 0
#P0 0 0 0 0 -5 2.0000047 -12.85 31.4
#P1 9.9993 15.8375 50 8.02625 2.975 -5.26 -2.0356234e-08 -2.2285305
#P2 155 24 0 37 -7.5 1.5 1 0.5
#P3 -0.05 0 50.11 598 20 0 50 200
#P4 20 0 -789500 -789500 0 9499.9965 -12.008819 11232
#P5 -22400 1600 1600 48000 1600 -9600 0 0
#P6 18.4 15.1 1.805 1 0 -0.02 -0.004 -0.215231
#P7 -2 0.17 0 -0.475231 
#N 51
#L Z  H  K  L  Epoch  Seconds  T_euro1  ls_t1  Counter 5  pilatus_max  pilatus_sum  pil_roi  RingCurrent  SBcurrent  SBposition  ls_t1  ls_t2  ls_t3  ls_t4  temp_sample  tau_zero_apd  I0  femto1  femto2  femto3  femto4  femto5  femto6  femtoALL  delay_m  tau_apd  energy  pilatus_max_x  pilatus_max_y  absorber  tau_apd_file  ring_c_file  sb_current_file  I0fast  EURO_CT  TAPD_CT  kei0  orca_0  PH_average  PH_av_std  delay  tau_apd_zero  las_power  FIFERforce  Monitor  Detector
-6 0 0 0 1547.073 1 0 0 0 787628 11644116 1735 15.248652 14.718553 0 0 0 0 0 0 0 1.2197e-10 0 0 0 0 0 0 0 0 0 9500.0003 298 1 0 0 0 0 -4.2371e-12 0 0 0 0 0 0 0 0 0 0 0 0
-6 0 0 0 1549.092 1 0 0 0 787697 11626479 1718 15.240777 14.716329 0 0 0 0 0 0 0 1.2197e-10 0 0 0 0 0 0 0 0 0 9499.9984 298 1 0 0 0 0 -1.8159e-12 0 0 0 0 0 0 0 0 0 0 0 0

#S 2  acquire 1 1 0
#D Tue Feb 14 10:16:50 2023
#T 1  (Seconds)
#G0 0 0 0 0 0 1 0 0 0 0 0 0 50 0 0.1 0 68 68 50 -1 1 1 3.13542 3.13542 0 463.6 838.8
#G1 1.54 1.54 1.54 90 90 90 4.079990459 4.079990459 4.079990459 90 90 90 1 0 0 0 1 0 60 30 0 0 0 0 60 30 0 -90 0 0 1.54 1.54 0 0
#G3 4.079990459 -6.561207576e-16 -6.561207576e-16 0 -4.079990459 2.498273628e-16 0 0 -4.079990459
#G4 0 0 0 1.54 0 0 0 90 0 0 0 0 0 0 0 0 -180 -180 -180 -180 -180 -180 -180 -180 -180 0
#Q 0 0 0
#P0 0 0 0 0 -5 2.0000047 -12.85 31.4
#P1 9.9993 15.8375 50 8.02625 2.975 -5.26 -2.0356234e-08 -2.2285305
#P2 155 24 0 37 -7.5 1.5 1 0.5
#P3 -0.05 0 50.11 598 20 0 50 200
#P4 20 0 -789500 -789500 0 9499.9965 -12.008817 11232
#P5 -22400 1600 1600 48000 1600 -9600 0 0
#P6 18.4 15.1 1.805 1 0 -0.02 -0.004 -0.215231
#P7 -2 0.17 0 -0.475231 
#N 48
#L Time  Epoch  Seconds  T_euro1  ls_t1  Counter 5  pilatus_max  pilatus_sum  pil_roi  RingCurrent  SBcurrent  SBposition  ls_t1  ls_t2  ls_t3  ls_t4  temp_sample  tau_zero_apd  I0  femto1  femto2  femto3  femto4  femto5  femto6  femtoALL  delay_m  tau_apd  energy  pilatus_max_x  pilatus_max_y  absorber  tau_apd_file  ring_c_file  sb_current_file  I0fast  EURO_CT  TAPD_CT  kei0  orca_0  PH_average  PH_av_std  delay  tau_apd_zero  las_power  FIFERforce  Monitor  Detector
9.05991e-06 1569.077 1 0 0 0 782644 11539140 1204 15.170827 14.639822 0 0 0 0 0 0 0 1.2197e-10 0 0 0 0 0 0 0 0 0 9500.0022 298 1 0 0 0 0 6.053e-13 0 0 0 0 0 0 0 0 0 0 0 0

#S 3  timescan 1 0
#D Tue Feb 14 10:19:32 2023
#T 1  (Seconds)
#G0 0 0 0 0 0 1 0 0 0 0 0 0 50 0 0.1 0 68 68 50 -1 1 1 3.13542 3.13542 0 463.6 838.8
#G1 1.54 1.54 1.54 90 90 90 4.079990459 4.079990459 4.079990459 90 90 90 1 0 0 0 1 0 60 30 0 0 0 0 60 30 0 -90 0 0 1.54 1.54 0 0
#G3 4.079990459 -6.561207576e-16 -6.561207576e-16 0 -4.079990459 2.498273628e-16 0 0 -4.079990459
#G4 0 0 0 1.54 0 0 0 90 0 0 0 0 0 0 0 0 -180 -180 -180 -180 -180 -180 -180 -180 -180 0
#Q 0 0 0
#P0 0 0 0 0 -5 2.0000047 -12.85 31.4
#P1 9.9993 15.8375 50 8.02625 2.975 -5.26 -2.0356234e-08 -2.2285305
#P2 155 24 0 37 -7.5 1.5 1 0.5
#P3 -0.05 0 50.11 598 20 0 50 200
#P4 20 0 -789500 -789500 0 9499.9965 -12.008817 11232
#P5 -22400 1600 1600 48000 1600 -9600 0 0
#P6 18.4 15.1 1.805 1 0 -0.02 -0.004 -0.215231
#P7 -2 0.17 0 -0.475231 
#N 48
#L Time  Epoch  Seconds  T_euro1  ls_t1  Counter 5  pilatus_max  pilatus_sum  pil_roi  RingCurrent  SBcurrent  SBposition  ls_t1  ls_t2  ls_t3  ls_t4  temp_sample  tau_zero_apd  I0  femto1  femto2  femto3  femto4  femto5  femto6  femtoALL  delay_m  tau_apd  energy  pilatus_max_x  pilatus_max_y  absorber  tau_apd_file  ring_c_file  sb_current_file  I0fast  EURO_CT  TAPD_CT  kei0  orca_0  PH_average  PH_av_std  delay  tau_apd_zero  las_power  FIFERforce  Monitor  Detector
