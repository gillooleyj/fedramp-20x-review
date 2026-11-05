# Rules Change Report: 2026.10.05.01 to 2026.11.02.01

## Applicability by Class

| Class | Rules (old to new) | KSIs (old to new) | Added | Removed | Force changed | Statement changed |
| --- | --- | --- | --- | --- | --- | --- |
| A | 50 to 51 | 7 to 7 | SDR-CSX-KSI | None | None | MKT-CSO-PML |
| B | 155 to 154 | 46 to 46 | None | FRC-CSX-MOT | SDR-CSX-KMT (MUST to SHOULD) | KSI-SCR-MIT, MKT-CSO-PML, SDR-CSX-KMT |
| C | 155 to 154 | 46 to 46 | None | FRC-CSX-MOT | None | KSI-SCR-MIT, MKT-CSO-PML |

## High Severity (5)

- `FRC-CLA-MFR` (FRR, `FRR.FRC.data.all.CLA.FRC-CLA-MFR`): overlay
- `FRC-CLA-RFR` (FRR, `FRR.FRC.data.all.CLA.FRC-CLA-RFR`): overlay
- `FRC-CSX-MOT` (FRR, `FRR.FRC.data.20x.CSX.FRC-CSX-MOT`): removed
- `FRD-MAS` (FRD, `FRD.data.all.FRD-MAS`): added
- `SDR-CSX-KMT` (FRR, `FRR.SDR.data.20x.CSX.SDR-CSX-KMT`): force

## Medium Severity (8)

- `FRC-CCL-UCC` (FRR, `FRR.FRC.data.all.CCL.FRC-CCL-UCC`): statement
- `FRD-SNT` (FRD, `FRD.data.all.FRD-SNT`): definition
- `IEC-CSO-FIR` (FRR, `FRR.IEC.data.all.CSO.IEC-CSO-FIR`): notification
- `IEC-CSO-IIR` (FRR, `FRR.IEC.data.all.CSO.IEC-CSO-IIR`): notification
- `IEC-CSO-OIR` (FRR, `FRR.IEC.data.all.CSO.IEC-CSO-OIR`): notification
- `KSI-SCR-MIT` (KSI, `KSI.SCR.indicators.KSI-SCR-MIT`): statement
- `MKT-CSO-PML` (FRR, `FRR.MKT.data.all.CSO.MKT-CSO-PML`): statement
- `SDR-CSX-KMT` (FRR, `FRR.SDR.data.20x.CSX.SDR-CSX-KMT`): statement, following_information

## Low Severity (90)

- `AFC-CSO-INB` (FRR, `FRR.AFC.data.all.CSO.AFC-CSO-INB`): controls
- `AGU-USE-RSG` (FRR, `FRR.AGU.data.all.USE.AGU-USE-RSG`): controls
- `CCM-OCR-AVL` (FRR, `FRR.CCM.data.all.OCR.CCM-OCR-AVL`): controls
- `CCM-QTR-ACT` (FRR, `FRR.CCM.data.all.QTR.CCM-QTR-ACT`): controls
- `CCM-QTR-MTG` (FRR, `FRR.CCM.data.all.QTR.CCM-QTR-MTG`): controls
- `CDS-CSO-SVC` (FRR, `FRR.CDS.data.all.CSO.CDS-CSO-SVC`): terms, updated_not_recorded
- `CMU-CSO-CMD` (FRR, `FRR.CMU.data.all.CSO.CMU-CSO-CMD`): controls
- `CMU-CSO-UVM` (FRR, `FRR.CMU.data.all.CSO.CMU-CSO-UVM`): controls
- `CPO-CSO-OSA` (FRR, `FRR.CPO.data.all.CSO.CPO-CSO-OSA`): controls
- `CPO-CSO-OVR` (FRR, `FRR.CPO.data.all.CSO.CPO-CSO-OVR`): terms, updated_not_recorded
- `FRC-CCL-DCC` (FRR, `FRR.FRC.data.all.CCL.FRC-CCL-DCC`): notes
- `FRC-CCL-UCC` (FRR, `FRR.FRC.data.all.CCL.FRC-CCL-UCC`): notes
- `FRC-CLA-MFR` (FRR, `FRR.FRC.data.all.CLA.FRC-CLA-MFR`): related, terms
- `FRC-CLA-RFR` (FRR, `FRR.FRC.data.all.CLA.FRC-CLA-RFR`): related
- `FRC-CSX-MAS` (FRR, `FRR.FRC.data.20x.CSX.FRC-CSX-MAS`): terms, updated_not_recorded
- `FRC-CSX-VVK` (FRR, `FRR.FRC.data.20x.CSX.FRC-CSX-VVK`): controls
- `FRC-CSX-VVR` (FRR, `FRR.FRC.data.20x.CSX.FRC-CSX-VVR`): controls
- `FRD-CRP` (FRD, `FRD.data.all.FRD-CRP`): reference_url, updated_not_recorded
- `FRD-FCR` (FRD, `FRD.data.all.FRD-FCR`): reference, reference_url, updated_not_recorded
- `FRD-FCT` (FRD, `FRD.data.all.FRD-FCT`): reference, reference_url, updated_not_recorded
- `FRD-VLN` (FRD, `FRD.data.all.FRD-VLN`): reference, reference_url, updated_not_recorded
- `FRD-VRF` (FRD, `FRD.data.all.FRD-VRF`): reference, reference_url, updated_not_recorded
- `IEC-CSO-EFR` (FRR, `FRR.IEC.data.all.CSO.IEC-CSO-EFR`): controls
- `IEC-CSO-FIR` (FRR, `FRR.IEC.data.all.CSO.IEC-CSO-FIR`): controls
- `IEC-CSO-IIR` (FRR, `FRR.IEC.data.all.CSO.IEC-CSO-IIR`): controls
- `IEC-CSO-OIR` (FRR, `FRR.IEC.data.all.CSO.IEC-CSO-OIR`): controls
- `IVV-CSO-FIA` (FRR, `FRR.IVV.data.all.CSO.IVV-CSO-FIA`): controls
- `IVV-IAS-VEF` (FRR, `FRR.IVV.data.all.IAS.IVV-IAS-VEF`): controls, updated_not_recorded
- `KSI-CED-RAT` (KSI, `KSI.CED.indicators.KSI-CED-RAT`): controls
- `KSI-CMT-LMC` (KSI, `KSI.CMT.indicators.KSI-CMT-LMC`): controls
- `KSI-CMT-VTD` (KSI, `KSI.CMT.indicators.KSI-CMT-VTD`): controls
- `KSI-CNA-DFP` (KSI, `KSI.CNA.indicators.KSI-CNA-DFP`): controls
- `KSI-CNA-EIS` (KSI, `KSI.CNA.indicators.KSI-CNA-EIS`): controls
- `KSI-CNA-IBP` (KSI, `KSI.CNA.indicators.KSI-CNA-IBP`): controls
- `KSI-CNA-MAT` (KSI, `KSI.CNA.indicators.KSI-CNA-MAT`): controls
- `KSI-CNA-OFA` (KSI, `KSI.CNA.indicators.KSI-CNA-OFA`): controls
- `KSI-CNA-RNT` (KSI, `KSI.CNA.indicators.KSI-CNA-RNT`): controls
- `KSI-CNA-RVP` (KSI, `KSI.CNA.indicators.KSI-CNA-RVP`): controls
- `KSI-CNA-ULN` (KSI, `KSI.CNA.indicators.KSI-CNA-ULN`): controls
- `KSI-IAM-AAM` (KSI, `KSI.IAM.indicators.KSI-IAM-AAM`): controls
- `KSI-IAM-APM` (KSI, `KSI.IAM.indicators.KSI-IAM-APM`): controls
- `KSI-IAM-ELP` (KSI, `KSI.IAM.indicators.KSI-IAM-ELP`): controls
- `KSI-IAM-JIT` (KSI, `KSI.IAM.indicators.KSI-IAM-JIT`): controls
- `KSI-IAM-SNU` (KSI, `KSI.IAM.indicators.KSI-IAM-SNU`): controls
- `KSI-IAM-SUS` (KSI, `KSI.IAM.indicators.KSI-IAM-SUS`): controls
- `KSI-INR-AAR` (KSI, `KSI.INR.indicators.KSI-INR-AAR`): controls
- `KSI-INR-RIR` (KSI, `KSI.INR.indicators.KSI-INR-RIR`): controls
- `KSI-INR-RPI` (KSI, `KSI.INR.indicators.KSI-INR-RPI`): controls
- `KSI-MLA-ALA` (KSI, `KSI.MLA.indicators.KSI-MLA-ALA`): controls
- `KSI-MLA-EVC` (KSI, `KSI.MLA.indicators.KSI-MLA-EVC`): controls
- `KSI-MLA-LET` (KSI, `KSI.MLA.indicators.KSI-MLA-LET`): controls
- `KSI-MLA-OSM` (KSI, `KSI.MLA.indicators.KSI-MLA-OSM`): controls
- `KSI-MLA-RVL` (KSI, `KSI.MLA.indicators.KSI-MLA-RVL`): controls
- `KSI-PIY-GIV` (KSI, `KSI.PIY.indicators.KSI-PIY-GIV`): controls
- `KSI-PIY-RIS` (KSI, `KSI.PIY.indicators.KSI-PIY-RIS`): controls
- `KSI-PIY-RSD` (KSI, `KSI.PIY.indicators.KSI-PIY-RSD`): controls
- `KSI-RPL-ABO` (KSI, `KSI.RPL.indicators.KSI-RPL-ABO`): controls
- `KSI-RPL-TRC` (KSI, `KSI.RPL.indicators.KSI-RPL-TRC`): controls
- `KSI-SCR-MIT` (KSI, `KSI.SCR.indicators.KSI-SCR-MIT`): controls
- `KSI-SCR-MON` (KSI, `KSI.SCR.indicators.KSI-SCR-MON`): controls
- `KSI-SVC-ACM` (KSI, `KSI.SVC.indicators.KSI-SVC-ACM`): controls
- `KSI-SVC-ASM` (KSI, `KSI.SVC.indicators.KSI-SVC-ASM`): controls
- `KSI-SVC-EIS` (KSI, `KSI.SVC.indicators.KSI-SVC-EIS`): controls
- `KSI-SVC-PRR` (KSI, `KSI.SVC.indicators.KSI-SVC-PRR`): controls
- `KSI-SVC-RUD` (KSI, `KSI.SVC.indicators.KSI-SVC-RUD`): controls
- `KSI-SVC-SIN` (KSI, `KSI.SVC.indicators.KSI-SVC-SIN`): controls
- `KSI-SVC-VCM` (KSI, `KSI.SVC.indicators.KSI-SVC-VCM`): controls
- `KSI-SVC-VRI` (KSI, `KSI.SVC.indicators.KSI-SVC-VRI`): controls
- `MAS-CSO-FLO` (FRR, `FRR.MAS.data.all.CSO.MAS-CSO-FLO`): controls
- `MAS-CSO-IIR` (FRR, `FRR.MAS.data.all.CSO.MAS-CSO-IIR`): controls
- `MAS-CSO-MDI` (FRR, `FRR.MAS.data.all.CSO.MAS-CSO-MDI`): terms, updated_not_recorded
- `MAS-CSO-TPR` (FRR, `FRR.MAS.data.all.CSO.MAS-CSO-TPR`): controls, terms
- `SCG-CSO-RSC` (FRR, `FRR.SCG.data.all.CSO.SCG-CSO-RSC`): controls
- `SCN-CSO-EMG` (FRR, `FRR.SCN.data.all.CSO.SCN-CSO-EMG`): controls
- `SCN-CSO-EVA` (FRR, `FRR.SCN.data.all.CSO.SCN-CSO-EVA`): controls
- `SDR-CSX-KMT` (FRR, `FRR.SDR.data.20x.CSX.SDR-CSX-KMT`): note, terms
- `VDR-CSO-ADT` (FRR, `FRR.VDR.data.all.CSO.VDR-CSO-ADT`): controls
- `VDR-CSO-AKE` (FRR, `FRR.VDR.data.all.CSO.VDR-CSO-AKE`): controls
- `VDR-CSO-DAC` (FRR, `FRR.VDR.data.all.CSO.VDR-CSO-DAC`): controls
- `VDR-CSO-DET` (FRR, `FRR.VDR.data.all.CSO.VDR-CSO-DET`): controls
- `VDR-CSO-FAV` (FRR, `FRR.VDR.data.all.CSO.VDR-CSO-FAV`): controls
- `VDR-CSO-MSP` (FRR, `FRR.VDR.data.all.CSO.VDR-CSO-MSP`): controls
- `VDR-CSO-RES` (FRR, `FRR.VDR.data.all.CSO.VDR-CSO-RES`): controls
- `VDR-CSO-SIR` (FRR, `FRR.VDR.data.all.CSO.VDR-CSO-SIR`): controls
- `VDR-TFR-PDD` (FRR, `FRR.VDR.data.all.TFR.VDR-TFR-PDD`): controls
- `VDR-TFR-PVR` (FRR, `FRR.VDR.data.all.TFR.VDR-TFR-PVR`): controls
- `VER-EVA-EFA` (FRR, `FRR.VER.data.all.EVA.VER-EVA-EFA`): controls
- `VER-EVA-EPA` (FRR, `FRR.VER.data.all.EVA.VER-EVA-EPA`): controls
- `VER-RPT-PER` (FRR, `FRR.VER.data.all.RPT.VER-RPT-PER`): controls
- `VER-RPT-VDT` (FRR, `FRR.VER.data.all.RPT.VER-RPT-VDT`): controls

## Dataset Info

- `last_updated` changed
- `version` changed
